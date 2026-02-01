import { describe, expect, it, beforeEach, vi } from 'vitest';

import { isSafeCommand, activeSandboxes, action } from '../app/routes/api.e2b';

describe('E2B command validation (security)', () => {
    it('rejects commands with shell metacharacters', () => {
        const bad = 'ls; rm -rf /';
        const res = isSafeCommand(bad as any);
        expect(res.ok).toBe(false);
        expect(res.reason).toMatch(/forbidden|invalid/);
    });

    it('rejects token with quotes or subshells', () => {
        expect(isSafeCommand("echo \"hello\"").ok).toBe(false);
        expect(isSafeCommand('$(reboot)').ok).toBe(false);
    });

    it('allows simple safe commands', () => {
        expect(isSafeCommand('ls -la').ok).toBe(true);
        expect(isSafeCommand('node ./script.js').ok).toBe(true);
    });

    it('allows only whitelisted npm scripts', () => {
        expect(isSafeCommand('npm run dev').ok).toBe(true);
        expect(isSafeCommand('pnpm run build').ok).toBe(true);
        expect(isSafeCommand('npm run dangerously-evil').ok).toBe(false);
    });
});

describe('E2B action handler — integration-ish', () => {
    const sandboxId = 'test-sb-1';

    beforeEach(() => {
        activeSandboxes.clear();
    });

    it('returns 400 for unsafe commands (blocked before exec)', async () => {
        // install a fake sandbox that would throw if run() called
        const fakeSandbox: any = {
            commands: {
                run: vi.fn().mockResolvedValue({ stdout: '', stderr: '', exitCode: 0 }),
                start: vi.fn(),
            },
            files: { read: vi.fn(), write: vi.fn(), list: vi.fn() },
        };
        activeSandboxes.set(sandboxId, fakeSandbox);

        process.env.E2B_API_KEY = 'dummy';

        const payload = { action: 'commands.run', sandboxId, command: 'ls; rm -rf /' };
        const req: any = { json: async () => payload, url: 'http://localhost' };

        const res: any = await (action as any)({ request: req });
        const body = await res.json();

        expect(res.status).toBe(400);
        expect(body.error).toMatch(/Unsafe command/);
        expect(fakeSandbox.commands.run).not.toHaveBeenCalled();
    });

    it('executes allowed command via sandbox.commands.run', async () => {
        const fakeSandbox: any = {
            commands: {
                run: vi.fn().mockResolvedValue({ stdout: 'ok', stderr: '', exitCode: 0 }),
                start: vi.fn().mockResolvedValue({ pid: 1234 }),
            },
            files: { read: vi.fn(), write: vi.fn(), list: vi.fn() },
        };
        activeSandboxes.set(sandboxId, fakeSandbox);

        process.env.E2B_API_KEY = 'dummy';

        const payload = { action: 'commands.run', sandboxId, command: 'npm run dev' };
        const req: any = { json: async () => payload, url: 'http://localhost' };

        const res: any = await (action as any)({ request: req });
        const body = await res.json();

        expect(res.status).toBe(200);
        expect(body.success).toBe(true);
        expect(fakeSandbox.commands.run).toHaveBeenCalledWith('npm run dev', expect.any(Object));
    });
});
