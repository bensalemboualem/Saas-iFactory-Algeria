-- ============================================
-- CORRECTION ENCODAGE UTF-8
-- BBC School Algeria - OnestSchool
-- ============================================

-- Afficher charset actuel de la base
SELECT 'CHARSET ACTUEL DATABASE:' as status;
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'onest_school';

-- ============================================
-- CONVERSION DATABASE
-- ============================================

ALTER DATABASE onest_school
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- ============================================
-- CONVERSION TABLES CRITIQUES
-- ============================================

-- Table compteurs (problème affiché ???)
ALTER TABLE counter_translates
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table catégories livres (problème arabe)
ALTER TABLE book_categories
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table livres
ALTER TABLE books
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table actualités
ALTER TABLE news_translates
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table étudiants
ALTER TABLE students
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table parents
ALTER TABLE parent_guardians
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table personnel
ALTER TABLE staff
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table utilisateurs
ALTER TABLE users
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table classes
ALTER TABLE classes
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table matières
ALTER TABLE subjects
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table sections
ALTER TABLE sections
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table section_translates
ALTER TABLE section_translates
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table départements
ALTER TABLE departments
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table désignations
ALTER TABLE designations
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table galeries
ALTER TABLE galleries
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table véhicules
ALTER TABLE vehicles
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Table settings
ALTER TABLE settings
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- ============================================
-- VÉRIFICATION FINALE
-- ============================================

SELECT '✅ ENCODAGE UTF-8 APPLIQUÉ' as status;

SELECT 'Tables converties:' as info;
SELECT TABLE_NAME, TABLE_COLLATION
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'onest_school'
AND TABLE_NAME IN (
    'counter_translates',
    'book_categories',
    'books',
    'news_translates',
    'students',
    'staff',
    'users',
    'classes',
    'subjects'
)
ORDER BY TABLE_NAME;

-- ============================================
-- TEST AFFICHAGE ARABE
-- ============================================

SELECT 'TEST ARABE - Compteurs:' as test;
SELECT name, total_count FROM counter_translates WHERE locale='ar';

SELECT 'TEST ARABE - Catégories livres:' as test;
SELECT name FROM book_categories LIMIT 5;
