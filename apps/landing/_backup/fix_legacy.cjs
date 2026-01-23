const fs = require('fs');

// Lire le fichier HTML de la landing qui fonctionne
const html = fs.readFileSync('D:/IAFactory/frontend/landing/index.html', 'utf8');

// Extraire le body
const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
if (!bodyMatch) {
  console.log('No body found');
  process.exit(1);
}
let body = bodyMatch[1];

// Retirer les scripts du body
body = body.replace(/<script[\s\S]*?<\/script>/gi, '');

// Extraire les scripts
const scripts = [];
const scriptRegex = /<script([^>]*)>([\s\S]*?)<\/script>/gi;
let match;
while ((match = scriptRegex.exec(html)) !== null) {
  const attrs = match[1];
  const content = match[2].trim();
  if (content) {
    scripts.push({ inline: content });
  } else if (attrs.includes('src=')) {
    const srcMatch = attrs.match(/src=["']([^"']+)["']/);
    if (srcMatch) {
      scripts.push({ src: srcMatch[1] });
    }
  }
}

// Créer le fichier TypeScript
const tsContent = `export const legacyBody = ${JSON.stringify(body)};

export const legacyScripts: Array<{ inline?: string; src?: string }> = ${JSON.stringify(scripts, null, 2)};
`;

fs.writeFileSync('D:/iafactorychatgpt/landing-bolt-style/src/legacy.ts', tsContent);
console.log('Done! Created legacy.ts');
console.log('Body length:', body.length);
console.log('Scripts:', scripts.length);
