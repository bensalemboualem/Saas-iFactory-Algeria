-- ============================================
-- CORRECTION URGENTE - COMPTEURS HOMEPAGE
-- BBC School Algeria - OnestSchool
-- ============================================

-- Afficher les valeurs actuelles
SELECT 'AVANT CORRECTION:' as status;
SELECT locale, name, total_count FROM counter_translates ORDER BY locale, id;

-- ============================================
-- CORRECTION ARABE
-- ============================================

-- Étudiants Actifs: 4 → 804
UPDATE counter_translates
SET total_count = 804
WHERE (name LIKE '%طلاب%' OR name LIKE '%الطلاب%')
AND locale = 'ar';

-- Enseignants Experts: 54 → 70
UPDATE counter_translates
SET total_count = 70
WHERE (name LIKE '%معلم%' OR name LIKE '%المعلم%')
AND locale = 'ar';

-- Classes Actives: 22 → 250
UPDATE counter_translates
SET total_count = 250
WHERE (name LIKE '%فصل%' OR name LIKE '%الفصول%')
AND locale = 'ar';

-- Taux de Réussite: garder 98%
-- (déjà correct)

-- ============================================
-- CORRECTION ANGLAIS
-- ============================================

-- Active Students: 4 → 804
UPDATE counter_translates
SET total_count = 804
WHERE name = 'Active Students'
AND locale = 'en';

-- Expert Teachers: 54 → 70
UPDATE counter_translates
SET total_count = 70
WHERE name = 'Expert Teachers'
AND locale = 'en';

-- Active Classes: 22 → 250
UPDATE counter_translates
SET total_count = 250
WHERE name = 'Active Classes'
AND locale = 'en';

-- Success Rate: garder 98%
-- (déjà correct)

-- Parents: garder 304
-- (déjà correct)

-- ============================================
-- CORRECTION FRANÇAIS
-- ============================================

-- Étudiants Actifs: 4 → 804
UPDATE counter_translates
SET total_count = 804
WHERE name LIKE '%tudiants Actifs%'
AND locale = 'fr';

-- Enseignants Experts: 54 → 70
UPDATE counter_translates
SET total_count = 70
WHERE name LIKE '%Enseignants%'
AND locale = 'fr';

-- Classes Actives: 22 → 250
UPDATE counter_translates
SET total_count = 250
WHERE name LIKE '%Classes Actives%'
AND locale = 'fr';

-- Taux de Réussite: garder 98%
-- (déjà correct)

-- ============================================
-- VÉRIFICATION FINALE
-- ============================================

SELECT 'APRÈS CORRECTION:' as status;
SELECT locale, name, total_count FROM counter_translates ORDER BY locale, id;

-- ============================================
-- RÉSUMÉ
-- ============================================
SELECT '✅ COMPTEURS CORRIGÉS' as status;
SELECT 'Étudiants: 4 → 804' as correction_1;
SELECT 'Enseignants: 54 → 70' as correction_2;
SELECT 'Classes: 22 → 250' as correction_3;
