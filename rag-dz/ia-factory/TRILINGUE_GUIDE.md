# Guide Trilingue IA Factory / Trilingual Guide / الدليل ثلاثي اللغات

## 📚 Documentation Créée / Documentation Created / الوثائق المنشأة

### READMEs

| Langue | Fichier | Statut |
|--------|---------|--------|
| 🇫🇷 Français | `README.md` | ✅ Original |
| 🇬🇧 English | `README_EN.md` | ✅ Created |
| 🇩🇿 العربية | `README_AR.md` | ✅ Created (RTL) |

### Documentation API

| Langue | Fichier | Statut |
|--------|---------|--------|
| 🇫🇷 Français | `docs/API_FR.md` | ✅ Created |
| 🇬🇧 English | `docs/API_EN.md` | ✅ Created |
| 🇩🇿 العربية | `docs/API_AR.md` | ✅ Created (RTL) |

### Frontend Landing Pages

| Langue | Fichier | Statut |
|--------|---------|--------|
| 🇫🇷 Français | `frontend/src/index.html` | ✅ Created |
| 🇬🇧 English | `frontend/src/index_en.html` | ✅ Created |
| 🇩🇿 العربية | `frontend/src/index_ar.html` | ✅ Created (RTL) |

---

## 🌐 Structure des Fichiers / File Structure / هيكل الملفات

```
ia-factory/
├── README.md                      # 🇫🇷 Documentation principale
├── README_EN.md                   # 🇬🇧 Main documentation
├── README_AR.md                   # 🇩🇿 الوثائق الرئيسية
├── TRILINGUE_GUIDE.md             # Ce fichier / This file / هذا الملف
├── docs/
│   ├── API_FR.md                  # 🇫🇷 Documentation API
│   ├── API_EN.md                  # 🇬🇧 API Documentation  
│   └── API_AR.md                  # 🇩🇿 توثيق API
├── frontend/
│   └── src/
│       ├── index.html             # 🇫🇷 Landing page française
│       ├── index_en.html          # 🇬🇧 English landing page
│       └── index_ar.html          # 🇩🇿 صفحة الهبوط العربية
└── backend/
    └── app/
        └── ...                    # Code source (non traduit)
```

---

## 🔗 URLs de Production / Production URLs / روابط الإنتاج

### API
- **Base**: `https://www.iafactoryalgeria.com/ia-factory/`
- **Health**: `https://www.iafactoryalgeria.com/ia-factory/health`
- **Docs (Swagger)**: `https://www.iafactoryalgeria.com/ia-factory/docs`

### Frontend (à déployer / to deploy / للنشر)
- **FR**: `https://www.iafactoryalgeria.com/ia-factory/fr/`
- **EN**: `https://www.iafactoryalgeria.com/ia-factory/en/`
- **AR**: `https://www.iafactoryalgeria.com/ia-factory/ar/`

---

## 🔄 Language Switcher / Sélecteur de Langue / محول اللغة

Les pages frontend incluent un sélecteur de langue en haut à droite (ou à gauche pour RTL) permettant de basculer entre les trois versions.

The frontend pages include a language switcher in the top right (or left for RTL) corner allowing users to switch between the three versions.

تتضمن صفحات الواجهة الأمامية محول لغة في أعلى اليمين (أو اليسار للـ RTL) يسمح للمستخدمين بالتبديل بين الإصدارات الثلاثة.

---

## 📝 Notes Techniques / Technical Notes / ملاحظات تقنية

### Support RTL (Arabe / Arabic / العربية)

Les fichiers arabes utilisent:
- `dir="rtl"` sur l'élément `<html>`
- `lang="ar"`
- Police Cairo de Google Fonts
- `space-x-reverse` pour Tailwind CSS
- Code blocks restent en LTR pour lisibilité

### Polices / Fonts / الخطوط

- **FR/EN**: Inter (Google Fonts)
- **AR**: Cairo (Google Fonts)

### Framework CSS

Toutes les pages utilisent Tailwind CSS 2.2.19 via CDN.

---

## 🚀 Déploiement Frontend / Frontend Deployment / نشر الواجهة الأمامية

Pour déployer les pages frontend sur le VPS:

```bash
# 1. Copier les fichiers
scp -r frontend/src/* root@46.224.3.125:/var/www/ia-factory-frontend/

# 2. Configurer Nginx (ajouter au bloc existant)
# location /ia-factory/fr/ {
#     alias /var/www/ia-factory-frontend/;
#     index index.html;
# }
# location /ia-factory/en/ {
#     alias /var/www/ia-factory-frontend/;
#     index index_en.html;
# }
# location /ia-factory/ar/ {
#     alias /var/www/ia-factory-frontend/;
#     index index_ar.html;
# }

# 3. Recharger Nginx
nginx -s reload
```

---

## ✅ Checklist de Validation / Validation Checklist / قائمة التحقق

### Documentation
- [x] README français complet
- [x] README anglais complet
- [x] README arabe complet (RTL)
- [x] API doc française complète
- [x] API doc anglaise complète
- [x] API doc arabe complète (RTL)

### Frontend
- [x] Landing page française
- [x] Landing page anglaise
- [x] Landing page arabe (RTL)
- [x] Language switcher fonctionnel
- [x] Responsive design (mobile/desktop)

### Code Examples
- [x] Python examples dans API docs
- [x] JavaScript examples dans API docs
- [x] cURL examples dans API docs

---

## 📞 Support

- **Email**: support@iafactory.dz
- **Location**: Alger, Algérie / Algiers, Algeria / الجزائر العاصمة، الجزائر

---

*Document créé le 12 Janvier 2025 / Created January 12, 2025 / تم الإنشاء في 12 يناير 2025*
