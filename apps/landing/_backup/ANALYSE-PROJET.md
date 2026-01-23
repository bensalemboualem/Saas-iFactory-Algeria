# ANALYSE-PROJET (landing-bolt-style)

## 1) Structure (depth 3, excluding node_modules/.git/dist)

```
assets
shared
src
agents-admin.html
apps-admin.html
index.html
index.legacy.html
package-lock.json
package.json
tsconfig.json
vite.config.ts
assets\images
assets\images\dziria.png
assets\images\lala-fatma.png
assets\images\logo-dark.png
assets\images\logo-full-dark.png
assets\images\logo-full-light.png
assets\images\logo-iafactory-full.svg
assets\images\logo-iafactory-new.png
assets\images\logo-light.png
assets\images\logocalire.png
assets\images\logodark.png
assets\images\logoh.png
assets\images\logohc-transparent.png
assets\images\logohc.png
assets\images\logoiafactalg.png
assets\images\logoiafactoryalgeria-dark.png
assets\images\logoiafactoryalgeria-light-v2.png
assets\images\logoiafactoryalgeria-light.png
assets\images\logoiafactoryalgeria.png
assets\images\LOGOSORA.png
shared\footer-inject.js
shared\footer.html
shared\header.html
shared\i18n.js
shared\iafactory-design-system.css
shared\iafactory-theme.css
shared\iafactory-unified.css
shared\language-switcher.js
src\App.tsx
src\legacy.css
src\legacy.ts
src\main.tsx
src\styles.css
```

## 2) Dependencies (package.json)

Dependencies:
- react ^19.0.0
- react-dom ^19.0.0

DevDependencies:
- @types/react ^19.0.0
- @types/react-dom ^19.0.0
- @vitejs/plugin-react ^4.3.1
- typescript ^5.6.3
- vite ^5.4.8

## 3) Imports externes (risques hors projet)

### A) References to ../iafactory or ../../iafactory
Found references to external project paths in:
- shared/footer.html (links to ../iafactory-landing/...)
  Examples:
  - ../iafactory-landing/apps.html
  - ../iafactory-landing/docs/directory/agents.html
  - ../iafactory-landing/docs/directory/workflows.html
  - ../iafactory-landing/docs/api-setup.html
  - ../iafactory-landing/docs/rag-assistants.html
  - ../iafactory-landing/docs/developer-tools.html
  - ../iafactory-landing/docs/documentation.html
  - ../iafactory-landing/docs/getstarted.html
  - ../iafactory-landing/docs/blog.html
  - ../iafactory-landing/docs/contact.html
  - ../iafactory-landing/docs/a-propos.html
  - ../iafactory-landing/docs/tarifs.html
  - ../iafactory-landing/docs/newsletter.html
  - ../iafactory-landing/docs/mentions.html
  - ../iafactory-landing/docs/confidentialite.html
  - ../iafactory-landing/docs/conditions.html

### B) Absolute paths to other projects
- No Windows absolute paths (e.g., D:\...) found in source files.

### C) Aliases pointing outside the project
- tsconfig.json has no "paths" or aliases configured.

### D) External JS/TS imports
- vite.config.ts imports: vite, @vitejs/plugin-react
- src/App.tsx imports: react, ./legacy, ./legacy.css
- src/main.tsx imports: react, react-dom/client, ./App, ./styles.css

## 4) Config files
- vite.config.ts
- tsconfig.json
- package.json
- package-lock.json
- No .env* files found

## 5) Pages / routes
- No Next.js pages/ or app/ directories.
- Static HTML pages present:
  - index.legacy.html (legacy static landing)
  - apps-admin.html
  - agents-admin.html
- React entry uses index.html with Vite mount.
