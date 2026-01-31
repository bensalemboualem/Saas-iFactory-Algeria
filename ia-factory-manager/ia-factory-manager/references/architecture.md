# 🏗️ Architecture Écosystème IA Factory

> Vue d'ensemble de tous les composants et leurs relations
> Dernière mise à jour: 2026-01-28

## Vue Globale

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           IA FACTORY ECOSYSTEM                               │
├─────────────────────────────────┬───────────────────────────────────────────┤
│       🇩🇿 ALGÉRIE                │           🇨🇭 SUISSE                       │
│   iafactoryalgeria.com          │        iafactory.ch                       │
│   45M users potentiels          │        Marché B2B/B2C                     │
│   Paiement: Chargily            │        Paiement: Stripe                   │
│   Devise: DZD                   │        Devise: CHF                        │
└─────────────────────────────────┴───────────────────────────────────────────┘
```

## Architecture Algérie 🇩🇿

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IA FACTORY ALGERIA - PLATFORM PRINCIPAL                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Frontend   │  │  API Gateway │  │   Database   │  │   Auth       │    │
│  │   Next.js    │──│  49 Routers  │──│  PostgreSQL  │──│   System     │    │
│  │   React      │  │              │  │   Prisma     │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                 │                                                  │
│         ▼                 ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         25+ APPLICATIONS IA                          │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • Chat IA Multi-modèle    • Génération Images    • Voice Assistant │    │
│  │  • Traduction FR/AR/Darija • Résumé Documents     • Code Assistant  │    │
│  │  • Education Tools         • Real Estate AI       • Gov Services    │    │
│  │  • Interview Agents        • Content Writer       • Data Analyzer   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                           17 AGENTS IA                               │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • Council (Multi-AI Consensus)     • BMAD Workflow Orchestrator    │    │
│  │  • Voice Assistant + Archon Bridge  • Education Agent               │    │
│  │  • Customer Discovery Agent         • Real Estate Agent             │    │
│  │  • Government Services Agent        • Research Agent                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        LLM PROVIDERS                                 │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  OpenAI  │  Anthropic  │  Google AI  │  Groq  │  Local Models      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│         │                                                                    │
│         ▼                                                                    │
│  ┌──────────────┐                                                           │
│  │ Chargily Pay │  ← UNIQUEMENT POUR ALGÉRIE                               │
│  │     DZD      │                                                           │
│  └──────────────┘                                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Projets Satellites Algérie 🇩🇿

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PROJETS EN DÉVELOPPEMENT                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│  │   BOLT-PLUS     │   │   RAG SYSTEM    │   │  VIDEO STUDIO   │           │
│  │      IDE        │   │                 │   │                 │           │
│  ├─────────────────┤   ├─────────────────┤   ├─────────────────┤           │
│  │ • Code Gen      │   │ • Vector DB     │   │ • TikTok Gen    │           │
│  │ • Multi-model   │   │ • Doc Process   │   │ • YouTube       │           │
│  │ • Monaco Editor │   │ • Semantic      │   │ • Replicate API │           │
│  │                 │   │                 │   │ • Wan 2.1       │           │
│  │ ⚠️ CONTAMINATION │   │ ⚠️ CONTAMINATION │   │ ⚠️ CONTAMINATION │           │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘           │
│         │                      │                      │                     │
│         └──────────────────────┼──────────────────────┘                     │
│                                │                                            │
│                    ⚠️ PROBLÈME: CODE MÉLANGÉ                                │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│  │ JORADP ARCHIVER │   │ INTERVIEW       │   │ GOV SERVICES    │           │
│  │                 │   │ AGENTS          │   │ AUTOMATION      │           │
│  ├─────────────────┤   ├─────────────────┤   ├─────────────────┤           │
│  │ • PDF Scraping  │   │ • UX Research   │   │ • Utilities     │           │
│  │ • OCR FR/AR     │   │ • Customer      │   │ • Telecom       │           │
│  │ • Vector DB     │   │   Discovery     │   │ • CNAS/CASNOS   │           │
│  │ • Journal Off.  │   │ • Auto Interviews│   │ • CNRC          │           │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Architecture Suisse 🇨🇭

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      IA FACTORY SUISSE - PLATFORM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Frontend   │  │  API Gateway │  │   Database   │  │   Auth       │    │
│  │   Next.js    │──│   Routers    │──│  PostgreSQL  │──│   System     │    │
│  │   React      │  │              │  │   Prisma     │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         APPLICATIONS IA                              │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • Agents IA                                                         │    │
│  │  • Voice Assistant                                                   │    │
│  │  • (Features subset d'Algérie)                                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        LLM PROVIDERS                                 │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  OpenAI  │  Anthropic  │  Google AI                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│         │                                                                    │
│         ▼                                                                    │
│  ┌──────────────┐                                                           │
│  │    Stripe    │  ← UNIQUEMENT POUR SUISSE                                │
│  │     CHF      │                                                           │
│  └──────────────┘                                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Flow de Données

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    User     │────▶│   Frontend  │────▶│  API Router │────▶│   Service   │
│   Request   │     │   (Next.js) │     │             │     │  (Agent/App)│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Response  │◀────│   Format    │◀────│     LLM     │◀────│   Process   │
│   to User   │     │   Output    │     │   Provider  │     │   Request   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Zones de Risque de Contamination

```
⚠️ DANGER ZONES - Ne JAMAIS mélanger:

1. PAYMENT
   ┌─────────────────────────────────────────────────────────────────┐
   │  🇩🇿 Chargily (DZD)  ◄──── MURS ────►  🇨🇭 Stripe (CHF)         │
   │  JAMAIS dans Suisse                     JAMAIS dans Algérie    │
   └─────────────────────────────────────────────────────────────────┘

2. ENV FILES
   ┌─────────────────────────────────────────────────────────────────┐
   │  .env.algeria  ◄────── SÉPARÉS ──────►  .env.suisse            │
   │  Ne jamais copier de l'un à l'autre                            │
   └─────────────────────────────────────────────────────────────────┘

3. PROJETS SATELLITES
   ┌─────────────────────────────────────────────────────────────────┐
   │  BOLT-PLUS  ◄──── CONTAMINATION ACTUELLE ────►  RAG + VIDEO    │
   │  ACTION: Nettoyer chaque repo individuellement                 │
   └─────────────────────────────────────────────────────────────────┘
```

## Checklist Nouvelle Feature

```
□ Quel marché? (🇩🇿 ou 🇨🇭)
□ Quel projet? (voir projects.json)
□ Quel .env?
□ Quelles clés API nécessaires?
□ Header commentaire ajouté? (// Market: ALGERIA ou // Market: SWITZERLAND)
□ Test contamination passé?
```
