import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const LANDING_ROOT = path.resolve(SCRIPT_DIR, '..');
const SRC_ROOT = path.join(LANDING_ROOT, 'src');
const STRICT = process.env.STRICT === '1';

const SCAN_DIRS = ['components', 'pages', 'app'];
if (STRICT) SCAN_DIRS.push('data');

const IGNORE_DIRS = new Set([
  'node_modules',
  'dist',
  'build',
  '.next',
  'coverage',
  '.turbo',
  '.git',
  'stories',
]);

const IGNORE_PATHS = [
  `${path.sep}i18n${path.sep}`,
  `${path.sep}data${path.sep}`,
];

const BANNED_PHRASES = [
  'Pricing',
  'Tools',
  'Search a solution',
  'Concrete use cases',
  "write a poem for my mother's birthday",
  'All rights reserved',
];

const BANNED_UI_WORDS = ['Pricing', 'Tools', 'Try', 'View', 'Filter', 'Clear'];

const IGNORE_LINE_RE = [
  /^\s*import\b/,
  /^\s*export\b/,
  /t\(\s*["'`]/,
  /\/[a-z-]+/,
];

const UI_ATTR_RE = /\b(label|placeholder|title|aria-label)\s*=\s*["'`](.*?)["'`]/g;
const JSX_TEXT_RE = />([^<]+)</g;

async function exists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

function shouldIgnorePath(filePath) {
  if (filePath.endsWith('.d.ts') || filePath.endsWith('.map')) return true;
  if (/\.(test|spec)\./.test(filePath)) return true;
  if (filePath.includes(`${path.sep}stories${path.sep}`)) return true;
  if (!STRICT) {
    return IGNORE_PATHS.some((p) => filePath.includes(p));
  }
  return filePath.includes(`${path.sep}i18n${path.sep}`);
}

async function collectFiles(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (IGNORE_DIRS.has(entry.name)) continue;
      files.push(...(await collectFiles(fullPath)));
      continue;
    }
    if (shouldIgnorePath(fullPath)) continue;
    files.push(fullPath);
  }
  return files;
}

function hasIgnoredLine(line) {
  return IGNORE_LINE_RE.some((re) => re.test(line));
}

function matchBanned(text) {
  const hits = [];
  for (const phrase of BANNED_PHRASES) {
    const re = new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
    if (re.test(text)) hits.push(phrase);
  }
  for (const word of BANNED_UI_WORDS) {
    const re = new RegExp(`\\b${word}\\b`, 'i');
    if (re.test(text)) hits.push(word);
  }
  return hits;
}

function scanLine(line) {
  const hits = [];
  for (const match of line.matchAll(UI_ATTR_RE)) {
    hits.push(...matchBanned(match[2]));
  }
  for (const match of line.matchAll(JSX_TEXT_RE)) {
    const text = match[1].trim();
    if (text.length === 0) continue;
    hits.push(...matchBanned(text));
  }
  return hits;
}

function scanFile(filePath, content) {
  const lines = content.split(/\r?\n/);
  const hits = [];
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (hasIgnoredLine(line)) continue;
    const lineHits = scanLine(line);
    if (lineHits.length > 0) {
      hits.push({
        filePath,
        line: i + 1,
        text: line,
      });
    }
  }
  return hits;
}

async function main() {
  const scanRoots = [];
  for (const dir of SCAN_DIRS) {
    const fullPath = path.join(SRC_ROOT, dir);
    if (await exists(fullPath)) scanRoots.push(fullPath);
  }
  if (scanRoots.length === 0) {
    console.log('check:no-en OK: no scan roots found.');
    return;
  }

  const allFiles = [];
  for (const root of scanRoots) {
    allFiles.push(...(await collectFiles(root)));
  }

  const allHits = [];
  for (const filePath of allFiles) {
    let content;
    try {
      content = await fs.readFile(filePath, 'utf8');
    } catch {
      continue;
    }
    allHits.push(...scanFile(filePath, content));
  }

  if (allHits.length === 0) {
    console.log('check:no-en OK: no forbidden English strings found.');
    return;
  }

  console.error('check:no-en FAILED: forbidden English strings found.');
  for (const hit of allHits) {
    const rel = path.relative(process.cwd(), hit.filePath);
    console.error(`${rel}:${hit.line}: ${hit.text}`);
  }
  process.exit(1);
}

main().catch((err) => {
  console.error('check:no-en FAILED:', err);
  process.exit(1);
});
