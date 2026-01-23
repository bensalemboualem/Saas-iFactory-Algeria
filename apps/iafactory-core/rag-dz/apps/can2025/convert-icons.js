/**
 * Script de conversion automatique SVG → PNG
 * CAN 2025 PWA Icons
 */

const fs = require('fs');
const { execSync } = require('child_process');

console.log('🎨 CAN 2025 - Conversion Icônes PWA\n');

// Vérifier si ImageMagick est disponible
let hasImageMagick = false;
try {
  execSync('convert -version', { stdio: 'ignore' });
  hasImageMagick = true;
  console.log('✅ ImageMagick détecté');
} catch (e) {
  console.log('⚠️  ImageMagick non trouvé');
}

// Vérifier si sharp est disponible
let hasSharp = false;
try {
  require.resolve('sharp');
  hasSharp = true;
  console.log('✅ Sharp (Node.js) détecté');
} catch (e) {
  console.log('⚠️  Sharp non installé');
}

console.log('');

// Méthode 1: ImageMagick
if (hasImageMagick) {
  console.log('🔄 Conversion avec ImageMagick...\n');

  try {
    process.chdir('public');

    console.log('→ Conversion icon-192.svg...');
    execSync('convert icon-192.svg -resize 192x192 icon-192x192.png');
    console.log('  ✅ icon-192x192.png créé');

    console.log('→ Conversion icon-512.svg...');
    execSync('convert icon-512.svg -resize 512x512 icon-512x512.png');
    console.log('  ✅ icon-512x512.png créé');

    console.log('→ Conversion apple-touch-icon...');
    execSync('convert icon-192.svg -resize 180x180 apple-touch-icon.png');
    console.log('  ✅ apple-touch-icon.png créé');

    process.chdir('..');

    console.log('\n✅ SUCCÈS! Toutes les icônes ont été converties.\n');

    // Vérifier les fichiers
    const files = ['icon-192x192.png', 'icon-512x512.png', 'apple-touch-icon.png'];
    console.log('📊 Tailles fichiers:');
    files.forEach(file => {
      const path = `public/${file}`;
      if (fs.existsSync(path)) {
        const stats = fs.statSync(path);
        const sizeKB = (stats.size / 1024).toFixed(1);
        console.log(`  ${file}: ${sizeKB} KB`);
      }
    });

    console.log('\n🚀 PWA icons prêtes pour déploiement!');
    process.exit(0);

  } catch (error) {
    console.error('❌ Erreur lors de la conversion:', error.message);
    process.exit(1);
  }
}

// Méthode 2: Sharp (fallback)
else if (hasSharp) {
  console.log('🔄 Conversion avec Sharp...\n');

  const sharp = require('sharp');

  (async () => {
    try {
      console.log('→ Conversion icon-192.svg...');
      await sharp('public/icon-192.svg')
        .resize(192, 192)
        .png()
        .toFile('public/icon-192x192.png');
      console.log('  ✅ icon-192x192.png créé');

      console.log('→ Conversion icon-512.svg...');
      await sharp('public/icon-512.svg')
        .resize(512, 512)
        .png()
        .toFile('public/icon-512x512.png');
      console.log('  ✅ icon-512x512.png créé');

      console.log('→ Conversion apple-touch-icon...');
      await sharp('public/icon-192.svg')
        .resize(180, 180)
        .png()
        .toFile('public/apple-touch-icon.png');
      console.log('  ✅ apple-touch-icon.png créé');

      console.log('\n✅ SUCCÈS! Toutes les icônes ont été converties.\n');

      // Vérifier les fichiers
      const files = ['icon-192x192.png', 'icon-512x512.png', 'apple-touch-icon.png'];
      console.log('📊 Tailles fichiers:');
      files.forEach(file => {
        const path = `public/${file}`;
        if (fs.existsSync(path)) {
          const stats = fs.statSync(path);
          const sizeKB = (stats.size / 1024).toFixed(1);
          console.log(`  ${file}: ${sizeKB} KB`);
        }
      });

      console.log('\n🚀 PWA icons prêtes pour déploiement!');

    } catch (error) {
      console.error('❌ Erreur lors de la conversion:', error.message);
      process.exit(1);
    }
  })();
}

// Aucune méthode disponible
else {
  console.log('❌ Aucun outil de conversion trouvé!\n');
  console.log('📋 Solutions:\n');
  console.log('1. Installer ImageMagick:');
  console.log('   Windows: choco install imagemagick');
  console.log('   Linux:   sudo apt install imagemagick');
  console.log('   Mac:     brew install imagemagick\n');
  console.log('2. OU installer Sharp (Node.js):');
  console.log('   npm install --save-dev sharp\n');
  console.log('3. OU convertir en ligne:');
  console.log('   https://cloudconvert.com/svg-to-png\n');
  console.log('Voir: public/GENERATE_ICONS.md pour plus de détails');
  process.exit(1);
}
