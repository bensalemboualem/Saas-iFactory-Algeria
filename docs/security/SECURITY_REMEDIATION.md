# SECURITY REMEDIATION - IAFactory Projects

**Date:** 2025-12-30
**Status:** URGENT - Action Required
**Affected Projects:** `onestschooled`, `iafactory-academy`, `rag-dz`

---

## EXECUTIVE SUMMARY

A security audit identified **CRITICAL vulnerabilities** across 3 projects:
- **15+ API keys exposed** in committed `.env` files
- **OTP returned in API response** (authentication bypass)
- **Database reset endpoints** accessible via HTTP
- **DEBUG mode enabled** in production configurations
- **No rate limiting** on sensitive endpoints
- **CORS wildcard (**)** allowing any origin

This document outlines the remediation steps completed and **MANDATORY actions** that require manual intervention.

---

## PART 1: MANDATORY SECRET ROTATION

### ALL SECRETS BELOW ARE COMPROMISED AND MUST BE ROTATED IMMEDIATELY

#### onestschooled (Laravel/PHP)

| Secret | Location | Action Required |
|--------|----------|-----------------|
| `APP_KEY` | `.env:3` | Run: `php artisan key:generate` |
| `JWT_SECRET` | `.env:55` | Generate new 64+ char random string |
| `MAIL_PASSWORD` | `.env:50` | Rotate in mail provider dashboard |

```bash
# Generate new APP_KEY
cd onestschooled
php artisan key:generate

# Generate new JWT_SECRET
php -r "echo 'JWT_SECRET=' . bin2hex(random_bytes(32)) . PHP_EOL;"
```

#### iafactory-academy (FastAPI/Python)

| Secret | Location | Action Required |
|--------|----------|-----------------|
| `OPENAI_API_KEY` | `.env:72` | Rotate in OpenAI dashboard |
| `ANTHROPIC_API_KEY` | `.env:75` | Rotate in Anthropic console |
| `GROQ_API_KEY` | `.env:78` | Rotate in Groq dashboard |
| `GEMINI_API_KEY` | `.env:81-82` | Rotate in Google Cloud console |
| `MISTRAL_API_KEY` | `.env:86` | Rotate in Mistral dashboard |
| `DEEPSEEK_API_KEY` | `.env:89` | Rotate in DeepSeek dashboard |
| `QWEN_API_KEY` | `.env:92-93` | Rotate in Alibaba Cloud |
| `COHERE_API_KEY` | `.env:96` | Rotate in Cohere dashboard |
| `TOGETHER_API_KEY` | `.env:99` | Rotate in Together AI dashboard |
| `OPEN_ROUTER_API_KEY` | `.env:102` | Rotate in OpenRouter dashboard |
| `KLING_ACCESS_KEY` | `.env:105-106` | Rotate in Kling dashboard |
| `SUPABASE_KEY` | `.env:111-113` | Rotate in Supabase project settings |
| `SECRET_KEY` | `.env:6` | Generate new 64+ char random string |
| `JWT_SECRET_KEY` | `.env:7-8` | Generate new 64+ char random string |
| PostgreSQL credentials | `.env:18, 22-30` | Change database passwords |
| `STRIPE_SECRET_KEY` | `backend/.env:46-48` | Rotate in Stripe dashboard |
| `SENDGRID_API_KEY` | `backend/.env:54` | Rotate in SendGrid dashboard |

```bash
# Generate new secret keys
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(64))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(64))"
```

#### rag-dz (FastAPI/Python)

| Secret | Location | Action Required |
|--------|----------|-----------------|
| DashScope API keys | `apps/dzirvideo/.env:5-14` | Rotate in Alibaba Cloud |
| Database credentials | `services/api/.env:7` | Change database password |
| JWT Secret | `services/api/.env:15` | Generate new secret |
| Groq API Key | `services/api/.env:22` | Rotate in Groq dashboard |
| Chargily credentials | `services/api/.env:26-28` | Rotate in Chargily dashboard |
| Supabase Service Key | `.env.local:30` | Rotate in Supabase settings |
| Multiple API keys | `.env.local:81-120` | Rotate all exposed keys |

---

## PART 2: CODE FIXES APPLIED

### onestschooled

| File | Change | Severity |
|------|--------|----------|
| `app/Http/Controllers/Api/AuthController.php:135` | OTP removed from API response | CRITICAL |
| `app/Http/Controllers/Backend/AuthenticationController.php:21-31` | Artisan migrate removed from constructor | CRITICAL |
| `app/Http/Controllers/ManagerController.php` | Database reset endpoint disabled | CRITICAL |
| `Modules/MainApp/Http/Controllers/AuthenticationController.php:18-26` | Artisan migrate removed | CRITICAL |
| `app/Http/Controllers/Backend/SettingController.php:189-197` | Artisan migrate disabled | HIGH |
| `routes/web.php:128-138` | /migrate-seed and /optimize routes disabled | CRITICAL |
| `app/Helpers/common-helpers.php:763` | dd() replaced with Log::error() | MEDIUM |
| `app/Traits/SendNotificationTrait.php:176` | dd() replaced with Log::error() | MEDIUM |
| `app/Http/Controllers/HomeController.php:66` | dd() replaced with Log::error() | MEDIUM |
| `tests/Feature/OtpSecurityTest.php` | New security regression tests | N/A |

### iafactory-academy

| File | Change | Severity |
|------|--------|----------|
| `backend/app/core/config.py:15-29` | DEBUG=False default + production guard | CRITICAL |
| `backend/app/main.py:67-173` | Rate limiting middleware added | HIGH |
| `backend/app/core/security.py:11-31` | JWT algorithm allowlist (rejects "none") | CRITICAL |
| `backend/app/core/security.py:107-134` | decode_token() hardened | CRITICAL |
| `backend/tests/test_jwt_security.py` | New JWT security tests | N/A |

### rag-dz

| File | Change | Severity |
|------|--------|----------|
| `services/api/main.py:18-60` | CORS restricted to specific origins | HIGH |

---

## PART 3: REMAINING WORK

### High Priority (Do This Week)

1. **Remove `.env` files from git history**
   ```bash
   # Option 1: BFG Repo-Cleaner (recommended)
   bfg --delete-files .env

   # Option 2: git filter-branch
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env .env.local .env.production" \
     --prune-empty --tag-name-filter cat -- --all

   # Force push (coordinate with team!)
   git push origin --force --all
   ```

2. **Enable GitHub Secret Scanning**
   - Go to repository Settings > Code security and analysis
   - Enable "Secret scanning"
   - Enable "Push protection"

3. **Replace remaining dd() calls in onestschooled** (40 remaining in repositories)
   ```bash
   # Find all remaining dd() calls
   grep -rn "dd(" app/ Modules/ --include="*.php" | grep -v "//.*dd("
   ```

4. **Add .env to .gitignore** (verify in all projects)
   ```gitignore
   .env
   .env.local
   .env.*.local
   .env.production
   !.env.example
   ```

### Medium Priority (This Month)

1. **Implement Redis-based rate limiting** (iafactory-academy)
   - Current implementation is in-memory, won't work with multiple instances

2. **Add CAPTCHA to registration endpoints**

3. **Implement token blacklisting for logout** (iafactory-academy)
   - TODO in `backend/app/api/auth.py:155`

4. **Reduce password reset token expiry** (onestschooled)
   - Current: 600,000 minutes (~416 days)
   - Recommended: 15-60 minutes
   - File: `config/auth.php:97-98`

---

## PART 4: TESTING COMMANDS

### onestschooled (Laravel/PHPUnit)
```bash
cd onestschooled
php artisan test --filter=OtpSecurityTest
```

### iafactory-academy (FastAPI/Pytest)
```bash
cd iafactory-academy/backend
pip install pytest pytest-asyncio
pytest tests/test_jwt_security.py -v
```

### rag-dz
```bash
cd rag-dz/services/api
# Verify CORS configuration
curl -X OPTIONS http://localhost:8181/api/rag/query \
  -H "Origin: https://evil.com" \
  -H "Access-Control-Request-Method: POST" \
  -i
# Should NOT return Access-Control-Allow-Origin: * in production
```

---

## PART 5: DEPLOYMENT CHECKLIST

Before deploying to production:

- [ ] All secrets rotated (see Part 1)
- [ ] `.env` files removed from git history
- [ ] GitHub secret scanning enabled
- [ ] `ENVIRONMENT=production` set in all deployments
- [ ] `DEBUG=false` verified in all deployments
- [ ] `CORS_ORIGINS` set to specific domains (not `*`)
- [ ] Rate limiting enabled (`RATE_LIMIT_ENABLED=True`)
- [ ] Database migrations run via CI/CD (not HTTP endpoints)
- [ ] Swagger/ReDoc disabled in production
- [ ] All tests passing

---

## REFERENCES

- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [GitHub: Remediating a Leaked Secret](https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/remediating-a-leaked-secret)
- [JWT "none" Algorithm Vulnerability](https://www.invicti.com/web-vulnerability-scanner/vulnerabilities/jwt-signature-bypass-via-none-algorithm)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)

---

**Document generated:** 2025-12-30
**Next review:** Before production deployment
