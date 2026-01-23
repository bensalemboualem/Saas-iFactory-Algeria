# وثائق CI/CD Pipeline

**IAFACTORY - وثائق التكامل والنشر المستمر**

*آخر تحديث: 19 يناير 2026*

---

## جدول المحتويات

1. [نظرة عامة](#1-نظرة-عامة)
2. [GitHub Actions](#2-github-actions)
3. [البيئات](#3-البيئات)
4. [خط أنابيب البناء](#4-خط-أنابيب-البناء)
5. [الاختبارات الآلية](#5-الاختبارات-الآلية)
6. [النشر](#6-النشر)
7. [المراقبة](#7-المراقبة)
8. [التراجع](#8-التراجع)

---

## 1. نظرة عامة

### هيكل CI/CD

```
┌─────────────────────────────────────────────────────────────────┐
│                        مستودع GitHub                             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Actions                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Lint &    │  │    بناء    │  │   اختبار   │             │
│  │  TypeCheck  │  │             │  │             │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         └─────────────────┼─────────────────┘                   │
│                           ▼                                      │
│                  ┌─────────────┐                                │
│                  │    نشر     │                                │
│                  └──────┬──────┘                                │
└─────────────────────────┼───────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Vercel  │   │  بيئة    │   │  بيئة   │
    │ معاينة  │   │ التجريب  │   │ الإنتاج │
    └──────────┘   └──────────┘   └──────────┘
```

### الفروع

| الفرع | البيئة | النشر |
|-------|--------|-------|
| `main` | - | لا شيء (محمي) |
| `next` | التجريب | تلقائي |
| `release/*` | الإنتاج | يدوي (موافقة) |
| `feat/*` | معاينة | تلقائي (Vercel) |

---

## 2. GitHub Actions

### 2.1 سير العمل الرئيسية

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [next, main]
  pull_request:
    branches: [next, main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 10

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: تثبيت التبعيات
        run: pnpm install --frozen-lockfile

      - name: فحص الأنواع
        run: pnpm run type-check

      - name: Lint
        run: pnpm run lint

  test:
    name: الاختبارات
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 10

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: تثبيت التبعيات
        run: pnpm install --frozen-lockfile

      - name: تشغيل الاختبارات
        run: pnpm run test:ci

      - name: رفع تغطية الكود
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build:
    name: البناء
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 10

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: تثبيت التبعيات
        run: pnpm install --frozen-lockfile

      - name: البناء
        run: pnpm run build
        env:
          NEXT_PUBLIC_API_URL: ${{ secrets.NEXT_PUBLIC_API_URL }}

      - name: رفع artifact البناء
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: .next
          retention-days: 7
```

### 2.2 سير عمل النشر

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [next]
  workflow_dispatch:
    inputs:
      environment:
        description: 'البيئة للنشر إليها'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

jobs:
  deploy-staging:
    name: النشر إلى التجريب
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/next' || github.event.inputs.environment == 'staging'
    environment:
      name: staging
      url: https://staging.iafactory.ai

    steps:
      - uses: actions/checkout@v4

      - name: النشر إلى VPS التجريب
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /var/www/iafactory
            git pull origin next
            pnpm install --frozen-lockfile
            pnpm run build
            pm2 restart iafactory-staging

      - name: إشعار Slack
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          fields: repo,commit,author,action
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

  deploy-production:
    name: النشر إلى الإنتاج
    runs-on: ubuntu-latest
    if: github.event.inputs.environment == 'production'
    environment:
      name: production
      url: https://app.iafactory.ai

    steps:
      - uses: actions/checkout@v4

      - name: النشر إلى VPS الإنتاج
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /var/www/iafactory
            git fetch --all
            git checkout ${{ github.sha }}
            pnpm install --frozen-lockfile
            pnpm run build
            pm2 restart iafactory-prod

      - name: إنشاء إصدار
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ github.run_number }}
          release_name: الإصدار ${{ github.run_number }}
          draft: false
          prerelease: false
```

---

## 3. البيئات

### 3.1 تكوين البيئات

| المتغير | التطوير | التجريب | الإنتاج |
|---------|---------|---------|---------|
| `NODE_ENV` | development | production | production |
| `NEXT_PUBLIC_API_URL` | localhost:3000 | staging.api.iafactory.ai | api.iafactory.ai |
| `DATABASE_URL` | postgres محلي | DB تجريب | DB إنتاج |
| `LOG_LEVEL` | debug | info | warn |

### 3.2 ملفات البيئة

```bash
# الهيكل
.env.local          # محلي (غير مُلتزم)
.env.development    # التطوير
.env.staging        # التجريب
.env.production     # الإنتاج (الأسرار في GitHub)
```

### 3.3 بيئات GitHub

```yaml
# التكوين في Settings > Environments

# التجريب
- Required reviewers: 0
- Wait timer: 0 دقيقة
- Deployment branches: next

# الإنتاج
- Required reviewers: 2
- Wait timer: 5 دقائق
- Deployment branches: release/*
```

---

## 4. خط أنابيب البناء

### 4.1 خطوات البناء

```mermaid
graph LR
    A[Checkout] --> B[تثبيت التبعيات]
    B --> C[فحص الأنواع]
    C --> D[Lint]
    D --> E[اختبار]
    E --> F[بناء]
    F --> G[نشر]
```

### 4.2 التحسينات

```yaml
# تخزين pnpm المؤقت
- name: الحصول على مسار مخزن pnpm
  shell: bash
  run: echo "STORE_PATH=$(pnpm store path --silent)" >> $GITHUB_ENV

- uses: actions/cache@v4
  with:
    path: ${{ env.STORE_PATH }}
    key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-pnpm-store-

# تخزين Next.js المؤقت
- uses: actions/cache@v4
  with:
    path: ${{ github.workspace }}/.next/cache
    key: ${{ runner.os }}-nextjs-${{ hashFiles('**/pnpm-lock.yaml') }}-${{ hashFiles('**/*.ts', '**/*.tsx') }}
    restore-keys: |
      ${{ runner.os }}-nextjs-${{ hashFiles('**/pnpm-lock.yaml') }}-
```

---

## 5. الاختبارات الآلية

### 5.1 تكوين Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    include: ['**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      exclude: ['node_modules', 'tests', '**/*.d.ts'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### 5.2 اختبارات CI

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:ci": "vitest run --coverage --reporter=verbose",
    "test:e2e": "playwright test"
  }
}
```

---

## 6. النشر

### 6.1 Vercel (معاينة)

```json
// vercel.json
{
  "buildCommand": "pnpm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["cdg1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@api_url"
  }
}
```

### 6.2 VPS (التجريب/الإنتاج)

```bash
# سكربت النشر
#!/bin/bash
# scripts/deploy.sh

set -e

echo "بدء النشر..."

# سحب أحدث كود
git pull origin $BRANCH

# تثبيت التبعيات
pnpm install --frozen-lockfile

# البناء
pnpm run build

# تشغيل الترحيلات
pnpm run db:migrate

# إعادة تشغيل التطبيق
pm2 restart ecosystem.config.js

echo "اكتمل النشر!"
```

### 6.3 تكوين PM2

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'iafactory-web',
      script: 'node_modules/.bin/next',
      args: 'start -p 3000',
      instances: 'max',
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
      },
      env_staging: {
        NODE_ENV: 'production',
        PORT: 3010,
      },
    },
  ],
};
```

---

## 7. المراقبة

### 7.1 فحوصات الصحة

```yaml
# سير عمل المراقبة
name: فحص الصحة

on:
  schedule:
    - cron: '*/5 * * * *'  # كل 5 دقائق

jobs:
  health:
    runs-on: ubuntu-latest
    steps:
      - name: فحص الإنتاج
        run: |
          response=$(curl -s -o /dev/null -w "%{http_code}" https://app.iafactory.ai/api/health)
          if [ $response != "200" ]; then
            echo "فشل فحص الصحة برمز $response"
            exit 1
          fi

      - name: تنبيه عند الفشل
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          text: 'فشل فحص صحة الإنتاج!'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 8. التراجع

### 8.1 التراجع التلقائي

```yaml
# سير عمل التراجع
name: Rollback

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'البيئة للتراجع'
        required: true
        type: choice
        options:
          - staging
          - production
      commit:
        description: 'SHA الcommit للتراجع إليه'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}

    steps:
      - name: التراجع
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets[format('{0}_HOST', upper(github.event.inputs.environment))] }}
          username: ${{ secrets[format('{0}_USER', upper(github.event.inputs.environment))] }}
          key: ${{ secrets[format('{0}_SSH_KEY', upper(github.event.inputs.environment))] }}
          script: |
            cd /var/www/iafactory
            git fetch --all
            git checkout ${{ github.event.inputs.commit }}
            pnpm install --frozen-lockfile
            pnpm run build
            pm2 restart all

      - name: إشعار
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              "text": "اكتمل التراجع إلى ${{ github.event.inputs.commit }} في ${{ github.event.inputs.environment }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### 8.2 الإجراء اليدوي

```bash
# في حالة الطوارئ
ssh user@production-server

cd /var/www/iafactory

# عرض آخر commits
git log --oneline -10

# التراجع إلى commit السابق
git checkout HEAD~1

# إعادة البناء
pnpm run build

# إعادة التشغيل
pm2 restart all

# التحقق
curl -I https://app.iafactory.ai/api/health
```

---

## التواصل

لأي استفسارات حول CI/CD:
- DevOps: devops@iafactory.ai
- Slack: #devops
