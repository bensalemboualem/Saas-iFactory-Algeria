import { beforeEach, describe, expect, it, vi } from 'vitest';

import { loader as e2bLoader } from '../app/routes/_e2b.$sandboxId';
import { activeSandboxes } from '../app/routes/api.e2b';

describe('E2B proxy route (loader)', () => {
    beforeEach(() => {
        activeSandboxes.clear();
    });

    it('serves index.html from the sandbox filesystem', async () => {
        const fakeSandbox: any = {
            files: {
                read: vi.fn().mockImplementation(async (p: string) => {
                    if (p === '/home/user/project/index.html') return '<html><body>ok</body></html>';
                    throw new Error('not found');
                }),
            },
        };

        activeSandboxes.set('proxy-sb', fakeSandbox as any);

        const req = new Request('https://example.test/_e2b/proxy-sb/');
        const res: any = await e2bLoader({ request: req, params: { sandboxId: 'proxy-sb' } } as any);
        const text = await res.text();

        expect(text).toContain('ok');
        expect(fakeSandbox.files.read).toHaveBeenCalledWith('/home/user/project/index.html');
    });
});
