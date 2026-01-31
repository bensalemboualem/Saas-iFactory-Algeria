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
const activeSandboxes = new Map<string, Sandbox>();

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

          return json({
            success: true,
            background: true,
            message: 'Command started in background',
          });
        }

        // Synchronous command (default)
        const result = await sandbox.commands.run(command, {
          cwd: resolvedCwd,
        });

        console.log('[E2B API] Command executed:', command, 'in', resolvedCwd, 'Exit code:', result.exitCode);

        return json({
          success: true,
          stdout: result.stdout,
          stderr: result.stderr,
          exitCode: result.exitCode,
        });
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
