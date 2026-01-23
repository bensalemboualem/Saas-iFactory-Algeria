# Troubleshooting Guide

**IAFACTORY - Common Problem Resolution**

*Last updated: January 19, 2026*

---

## Table of Contents

1. [Connection Issues](#1-connection-issues)
2. [Performance Issues](#2-performance-issues)
3. [AI Errors](#3-ai-errors)
4. [Payment Issues](#4-payment-issues)
5. [API Issues](#5-api-issues)
6. [Mobile/Desktop Issues](#6-mobiledesktop-issues)
7. [Error Codes](#7-error-codes)

---

## 1. Connection Issues

### 1.1 Unable to Log In

**Symptoms:**
- Login page reloading in a loop
- "Incorrect credentials" message
- White screen after login

**Solutions:**

1. **Verify credentials**
   ```
   - Check email is correct (watch for spaces)
   - Password is case-sensitive
   ```

2. **Clear browser cache**
   ```
   Chrome: Ctrl+Shift+Delete > All time > Clear
   Firefox: Ctrl+Shift+Delete > Everything > Clear
   Safari: Cmd+Alt+E
   ```

3. **Disable extensions**
   - AdBlockers can block requests
   - VPN/Proxy can cause issues

4. **Try incognito mode**
   ```
   Chrome: Ctrl+Shift+N
   Firefox: Ctrl+Shift+P
   ```

5. **Reset password**
   - [Password reset link](https://app.iafactory.ai/forgot-password)

### 1.2 Frequently Expired Sessions

**Possible cause:** Cookies blocked or automatically deleted

**Solution:**
1. Allow cookies for `*.iafactory.ai`
2. Check that browser doesn't delete cookies on close
3. Disable automatic cleaning extensions

### 1.3 "Too Many Attempts" Error

**Solution:**
- Wait 15 minutes
- Use "Forgot password" if needed
- Contact support if problem persists

---

## 2. Performance Issues

### 2.1 Slow Interface

**Diagnosis:**

```javascript
// Open console (F12) and run:
performance.now()
// Then after navigation:
performance.now()
// Difference > 3000ms = problem
```

**Solutions:**

1. **Check internet connection**
   ```bash
   # Latency test
   ping api.iafactory.ai
   ```

2. **Reduce active conversations**
   - Archive old conversations
   - Limit to 20 visible conversations

3. **Update browser**
   - Chrome, Firefox, Safari latest version

4. **Disable animations (accessibility)**
   ```
   Settings > Accessibility > Reduce animations
   ```

### 2.2 Slow Message Loading

**Possible causes:**
- Conversation with many messages (>100)
- Messages with large images/files

**Solutions:**
1. Create a new conversation
2. Export and archive the old one
3. Enable "Progressive loading" in settings

### 2.3 High Memory Usage

**Symptom:** Browser consuming > 2GB RAM

**Solutions:**
1. Close unnecessary tabs
2. Reload page (F5)
3. Use desktop app (more optimized)

---

## 3. AI Errors

### 3.1 "Generation Error"

**Code: `AI_GENERATION_ERROR`**

**Causes and solutions:**

| Cause | Solution |
|-------|----------|
| AI server overloaded | Retry in 1 minute |
| Prompt too long | Reduce to < 4000 tokens |
| Filtered content | Rephrase without sensitive terms |
| Timeout | Split request into parts |

### 3.2 "Model Unavailable"

**Code: `MODEL_UNAVAILABLE`**

**Solutions:**
1. Check status: [status.iafactory.ai](https://status.iafactory.ai)
2. Try another model
3. Wait for maintenance (usually < 1h)

### 3.3 Truncated Response

**Symptom:** Response cuts off abruptly

**Causes:**
- Token limit reached
- Generation timeout

**Solutions:**
1. Ask "Continue" or "Go on"
2. Increase token limit (Settings > Model)
3. Request a shorter response

### 3.4 Incorrect Response / Hallucinations

**AI can sometimes:**
- Invent facts
- Give outdated info
- Contradict itself

**Best practices:**
1. Always verify important information
2. Ask for sources
3. Rephrase with more context
4. Use a more recent model (GPT-4, Claude 3)

---

## 4. Payment Issues

### 4.1 Payment Declined

**Chargily Pay (Algeria):**

| Error | Solution |
|-------|----------|
| Card not recognized | Verify CIB/EDAHABIA enabled for e-commerce |
| Insufficient balance | Check bank balance |
| Limit reached | Contact your bank |
| Invalid OTP code | Request a new code |

**International card:**

| Error | Solution |
|-------|----------|
| 3D Secure failed | Allow online transactions |
| Expired card | Update card info |
| Invalid address | Use exact billing address |

### 4.2 Subscription Not Activated

**After successful payment but no credits:**

1. Wait 5 minutes (synchronization)
2. Log out/Log in
3. Check in Settings > Billing
4. Contact support with payment receipt

### 4.3 Billing Error

**Procedure:**
1. Download the relevant invoice
2. Send to billing@iafactory.ai with:
   - Invoice number
   - Problem description
   - Expected vs billed amount
3. Processing time: 5 business days

---

## 5. API Issues

### 5.1 Error 401 Unauthorized

```json
{
  "error": "unauthorized",
  "message": "Invalid API key"
}
```

**Solutions:**
1. Verify API key is correct
2. Check it hasn't been revoked
3. Regenerate a new key if necessary

### 5.2 Error 429 Too Many Requests

```json
{
  "error": "rate_limited",
  "message": "Too many requests",
  "retry_after": 60
}
```

**Solutions:**
1. Implement exponential backoff
2. Respect your plan limits
3. Upgrade if you need more requests

**Limits by plan:**

| Plan | Requests/minute |
|------|-----------------|
| Free | 10 |
| Pro | 60 |
| Pro+ | 300 |
| Enterprise | Custom |

### 5.3 Error 500 Internal Server Error

```json
{
  "error": "internal_error",
  "message": "Something went wrong",
  "request_id": "req_abc123"
}
```

**Actions:**
1. Retry the request
2. Check status.iafactory.ai
3. If persistent, contact support with `request_id`

### 5.4 Timeouts

**Symptom:** Request not completing

**Solutions:**
1. Increase client timeout (recommended: 120s for generation)
2. Use streaming for long responses
3. Split large requests

```typescript
// Example with streaming
const response = await fetch('/api/chat', {
  method: 'POST',
  body: JSON.stringify({ stream: true, ... }),
});

const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  // Process chunk
}
```

---

## 6. Mobile/Desktop Issues

### 6.1 Desktop App - White Screen

**Windows:**
```bash
# Delete cache
rmdir /s /q "%APPDATA%\iafactory"
# Relaunch application
```

**macOS:**
```bash
rm -rf ~/Library/Application\ Support/iafactory
rm -rf ~/Library/Caches/iafactory
```

**Linux:**
```bash
rm -rf ~/.config/iafactory
rm -rf ~/.cache/iafactory
```

### 6.2 Desktop App - Won't Start

**Solutions:**
1. Check system requirements
   - Windows 10+ / macOS 10.15+ / Ubuntu 20.04+
   - 4GB RAM minimum
2. Run as administrator (Windows)
3. Reinstall application

### 6.3 Sync Between Devices

**Symptom:** Different conversations on web and desktop

**Solutions:**
1. Check internet connection on both devices
2. Force sync: Settings > Data > Sync
3. Log out/Log in

---

## 7. Error Codes

### Quick Reference

| Code | Description | Quick Solution |
|------|-------------|----------------|
| `AUTH_001` | Token expired | Reconnect |
| `AUTH_002` | Account disabled | Contact support |
| `AUTH_003` | 2FA required | Enter 2FA code |
| `CRED_001` | Insufficient credits | Buy credits |
| `CRED_002` | Daily limit | Wait 24h or upgrade |
| `AI_001` | Model unavailable | Try another model |
| `AI_002` | Prompt too long | Shorten prompt |
| `AI_003` | Content filtered | Rephrase request |
| `AI_004` | Generation timeout | Retry or split |
| `API_001` | Invalid key | Verify/regenerate key |
| `API_002` | Rate limit | Wait or upgrade |
| `API_003` | Endpoint not found | Check URL |
| `PAY_001` | Payment declined | Check card/account |
| `PAY_002` | Subscription expired | Renew |
| `FILE_001` | File too large | Reduce size |
| `FILE_002` | Format not supported | Convert file |

---

## 8. Advanced Diagnostics

### 8.1 Collect Debug Information

Open console (F12) and run:

```javascript
// Copy this info for support
console.log({
  userAgent: navigator.userAgent,
  platform: navigator.platform,
  language: navigator.language,
  cookies: navigator.cookieEnabled,
  localStorage: typeof localStorage !== 'undefined',
  online: navigator.onLine,
  memory: navigator.deviceMemory,
});
```

### 8.2 Export Logs

**In the application:**
1. Settings > Advanced > Export logs
2. File `iafactory-logs-YYYYMMDD.zip` downloaded

### 8.3 Check Connectivity

```bash
# Test API
curl -I https://api.iafactory.ai/health

# Test WebSocket
wscat -c wss://ws.iafactory.ai/connect
```

---

## Contact Support

If the problem persists after trying these solutions:

- **Email**: support@iafactory.ai
- **Live chat**: app.iafactory.ai (Pro+ and Enterprise)
- **Discord**: discord.gg/iafactory

**Information to provide:**
1. Problem description
2. Steps to reproduce
3. Error code (if applicable)
4. Screenshots
5. Browser/OS/App version
6. Diagnostic result (section 8.1)

---

*This guide is updated regularly. Last revision: January 19, 2026*
