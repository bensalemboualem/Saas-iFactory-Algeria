import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ensurePreviewServer } from '../app/lib/.server/preview-manager';
import { activeSandboxes } from '../app/routes/api.e2b';

describe('Preview manager — E2B prototype flow', () => {
    beforeEach(() => {
        activeSandboxes.clear();
        delete process.env.VITE_E2B_API_KEY;
        delete process.env.E2B_API_KEY;
    });

    it('reuses an existing sandbox when sandboxId is provided', async () => {
        const fakeSandbox: any = {
            commands: { start: vi.fn() },
            files: { read: vi.fn().mockResolvedValue('<html>ok</html>') },
        } as const;

        activeSandboxes.set('fake-sb', fakeSandbox as any);

        const req = new Request('https://preview.test/_?provider=e2b&sandboxId=fake-sb');
        const status = await ensurePreviewServer(req as any);

        expect(status.running).toBe(true);
        expect(status.url).toContain('/_e2b/fake-sb');
    });

    it('returns error when no E2B API key and no existing sandbox', async () => {
        const req = new Request('https://preview.test/_?provider=e2b');
        const status = await ensurePreviewServer(req as any);

        expect(status.running).toBe(false);
        expect(status.message).toMatch(/E2B API key/i);
    });
});
