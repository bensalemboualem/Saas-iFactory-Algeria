const fs = require('fs');

// Read HTML source
const html = fs.readFileSync('./index.legacy.html', 'utf8');

// Extract body content
const bodyStart = html.indexOf('<!-- Header -->');
const bodyEnd = html.lastIndexOf('</script>') + '</script>'.length;
let bodyContent = html.substring(bodyStart, bodyEnd);

// Escape for JS string literal
function escapeForJsString(str) {
  return str
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '')
    .replace(/\t/g, '\\t');
}

const escapedBody = escapeForJsString(bodyContent);

// Extract scripts if any
const scriptMatches = [];
const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
let match;
while ((match = scriptRegex.exec(bodyContent)) !== null) {
  if (match[1].trim()) {
    scriptMatches.push({ inline: escapeForJsString(match[1]) });
  }
}

// Build legacy.ts content
const legacyTs = `export const legacyBody = "${escapedBody}";

export const legacyScripts: Array<{ inline?: string; src?: string }> = ${JSON.stringify(scriptMatches, null, 2)};
`;

fs.writeFileSync('./src/legacy.ts', legacyTs);
console.log('legacy.ts regenerated successfully');
