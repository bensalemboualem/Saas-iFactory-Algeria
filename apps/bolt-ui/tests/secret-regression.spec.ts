import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

// Scans only the apps/bolt-ui tree to keep the test fast and isolated.
const ROOT = path.resolve(__dirname, '..');

function walk(dir: string, cb: (file: string) => void) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'node_modules' || entry.name === '.git') continue;
      walk(full, cb);
    } else if (entry.isFile()) {
      cb(full);
    }
  }
}

function safeMask(s: string) {
  if (s.length <= 8) return '********';
  return s.slice(0, 4) + '…' + s.slice(-4);
}

const PATTERNS: { name: string; re: RegExp }[] = [
  { name: 'E2B API key', re: /e2b_[0-9a-f]{8,}/i },
  { name: 'OpenAI-style secret (sk-)', re: /sk-[A-Za-z0-9_\.-]{16,}/ },
  { name: 'IAFactory API key (test)', re: /iaf_test_key_[0-9A-Za-z_\-]{3,}/i },
  { name: 'Common env var', re: /\bOPENAI_API_KEY\b|\bIAFACTORY_API_KEY\b/ },
  { name: 'Google API key', re: /AIza[0-9A-Za-z\-_]{35}/ },
];

describe('bolt-ui: repository secret-regression (fast, scoped)', () => {
  it('fails when known secret patterns are present in tracked files under apps/bolt-ui', () => {
    const matches: Record<string, Array<{ file: string; snippet: string }>> = {};

    walk(ROOT, (file) => {
      // only scan textual files and bundles (client/server build outputs are included intentionally)
      const ext = path.extname(file).toLowerCase();
      if (['.png', '.jpg', '.jpeg', '.gif', '.webp', '.zip', '.tar', '.gz'].includes(ext)) return;
      let txt: string;
      try {
        txt = fs.readFileSync(file, 'utf8');
      } catch (err) {
        return;
      }

      for (const p of PATTERNS) {
        const m = p.re.exec(txt);
        if (m) {
          matches[p.name] = matches[p.name] || [];
          matches[p.name].push({ file: path.relative(ROOT, file), snippet: safeMask(m[0]) });
        }
      }
    });

    if (Object.keys(matches).length > 0) {
      // build a useful error message but avoid printing full secret values
      const lines: string[] = [];
      for (const k of Object.keys(matches)) {
        lines.push(`- ${k}:`);
        for (const m of matches[k]) lines.push(`    • ${m.file}: ${m.snippet}`);
      }
      const msg = [
        'Secret-regression: one or more secret patterns were found in `apps/bolt-ui`.',
        'This test catches committed API keys and build artifacts that contain secrets.',
        '',
        'Matches (values masked):',
        ...lines,
        '',
        'If these are legitimate non-secret strings, update the test PATTERNS to allow them.',
        'If these are real secrets: rotate the keys, remove the files from git, and purge history.',
      ].join('\n');

      // show a concise failure message for CI / local dev
      throw new Error(msg);
    }

    expect(Object.keys(matches).length).toBe(0);
  });
});
