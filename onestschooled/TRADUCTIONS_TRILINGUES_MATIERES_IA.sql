-- ============================================
-- TRADUCTIONS TRILINGUES MATIÈRES IA
-- BBC School Algeria
-- Arabe, Français, Anglais
-- ============================================

SELECT '🌍 MISE À JOUR TRADUCTIONS TRILINGUES - MATIÈRES IA' as status;

-- ============================================
-- 1. METTRE À JOUR LES NOMS DES MATIÈRES (Multilingue)
-- ============================================

-- Approche: Utiliser un format qui inclut les 3 langues
-- Format: "Nom FR / AR Name / EN Name"

-- Intelligence Artificielle
UPDATE subjects
SET name = 'Intelligence Artificielle / الذكاء الاصطناعي / Artificial Intelligence'
WHERE id = 273;

-- Robotique et Programmation
UPDATE subjects
SET name = 'Robotique et Programmation / الروبوتات والبرمجة / Robotics and Programming'
WHERE id = 274;

-- Programmation Python
UPDATE subjects
SET name = 'Programmation Python / برمجة بايثون / Python Programming'
WHERE id = 275;

SELECT 'Matières mises à jour avec noms trilingues' as resultat;

-- ============================================
-- 2. VÉRIFICATION
-- ============================================

SELECT '✅ VÉRIFICATION MATIÈRES TRILINGUES' as status;

SELECT id, name, code, status
FROM subjects
WHERE id IN (273, 274, 275);

-- ============================================
-- FIN
-- ============================================

SELECT '✅ TRADUCTIONS TRILINGUES APPLIQUÉES' as status;
