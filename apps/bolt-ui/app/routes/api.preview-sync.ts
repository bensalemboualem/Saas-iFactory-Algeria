import { json, type ActionFunctionArgs } from '@remix-run/cloudflare';
import { withSecurity } from '~/lib/security';
import path from 'node:path';
import { promises as fs } from 'node:fs';

interface SyncFile {
  path: string;
  content: string;
}

interface SyncPayload {
  files: SyncFile[];
}

function getProjectRoot(): string | null {
  return process.env.PREVIEW_PROJECT_ROOT || null;
}

function resolveSafePath(root: string, relativePath: string): string | null {
  const resolved = path.resolve(root, relativePath.replace(/^[\\/]+/, ''));
  const normalizedRoot = path.resolve(root);

  if (!resolved.startsWith(normalizedRoot)) {
    return null;
  }

  return resolved;
}

async function ensureDir(dirPath: string) {
  await fs.mkdir(dirPath, { recursive: true });
}

async function previewSyncAction({ request }: ActionFunctionArgs) {
  const projectRoot = getProjectRoot();

  if (!projectRoot) {
    return json({ ok: false, message: 'PREVIEW_PROJECT_ROOT is not set.' }, { status: 400 });
  }

  const payload = (await request.json()) as SyncPayload;
  const files = payload?.files ?? [];

  await ensureDir(projectRoot);

  for (const file of files) {
    if (!file?.path) {
      continue;
    }

    const safePath = resolveSafePath(projectRoot, file.path);

    if (!safePath) {
      continue;
    }

    await ensureDir(path.dirname(safePath));
    await fs.writeFile(safePath, file.content ?? '', 'utf-8');
  }

  return json({ ok: true, files: files.length });
}

export const action = withSecurity(previewSyncAction, { allowedMethods: ['POST'] });
