# 🔧 Refactoring IAFactory - Suivi

**Début** : 11 janvier 2026, 07h00  
**Backup** : D:\IAFactory-backup-2025-01-11-04h00\ ✅

---

## Phase 1 : Sécurité & Architecture

### ✅ Jour 1 - Audit (11/01/2026)
- [x] Backup complet
- [x] Audit clés API (50+ fichiers .env détectés)
- [x] Confirmation : toutes les clés = test
- [ ] Documenter ports par projet
- [ ] Décision stratégie ports (mutuellement exclusifs vs renumérotation)

### ⏳ Jour 2 - Désactivation billing rag-dz
- [ ] Renommer services billing de rag-dz (.DISABLED)
- [ ] Créer GatewayClient dans rag-dz
- [ ] Modifier routers pour utiliser GatewayClient
- [ ] Test avec utilisateur fictif

### ⏳ Jour 3 - Centralisation providers IA
- [ ] Vérifier providers dans gateway
- [ ] Remplacer appels directs dans rag-dz
- [ ] Remplacer appels directs dans academy
- [ ] Remplacer appels directs dans ai-tools

### ⏳ Jour 4-5 - Rotation clés API (quand prod arrive)
- [ ] Générer nouvelles clés prod
- [ ] Mettre uniquement dans gateway/.env
- [ ] Supprimer des autres .env
- [ ] Révoquer anciennes clés

---

## Décisions prises

**2026-01-11 07h00** : Continuer malgré fatigue, pas de prod donc liberté totale

---

## Notes / Blocages

(Remplir au fur et à mesure)
