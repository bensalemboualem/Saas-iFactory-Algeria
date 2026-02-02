import { type LoaderFunctionArgs, json } from '@remix-run/cloudflare';
import { activeSandboxes } from './api.e2b';

function contentTypeFor(path: string) {
    if (path.endsWith('.html') || path === '/' || path === '') return 'text/html; charset=utf-8';
    if (path.endsWith('.js')) return 'application/javascript; charset=utf-8';
    if (path.endsWith('.css')) return 'text/css; charset=utf-8';
    if (path.endsWith('.json')) return 'application/json; charset=utf-8';
    if (path.endsWith('.png')) return 'image/png';
    if (path.endsWith('.jpg') || path.endsWith('.jpeg')) return 'image/jpeg';
    return 'application/octet-stream';
}

export const loader = async ({ request, params }: LoaderFunctionArgs) => {
    const sandboxId = params.sandboxId;
    if (!sandboxId) return json({ error: 'missing sandboxId' }, { status: 400 });

    const sandbox = activeSandboxes.get(sandboxId);
    if (!sandbox) return json({ error: 'sandbox-not-found' }, { status: 404 });

    const url = new URL(request.url);
    // strip leading /_e2b/:sandboxId
    const prefix = `/\_e2b/${sandboxId}`;
    let rel = url.pathname.replace(prefix, '');
    if (!rel || rel === '/') rel = '/index.html';

    const resolved = `/home/user/project${rel}`;
    try {
        const content = await sandbox.files.read(resolved);
        const ct = contentTypeFor(rel);
        const headers = { 'content-type': ct };
        // binary content handling is out-of-scope for prototype — return as text
        return new Response(content as string, { status: 200, headers });
    } catch (err: any) {
        return json({ error: 'not-found', detail: err?.message }, { status: 404 });
    }
};
