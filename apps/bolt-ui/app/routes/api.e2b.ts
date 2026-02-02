/**
 * E2B Server-Side Proxy API
 *
 * This route handles all E2B operations server-side to avoid CORS issues.
 * The browser cannot directly communicate with E2B sandboxes due to CORS policy.
 */

import { json, type ActionFunctionArgs, type LoaderFunctionArgs } from '@remix-run/cloudflare';
import { Sandbox } from '@e2b/code-interpreter';
import nodePath from 'node:path';

// Store active sandboxes (in production, use Redis or similar)
export const activeSandboxes = new Map<string, Sandbox>();

const BASE_PATH = '/home/user/project';

/**
 * Normalize paths to work correctly in E2B sandbox
 * - /home/project/... → /home/user/project/...
 * - relative paths → /home/user/project/...
 * - Resolves .. and . components
 * - Ensures paths stay within project directory
 */
function resolvePath(inputPath: string): string {
  let workingPath = inputPath;

  // Handle /home/project/ prefix (WebContainer compatibility)
  if (workingPath.startsWith('/home/project/')) {
    workingPath = workingPath.substring('/home/project/'.length);
  } else if (workingPath === '/home/project') {
    return BASE_PATH;
  }
  // Handle /home/user/project/ prefix - extract relative part
  else if (workingPath.startsWith('/home/user/project/')) {
    workingPath = workingPath.substring('/home/user/project/'.length);
  } else if (workingPath === '/home/user/project') {
    return BASE_PATH;
  }
  // Handle other /home/user/ paths - extract relative part
  else if (workingPath.startsWith('/home/user/')) {
    workingPath = workingPath.substring('/home/user/'.length);
  }
  // Handle other absolute paths - keep as relative
  else if (workingPath.startsWith('/')) {
    workingPath = workingPath.substring(1);
  }

  // Normalize the path to resolve .. and . components
  // Use posix to ensure forward slashes on all platforms
  const normalizedRelative = nodePath.posix.normalize(workingPath);

  // Prevent path traversal outside project
  if (normalizedRelative.startsWith('..') || normalizedRelative.startsWith('/')) {
    console.warn('[E2B API] Path traversal attempt blocked:', inputPath, '→', normalizedRelative);
    // Default to src directory for components
    if (inputPath.includes('/src/')) {
      const srcIndex = inputPath.lastIndexOf('/src/');
      return `${BASE_PATH}${inputPath.substring(srcIndex)}`;
    }
    return BASE_PATH;
  }

  return `${BASE_PATH}/${normalizedRelative}`;
}

// --- Command validator (exported for unit + integration tests) ---
export function isSafeCommand(cmd: string) {
  if (!cmd || typeof cmd !== 'string') return { ok: false, reason: 'invalid' };

  // Disallow shell operators that permit chaining/substitution
  const forbidden = /[;&|`$<>\n\r]|\$\(|\)\s*\|\|/;
  if (forbidden.test(cmd)) return { ok: false, reason: 'forbidden-operators' };

  // Disallow quotes/newlines and other characters commonly used for
  // command/substitution/redirect attacks, then accept tokens that do
  // not contain those forbidden characters (flags like `-la` allowed).
  const forbiddenChars = /['"`\n\r;&|<>$]/;
  if (forbiddenChars.test(cmd)) return { ok: false, reason: 'forbidden-chars' };
  const tokens = cmd.trim().split(/\s+/);
  if (tokens.some((t) => t.length === 0 || t.length > 300)) return { ok: false, reason: 'bad-token' };

  const verb = tokens[0];
  if ((verb === 'npm' || verb === 'pnpm') && tokens[1] === 'run') {
    const allowedScripts = new Set(['dev', 'build', 'test', 'start', 'preview', 'electron:dev']);
    const script = tokens[2]?.replace(/^['"]|['"]$/g, '');
    if (!script || !allowedScripts.has(script)) return { ok: false, reason: 'disallowed-script' };
  }

  return { ok: true, argv: tokens };
}

interface E2BRequest {
  action: 'create' | 'files.write' | 'files.read' | 'files.list' | 'commands.run' | 'destroy';
  sandboxId?: string;
  path?: string;
  content?: string;
  command?: string;
  cwd?: string;
  template?: string;
  background?: boolean; // For long-running commands like npm run dev
}

// GET: Health check or sandbox status
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const url = new URL(request.url);
  const sandboxId = url.searchParams.get('sandboxId');

  if (sandboxId) {
    const exists = activeSandboxes.has(sandboxId);
    return json({ exists, sandboxId });
  }

  return json({
    status: 'healthy',
    activeSandboxes: activeSandboxes.size,
  });
};

// POST: Execute E2B operations
export const action = async ({ request }: ActionFunctionArgs) => {
  try {
    const body: E2BRequest = await request.json();
    const { action, sandboxId, path, content, command, cwd, template } = body;

    console.log('[E2B API] Action:', action, 'SandboxId:', sandboxId);

    const apiKey = process.env.VITE_E2B_API_KEY || process.env.E2B_API_KEY;
    if (!apiKey) {
      return json({ error: 'E2B API key not configured' }, { status: 500 });
    }

    switch (action) {
      case 'create': {
        // Create a new sandbox
        const sandbox = await Sandbox.create(template || 'base', {
          apiKey,
          timeoutMs: 5 * 60 * 1000, // 5 minutes
        });

        const newSandboxId = sandbox.sandboxId;
        activeSandboxes.set(newSandboxId, sandbox);

        // Create workdir
        await sandbox.commands.run('mkdir -p /home/user/project');

        console.log('[E2B API] Sandbox created:', newSandboxId);

        return json({
          success: true,
          sandboxId: newSandboxId,
        });
      }

      case 'files.write': {
        if (!sandboxId || !path || content === undefined) {
          return json({ error: 'Missing sandboxId, path, or content' }, { status: 400 });
        }

        const sandbox = activeSandboxes.get(sandboxId);
        if (!sandbox) {
          return json({ error: 'Sandbox not found' }, { status: 404 });
        }

        // Normalize the path
        const resolvedPath = resolvePath(path);
        console.log('[E2B API] files.write - Original:', path, '→ Resolved:', resolvedPath);

        // Ensure directory exists
        const dir = resolvedPath.substring(0, resolvedPath.lastIndexOf('/'));
        if (dir) {
          await sandbox.commands.run(`mkdir -p "${dir}"`);
        }

        // Write file
        await sandbox.files.write(resolvedPath, content);

        console.log('[E2B API] File written:', resolvedPath);

        return json({ success: true, path: resolvedPath });
      }

      case 'files.read': {
        if (!sandboxId || !path) {
          return json({ error: 'Missing sandboxId or path' }, { status: 400 });
        }

        const sandbox = activeSandboxes.get(sandboxId);
        if (!sandbox) {
          return json({ error: 'Sandbox not found' }, { status: 404 });
        }

        const resolvedPath = resolvePath(path);
        const fileContent = await sandbox.files.read(resolvedPath);

        return json({ success: true, content: fileContent });
      }

      case 'files.list': {
        if (!sandboxId || !path) {
          return json({ error: 'Missing sandboxId or path' }, { status: 400 });
        }

        const sandbox = activeSandboxes.get(sandboxId);
        if (!sandbox) {
          return json({ error: 'Sandbox not found' }, { status: 404 });
        }

        const resolvedPath = resolvePath(path);
        const files = await sandbox.files.list(resolvedPath);

        return json({ success: true, files });
      }

      case 'commands.run': {
        if (!sandboxId || !command) {
          return json({ error: 'Missing sandboxId or command' }, { status: 400 });
        }

        const sandbox = activeSandboxes.get(sandboxId);
        if (!sandbox) {
          return json({ error: 'Sandbox not found' }, { status: 404 });
        }

        const resolvedCwd = resolvePath(cwd || '/home/user/project');

        // --- Security: validate command to prevent shell/command injection ---
        // Reject any command containing shell metacharacters and enforce a
        // conservative token whitelist. For npm/pnpm scripts only allow known scripts.
        function __nested_isSafeCommand_removed_for_tests(cmd: string) {
          if (!cmd || typeof cmd !== 'string') return { ok: false, reason: 'invalid' };

          // Disallow common shell operators that allow command chaining / substitution
          const forbidden = /[;&|`$<>\n\r]|\$\(|\)\s*\|\|/;
          if (forbidden.test(cmd)) return { ok: false, reason: 'forbidden-operators' };

          // Allow only tokens composed of safe characters (no quotes, no redirects, no subshells)
          const tokenRe = /^[\w@.\/-:=+%]+$/i;
          const tokens = cmd.trim().split(/\s+/);
          if (!tokens.every((t) => tokenRe.test(t))) return { ok: false, reason: 'invalid-token' };

          const verb = tokens[0];
          // If running npm/pnpm scripts, only allow a short whitelist of script names
          if ((verb === 'npm' || verb === 'pnpm') && tokens[1] === 'run') {
            const allowedScripts = new Set([
              'dev',
              'build',
              'test',
              'start',
              'preview',
              'electron:dev',
            ]);
            const script = tokens[2]?.replace(/^['"]|['"]$/g, '');
            if (!script || !allowedScripts.has(script)) return { ok: false, reason: 'disallowed-script' };
          }

          return { ok: true, argv: tokens };
        }

        const safety = isSafeCommand(command);
        if (!safety.ok) {
          console.warn('[E2B API] Blocked unsafe command:', command, 'reason=', safety.reason);
          return json({ error: `Unsafe command: ${safety.reason}` }, { status: 400 });
        }

        // Check if this should run in background (for long-running commands like npm run dev)
        if (body.background) {
          console.log('[E2B API] Starting background command:', command, 'in', resolvedCwd);

          // Start command in background (don't await)
          sandbox.commands.start(command, {
            cwd: resolvedCwd,
            onStdout: (data) => console.log('[E2B Background]', data),
            onStderr: (data) => console.error('[E2B Background Error]', data),
          }).then((process) => {
            console.log('[E2B API] Background process started, PID:', process.pid);
          }).catch((error) => {
            console.error('[E2B API] Background process failed:', error);
          });

          return json({ success: true, background: true, message: 'Command started in background' });
        }

        // Synchronous command (validated above)
        const result = await sandbox.commands.run(command, { cwd: resolvedCwd });

        console.log('[E2B API] Command executed:', command, 'in', resolvedCwd, 'Exit code:', result.exitCode);

        return json({ success: true, stdout: result.stdout, stderr: result.stderr, exitCode: result.exitCode });
      }

      case 'destroy': {
        if (!sandboxId) {
          return json({ error: 'Missing sandboxId' }, { status: 400 });
        }

        const sandbox = activeSandboxes.get(sandboxId);
        if (sandbox) {
          await sandbox.kill();
          activeSandboxes.delete(sandboxId);
          console.log('[E2B API] Sandbox destroyed:', sandboxId);
        }

        return json({ success: true });
      }

      default:
        return json({ error: `Unknown action: ${action}` }, { status: 400 });
    }
  } catch (error: any) {
    console.error('[E2B API] Error details:', {
      message: error.message,
      stack: error.stack,
      name: error.name,
    });
    return json(
      { error: error.message || 'Internal server error', details: error.stack?.split('\n')[0] },
      { status: 500 }
    );
  }
};
