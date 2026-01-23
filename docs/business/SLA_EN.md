# Service Level Agreement (SLA)

**IAFACTORY - Service Level Agreement**

*Last updated: January 19, 2026*

---

## 1. Introduction

This document defines the service levels guaranteed by IAFACTORY for its various subscription plans.

---

## 2. Service Availability

### 2.1 Commitments by Plan

| Plan | Guaranteed Availability | Planned Maintenance |
|------|------------------------|---------------------|
| Free | Best effort | Not notified |
| Pro | 99.5% | 24h advance notice |
| Pro+ | 99.9% | 48h advance notice |
| Enterprise | 99.95% | 72h advance notice |

### 2.2 Availability Calculation

```
Availability (%) = ((Total Time - Downtime) / Total Time) × 100
```

**Exclusions from calculation:**
- Planned and notified maintenance
- Force majeure events
- Third-party provider issues (OpenAI, Anthropic, etc.)
- User-side network problems

---

## 3. Performance

### 3.1 API Response Times

| Metric | Free | Pro | Pro+ | Enterprise |
|--------|------|-----|------|------------|
| Median latency | < 2s | < 1s | < 500ms | < 200ms |
| P95 latency | < 5s | < 3s | < 2s | < 1s |
| Rate limit | 10 req/min | 60 req/min | 300 req/min | Custom |

### 3.2 AI Processing Times

AI response times depend on models used and are not guaranteed by this SLA. Typical times:

| Model | Typical Time (1K tokens) |
|-------|--------------------------|
| GPT-3.5 | 1-3 seconds |
| GPT-4 | 5-15 seconds |
| Claude 3 Sonnet | 3-8 seconds |
| Claude 3 Opus | 10-30 seconds |

---

## 4. Technical Support

### 4.1 Support Channels

| Plan | Email | Chat | Phone | Dedicated Slack/Teams |
|------|-------|------|-------|----------------------|
| Free | ✓ | - | - | - |
| Pro | ✓ | - | - | - |
| Pro+ | ✓ | ✓ | - | - |
| Enterprise | ✓ | ✓ | ✓ | ✓ |

### 4.2 Response Times (First Contact)

| Priority | Description | Free | Pro | Pro+ | Enterprise |
|----------|-------------|------|-----|------|------------|
| **P1 - Critical** | Service completely unavailable | 5 days | 4h | 1h | 15 min |
| **P2 - Major** | Major functionality impacted | 5 days | 8h | 4h | 1h |
| **P3 - Moderate** | Minor functionality impacted | 5 days | 24h | 8h | 4h |
| **P4 - Low** | Question, improvement | 5 days | 48h | 24h | 8h |

### 4.3 Priority Definitions

**P1 - Critical:**
- Platform completely inaccessible
- User data loss
- Critical security vulnerability

**P2 - Major:**
- Main functionality not working (chat, generation)
- Severely degraded performance (> 10x normal time)
- Authentication failure

**P3 - Moderate:**
- Secondary functionality not working
- Bug affecting user experience
- Moderate slowness

**P4 - Low:**
- Information request
- Improvement suggestion
- Cosmetic bug

---

## 5. Maintenance

### 5.1 Planned Maintenance

- **Standard window**: Sunday 02:00-06:00 UTC
- **Notification**: According to plan (see section 2.1)
- **Communication**: Email + in-app banner

### 5.2 Emergency Maintenance

For critical security fixes, emergency maintenance may be performed with minimal notice. Enterprise users will be contacted directly.

---

## 6. Backup and Recovery

### 6.1 Backup Policy

| Element | Frequency | Retention |
|---------|-----------|-----------|
| Database | Every 6h | 30 days |
| User files | Daily | 30 days |
| Logs | Continuous | 90 days |

### 6.2 Recovery Objectives

| Metric | Objective |
|--------|-----------|
| RPO (Recovery Point Objective) | 6 hours |
| RTO (Recovery Time Objective) | 4 hours |

---

## 7. Security

### 7.1 Commitments

- TLS 1.3 encryption for all communications
- AES-256 encryption of data at rest
- Annual security audits (Pro+ and Enterprise)
- GDPR and Algerian law 18-07 compliance

### 7.2 Incident Notification

| Severity | Notification Delay |
|----------|-------------------|
| Critical (data breach) | 24 hours |
| Major | 48 hours |
| Minor | Monthly report |

---

## 8. Service Credits (Compensation)

### 8.1 Eligibility

Service credits apply only to paid plans (Pro, Pro+, Enterprise) in case of non-compliance with availability commitments.

### 8.2 Credit Calculation

| Monthly Availability | Credit |
|---------------------|--------|
| 99.0% - 99.5% | 10% of monthly invoice |
| 95.0% - 99.0% | 25% of monthly invoice |
| 90.0% - 95.0% | 50% of monthly invoice |
| < 90.0% | 100% of monthly invoice |

### 8.3 Claim Procedure

1. Submit a request within 30 days of the incident
2. Email to sla@iafactory.ai with:
   - Dates and times of incidents
   - Description of impact
   - Screenshots if available
3. Response within 10 business days
4. Credit applied to next invoice

### 8.4 Limitations

- Maximum credit: 100% of monthly invoice
- Cannot be combined with other discounts
- Not convertible to cash
- Not applicable if user violates ToS

---

## 9. Exclusions

This SLA does not apply in the following cases:

1. **Force majeure**: natural disasters, wars, pandemics
2. **Third-party providers**: OpenAI, Anthropic, Google unavailability
3. **User actions**: abuse, ToS violation
4. **Network**: ISP issues on user side
5. **Alpha/Beta**: preview features

---

## 10. Modifications

IAFACTORY reserves the right to modify this SLA with 30 days notice. Unfavorable modifications do not apply to current Enterprise subscriptions.

---

## 11. Contact

**SLA Support:**
- Email: sla@iafactory.ai
- Portal: status.iafactory.ai

**Escalation (Enterprise):**
- Dedicated Account Manager
- Direct hotline

---

*This SLA is effective as of January 19, 2026.*
