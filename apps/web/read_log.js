const fs = require('fs');
const content = fs.readFileSync('build.log', 'utf16le');
console.log('--- ERROR LOG START ---');
const lines = content.split('\n');
const errors = lines.filter(l => l.toLowerCase().includes('error') || l.toLowerCase().includes('conflict') || l.toLowerCase().includes('failed'));
if (errors.length > 0) {
    errors.forEach(e => console.log(e));
} else {
    // If no explicit error keyword, show first 20 lines to see what happened
    console.log(lines.slice(0, 20).join('\n'));
}
console.log('--- ERROR LOG END ---');
