# 🎨 Guide Génération Icônes PWA

## Icônes Créées

✅ `icon-192.svg` - Source vectorielle 192x192
✅ `icon-512.svg` - Source vectorielle 512x512

## Conversion SVG → PNG

### Méthode 1: ImageMagick (Recommandé)
```bash
# Installer ImageMagick
# Windows: choco install imagemagick
# Linux: sudo apt install imagemagick
# Mac: brew install imagemagick

# Convertir les icônes
convert icon-192.svg -resize 192x192 icon-192x192.png
convert icon-512.svg -resize 512x512 icon-512x512.png
convert icon-192.svg -resize 180x180 apple-touch-icon.png
```

### Méthode 2: En ligne (Rapide)
1. Aller sur https://cloudconvert.com/svg-to-png
2. Upload `icon-192.svg` → Convert → Download `icon-192x192.png`
3. Upload `icon-512.svg` → Convert → Download `icon-512x512.png`
4. Upload `icon-192.svg` → Resize 180x180 → Download `apple-touch-icon.png`

### Méthode 3: Inkscape (GUI)
```bash
# Ouvrir icon-192.svg dans Inkscape
# File → Export PNG Image
# Width: 192, Height: 192
# Export As: icon-192x192.png
```

### Méthode 4: Node.js (Automatique)
```bash
# Installer sharp
npm install --save-dev sharp

# Créer convert-icons.js:
cat > convert-icons.js << 'EOF'
const sharp = require('sharp');

async function convertIcons() {
  await sharp('icon-192.svg')
    .resize(192, 192)
    .png()
    .toFile('icon-192x192.png');

  await sharp('icon-512.svg')
    .resize(512, 512)
    .png()
    .toFile('icon-512x512.png');

  await sharp('icon-192.svg')
    .resize(180, 180)
    .png()
    .toFile('apple-touch-icon.png');

  console.log('✅ Icons converted!');
}

convertIcons();
EOF

# Exécuter
node convert-icons.js
```

## Icônes Requises

- ✅ `icon-192x192.png` - Android (192x192)
- ✅ `icon-512x512.png` - Android (512x512)
- ✅ `apple-touch-icon.png` - iOS (180x180)
- [ ] `favicon.ico` - Browser tab (optionnel)

## Vérification

Après conversion, vérifier:
```bash
ls -lh icon-*.png apple-touch-icon.png
```

Devrait afficher:
```
icon-192x192.png      (~15-25 KB)
icon-512x512.png      (~40-60 KB)
apple-touch-icon.png  (~12-20 KB)
```

## Design Icônes

**Thème**: CAN 2025 Algérie
- 🏆 Trophée doré (champion)
- 🟢 Fond vert dégradé (couleur Algérie)
- ⭐ Étoile rouge (drapeau DZ)
- ⚽ Texte "CAN 2025"

**Responsive**: Les icônes sont vectorielles et peuvent être exportées à n'importe quelle taille sans perte de qualité.

## Manifest.json

Les icônes sont déjà référencées dans `manifest.json`:
```json
{
  "icons": [
    {
      "src": "/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

Après conversion PNG, l'app PWA sera complète! 🚀
