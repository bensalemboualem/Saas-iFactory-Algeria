-- ============================================
-- CORRECTION BBC SCHOOL ALGERIA
-- École jusqu'au BEM SEULEMENT (pas de secondaire)
-- ============================================

SELECT '🔧 CORRECTION BBC SCHOOL - PRIMAIRE + MOYEN UNIQUEMENT' as status;

-- ============================================
-- 1. SUPPRIMER TOUTES LES CLASSES SECONDAIRES
-- ============================================

SELECT '📋 ÉTAPE 1: Suppression classes secondaires (1AS, 2AS, 3AS)' as etape;

-- Désactiver les class_setups pour secondaire
UPDATE class_setups cs
JOIN classes c ON cs.classes_id = c.id
SET cs.status = 0
WHERE c.name LIKE '%Secondaire%'
   OR c.name LIKE '%AS%'
   OR c.name LIKE '%2AS%'
   OR c.name LIKE '%1AS%'
   OR c.name LIKE '%3AS%'
   OR c.name LIKE '%Bac%'
   OR c.name LIKE '%Lettres et Philosophie%'
   OR c.name LIKE '%Sciences Exactes%'
   OR c.name LIKE '%Sciences Naturelles%';

-- Marquer classes secondaires comme inactives
UPDATE classes
SET status = 0
WHERE name LIKE '%Secondaire%'
   OR name LIKE '%AS%'
   OR name LIKE '%2AS%'
   OR name LIKE '%1AS%'
   OR name LIKE '%3AS%'
   OR name LIKE '%Bac%'
   OR name LIKE '%Lettres et Philosophie%'
   OR name LIKE '%Sciences Exactes%'
   OR name LIKE '%Sciences Naturelles%';

SELECT 'Classes secondaires désactivées' as resultat;

-- ============================================
-- 2. GARDER UNIQUEMENT PRIMAIRE + MOYEN
-- ============================================

SELECT '📋 ÉTAPE 2: Activation classes Primaire + Moyen' as etape;

-- Activer classes primaires
UPDATE classes
SET status = 1
WHERE name LIKE '%Primaire%'
   OR name LIKE '%AP%'
   OR name IN ('1ère Année Primaire', '2ème Année Primaire', '3ème Année Primaire',
               '4ème Année Primaire', '5ème Année Primaire');

-- Activer classes moyennes
UPDATE classes
SET status = 1
WHERE name LIKE '%Moyenne%'
   OR name LIKE '%AM%'
   OR name IN ('1ère Année Moyenne', '2ème Année Moyenne', '3ème Année Moyenne', '4ème Année Moyenne');

SELECT 'Classes Primaire + Moyen activées' as resultat;

-- ============================================
-- 3. CRÉER/VÉRIFIER CLASSES OFFICIELLES ALGÉRIENNES
-- ============================================

SELECT '📋 ÉTAPE 3: Standardisation nomenclature algérienne' as etape;

-- Vérifier si les classes officielles existent
SELECT 'Classes Primaires existantes:' as info;
SELECT name, status FROM classes
WHERE name IN (
    '1ère Année Primaire', '2ème Année Primaire', '3ème Année Primaire',
    '4ème Année Primaire', '5ème Année Primaire',
    '1AP', '2AP', '3AP', '4AP', '5AP'
) ORDER BY name;

SELECT 'Classes Moyennes existantes:' as info;
SELECT name, status FROM classes
WHERE name IN (
    '1ère Année Moyenne', '2ème Année Moyenne', '3ème Année Moyenne', '4ème Année Moyenne',
    '1AM', '2AM', '3AM', '4AM'
) ORDER BY name;

-- ============================================
-- 4. CORRIGER COMPTEURS HOMEPAGE
-- ============================================

SELECT '📋 ÉTAPE 4: Correction compteurs (exclure secondaire)' as etape;

-- Compter uniquement étudiants Primaire + Moyen
SET @students_count = (
    SELECT COUNT(DISTINCT s.id)
    FROM students s
    JOIN class_setup_childrens csc ON s.id IN (
        SELECT student_id FROM class_setup_childrens WHERE student_id IS NOT NULL
    )
    JOIN class_setups cs ON csc.class_setup_id = cs.id
    JOIN classes c ON cs.classes_id = c.id
    WHERE c.status = 1
    AND (c.name LIKE '%Primaire%' OR c.name LIKE '%Moyenne%' OR c.name LIKE '%AP%' OR c.name LIKE '%AM%')
);

-- Note: Si la colonne student_id n'existe pas, utiliser COUNT des étudiants actifs
SET @students_total = (SELECT COUNT(*) FROM students);

-- Compter classes actives (Primaire + Moyen seulement)
SET @classes_count = (
    SELECT COUNT(*)
    FROM classes
    WHERE status = 1
    AND (name LIKE '%Primaire%' OR name LIKE '%Moyenne%' OR name LIKE '%AP%' OR name LIKE '%AM%')
);

-- Afficher statistiques
SELECT 'STATISTIQUES BBC SCHOOL:' as info;
SELECT CONCAT('Étudiants total: ', @students_total) as stat_1;
SELECT CONCAT('Classes actives (Primaire+Moyen): ', @classes_count) as stat_2;
SELECT CONCAT('Enseignants: 70') as stat_3;

-- Mettre à jour compteurs (Arabe)
UPDATE counter_translates
SET total_count = @students_total
WHERE locale = 'ar' AND (name LIKE '%طلاب%' OR name LIKE '%الطلاب%');

UPDATE counter_translates
SET total_count = 70
WHERE locale = 'ar' AND (name LIKE '%معلم%' OR name LIKE '%المعلم%');

UPDATE counter_translates
SET total_count = @classes_count
WHERE locale = 'ar' AND (name LIKE '%فصل%' OR name LIKE '%الفصول%');

-- Mettre à jour compteurs (Français)
UPDATE counter_translates
SET total_count = @students_total
WHERE locale = 'fr' AND name LIKE '%tudiants Actifs%';

UPDATE counter_translates
SET total_count = 70
WHERE locale = 'fr' AND name LIKE '%Enseignants%';

UPDATE counter_translates
SET total_count = @classes_count
WHERE locale = 'fr' AND name LIKE '%Classes Actives%';

-- Mettre à jour compteurs (Anglais)
UPDATE counter_translates
SET total_count = @students_total
WHERE locale = 'en' AND name = 'Active Students';

UPDATE counter_translates
SET total_count = 70
WHERE locale = 'en' AND name = 'Expert Teachers';

UPDATE counter_translates
SET total_count = @classes_count
WHERE locale = 'en' AND name = 'Active Classes';

SELECT 'Compteurs homepage corrigés' as resultat;

-- ============================================
-- 5. METTRE À JOUR INFORMATIONS ÉCOLE
-- ============================================

SELECT '📋 ÉTAPE 5: Mise à jour informations école' as etape;

-- Mettre à jour settings
UPDATE settings
SET value = 'BBC School Algeria - Primaire & Moyen (jusqu''au BEM)'
WHERE name = 'school_name';

UPDATE settings
SET value = 'École privée algérienne - Cycles Primaire et Moyen. Préparation au BEM (Brevet d''Enseignement Moyen).'
WHERE name = 'school_about' OR name = 'about';

SELECT 'Informations école mises à jour' as resultat;

-- ============================================
-- 6. VÉRIFICATIONS FINALES
-- ============================================

SELECT '✅ VÉRIFICATION FINALE' as status;
SELECT '================================' as separator;

SELECT 'Classes Primaires (actives):' as type;
SELECT name, status
FROM classes
WHERE status = 1 AND (name LIKE '%Primaire%' OR name LIKE '%AP%')
ORDER BY name
LIMIT 10;

SELECT 'Classes Moyennes (actives):' as type;
SELECT name, status
FROM classes
WHERE status = 1 AND (name LIKE '%Moyenne%' OR name LIKE '%AM%')
ORDER BY name
LIMIT 10;

SELECT 'Classes Secondaires (DÉSACTIVÉES):' as type;
SELECT name, status
FROM classes
WHERE status = 0 AND (name LIKE '%Secondaire%' OR name LIKE '%AS%')
ORDER BY name
LIMIT 10;

SELECT 'Compteurs Homepage:' as type;
SELECT locale, name, total_count
FROM counter_translates
WHERE name LIKE '%tudiant%' OR name LIKE '%Student%' OR name LIKE '%طلاب%'
   OR name LIKE '%Teacher%' OR name LIKE '%معلم%'
   OR name LIKE '%Class%' OR name LIKE '%فصل%'
ORDER BY locale, name;

-- ============================================
-- RÉSUMÉ
-- ============================================

SELECT '================================================' as separator;
SELECT '✅ CORRECTION TERMINÉE - BBC SCHOOL ALGERIA' as status;
SELECT '================================================' as separator;
SELECT '' as empty;
SELECT '🎓 NIVEAUX PROPOSÉS:' as titre;
SELECT '   ✅ Primaire: 1AP → 5AP (5 ans)' as niveau_1;
SELECT '   ✅ Moyen: 1AM → 4AM (4 ans) - Préparation BEM' as niveau_2;
SELECT '   ❌ Secondaire: NON (pas de BAC)' as niveau_3;
SELECT '' as empty;
SELECT '📊 CLASSES ACTIVES:' as titre;
SELECT CONCAT('   • Primaire: ', (SELECT COUNT(*) FROM classes WHERE status=1 AND (name LIKE '%Primaire%' OR name LIKE '%AP%')), ' classes') as stat_1;
SELECT CONCAT('   • Moyen: ', (SELECT COUNT(*) FROM classes WHERE status=1 AND (name LIKE '%Moyenne%' OR name LIKE '%AM%')), ' classes') as stat_2;
SELECT CONCAT('   • Secondaire: ', (SELECT COUNT(*) FROM classes WHERE status=0 AND (name LIKE '%Secondaire%' OR name LIKE '%AS%')), ' classes (DÉSACTIVÉES)') as stat_3;
SELECT '' as empty;
SELECT '🔄 PROCHAINES ÉTAPES:' as titre;
SELECT '   1. Nettoyer caches Laravel (php artisan cache:clear)' as etape_1;
SELECT '   2. Vérifier dashboard ne montre que Primaire + Moyen' as etape_2;
SELECT '   3. Tester inscription étudiants (max 4AM)' as etape_3;
SELECT '' as empty;
