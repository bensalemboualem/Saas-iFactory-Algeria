# METRICS DASHBOARD TEMPLATE (Google Sheets Ready)

Usage: duplique ce plan dans Google Sheets. Chaque sheet = un onglet. Les colonnes proposées sont en ligne 1; ajoute des validations simples (listes) et fige la 1ère ligne.

## Sheet 1 — Daily Metrics
Colonnes: Date | Visits | Signups | Enrollments | Revenue | Ad Spend | Emails Sent | Conversions | CVR (Signups/Visits) | CPA (Ad Spend/Signups) | ROAS (Revenue/Ad Spend) | ARPU (Revenue/Enrollments)
Formules type:
- CVR = `=IFERROR(Signups/Visits,0)`
- CPA = `=IFERROR(AdSpend/Signups,0)`
- ROAS = `=IFERROR(Revenue/AdSpend,0)`
- ARPU = `=IFERROR(Revenue/Enrollments,0)`

## Sheet 2 — Weekly Summary
Colonnes: Week # | Visits | Signups | Enrollments | Revenue | Ad Spend | CVR | CPA | ROAS | ARPU | Notes
- Utilise `=SUMIFS(Daily!B:B,Daily!A:A,">="&StartWeek,Daily!A:A,"<="&EndWeek)`

## Sheet 3 — Goals & Targets
Colonnes: KPI | Target (Month 1) | Actual | Status (✅/⚠️/❌) | Commentaires
Exemples: Visits 1,000 | Signups 300 | Enrollments 50 | Revenue 20,000 CHF | CAC < 30 CHF | ROAS > 3x | OR Email > 35% | CTR Ads > 3%

## Sheet 4 — Financial Tracking
Colonnes: Date | Cours | Revenue | Coût Contenu | Ad Spend | Opex | Profit | Marge%
- Profit = `=Revenue - (CoûtContenu + AdSpend + Opex)`
- Marge% = `=IFERROR(Profit/Revenue,0)`

## Sheet 5 — Marketing Channels
Colonnes: Channel | Spend | Clicks | Leads | Signups | Enrollments | Revenue | CVR Lead→Signup | CVR Signup→Enroll | CAC | ROAS | Notes
- CAC = `=IFERROR(Spend/Enrollments,0)`
- ROAS = `=IFERROR(Revenue/Spend,0)`

## Sheet 6 — Course Metrics
Colonnes: Cours | Enrollments | Completions | Completion% | Avg Rating | Revenue | Refunds | Net Revenue
- Completion% = `=IFERROR(Completions/Enrollments,0)`

## Sheet 7 — User Cohorts
Colonnes: Cohort Month | New Users | Week1 Retention | Week2 | Week4 | Churn% | Notes
- Churn% = `=1 - Week4Retention`

## Sheet 8 — Funnel Metrics
Colonnes: Visits | Signups | Onboarding Done | Course Started | Course Completed | Paid | CVR Visit→Signup | CVR Signup→Paid | Drop-off Notes

## Sheet 9 — Email Metrics
Colonnes: Campaign | Date | Audience | Sent | Opens | OR | Clicks | CTR | Conversions | CR | Revenue | Unsubs
- OR = `=IFERROR(Opens/Sent,0)`; CTR = `=IFERROR(Clicks/Sent,0)`; CR = `=IFERROR(Conversions/Clicks,0)`

## Sheet 10 — KPI Dashboard
Widgets suggérés:
- Today: Visits, Signups, Revenue, ROAS, CAC, ARPU
- 7d Trend: mini-charts Visits, Signups, Revenue
- Funnels: Visit→Signup→Enroll | Email CTR/OR | Ad ROAS top 3
- Alerts: ROAS < 2, CAC > 40, OR < 25%, CVR < 3%

## Mise en place rapide (15 min)
1) Crée un Google Sheet vide, ajoute 10 onglets nommés.
2) Copie les colonnes et formules ci-dessus.
3) Ajoute validation (listes) pour Status (✅/⚠️/❌) et Channels.
4) Connecte Looker/Data Studio en lecture si tu veux un front visuel.
5) Saisie jour 0, puis mets à jour 5 min/jour.

## Rythme d'utilisation
- Daily: 5 minutes de saisie
- Weekly: 30 minutes de review (reprioriser spend, contenus, offres)
- Monthly: ajuster targets, ajouter cours/canaux

## Check-list Qualité
- Vérifie cohérence: somme par semaine = somme daily
- Compare CAC vs ARPU; si CAC > ARPU → pause/optimise ads
- Si ROAS < 2: coupe les ensembles d’annonces faibles
- Si CVR landing < 3%: améliorer preuves, FAQ, CTA
- Si OR email < 25%: retravailler sujets, segments, timing
