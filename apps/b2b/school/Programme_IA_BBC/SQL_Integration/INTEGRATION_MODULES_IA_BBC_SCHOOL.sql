-- ============================================
-- INTÉGRATION MODULES IA - BBC SCHOOL ALGERIA
-- Programme d'Excellence IA (1AP → 4AM)
-- ============================================

SELECT '🤖 INTÉGRATION PROGRAMME EXCELLENCE IA - BBC SCHOOL' as status;
SELECT '================================================' as separator;

-- ============================================
-- 1. CRÉER NOUVELLE MATIÈRE: INTELLIGENCE ARTIFICIELLE
-- ============================================

SELECT '📋 ÉTAPE 1: Création matière IA' as etape;

-- Vérifier si la matière existe déjà
SELECT COUNT(*) as existe_deja FROM subjects WHERE name = 'Intelligence Artificielle';

-- Insérer matière IA (si n'existe pas)
INSERT INTO subjects (name, code, type, status, created_at, updated_at, branch_id)
SELECT 'Intelligence Artificielle', 'IA', 'Pratique', 1, NOW(), NOW(), 1
WHERE NOT EXISTS (SELECT 1 FROM subjects WHERE name = 'Intelligence Artificielle');

INSERT INTO subjects (name, code, type, status, created_at, updated_at, branch_id)
SELECT 'Robotique et Programmation', 'ROBO', 'Pratique', 1, NOW(), NOW(), 1
WHERE NOT EXISTS (SELECT 1 FROM subjects WHERE name = 'Robotique et Programmation');

INSERT INTO subjects (name, code, type, status, created_at, updated_at, branch_id)
SELECT 'Programmation Python', 'PY', 'Informatique', 1, NOW(), NOW(), 1
WHERE NOT EXISTS (SELECT 1 FROM subjects WHERE name = 'Programmation Python');

INSERT INTO subjects (name, code, type, status, created_at, updated_at, branch_id)
SELECT 'Scratch et Créativité Numérique', 'SCRATCH', 'Informatique', 1, NOW(), NOW(), 1
WHERE NOT EXISTS (SELECT 1 FROM subjects WHERE name = 'Scratch et Créativité Numérique');

INSERT INTO subjects (name, code, type, status, created_at, updated_at, branch_id)
SELECT 'IA Générative et Multimédia', 'IAGEN', 'Créativité', 1, NOW(), NOW(), 1
WHERE NOT EXISTS (SELECT 1 FROM subjects WHERE name = 'IA Générative et Multimédia');

SELECT 'Matières IA créées' as resultat;

-- ============================================
-- 2. CRÉER CATÉGORIES DE DEVOIRS IA
-- ============================================

SELECT '📋 ÉTAPE 2: Création catégories devoirs IA' as etape;

-- Note: structure exacte dépend du schéma homework_categories
-- Adapter selon la base de données réelle

-- ============================================
-- 3. CRÉER CONTENUS PÉDAGOGIQUES (STUDY MATERIALS)
-- ============================================

SELECT '📋 ÉTAPE 3: Création matériel d'étude IA' as etape;

-- Matériel 1AP: Découverte de l'IA
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'Les Robots et Moi - Guide 1AP',
    'Introduction à l\'IA pour les enfants de 6 ans. Découvrir ce qu\'est un robot, les assistants vocaux et les jeux éducatifs.',
    '/storage/ia_materials/1ap_robots_et_moi.pdf',
    (SELECT id FROM classes WHERE name LIKE '1%re Ann%e Primaire' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'Intelligence Artificielle' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '1%re Ann%e Primaire');

-- Matériel 2AP: IA et Langage
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'Parle Avec Robo - Guide 2AP',
    'Reconnaissance vocale et lecture assistée par IA. Activités interactives avec LALILO et chatbots éducatifs.',
    '/storage/ia_materials/2ap_parle_avec_robo.pdf',
    (SELECT id FROM classes WHERE name LIKE '2%me Ann%e Primaire' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'Intelligence Artificielle' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '2%me Ann%e Primaire');

-- Matériel 3AP: Premiers Algorithmes
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'Mes Premiers Algorithmes - Guide 3AP',
    'Comprendre les algorithmes, programmer avec Scratch Jr, créer avec l\'IA générative.',
    '/storage/ia_materials/3ap_premiers_algorithmes.pdf',
    (SELECT id FROM classes WHERE name LIKE '3%me Ann%e Primaire' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'Scratch et Créativité Numérique' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '3%me Ann%e Primaire');

-- Matériel 4AP: IA Utile
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'IA Responsable pour Enfants - Guide 4AP',
    'Recherche intelligente, analyse de données, IA dans les sciences et éthique numérique.',
    '/storage/ia_materials/4ap_ia_responsable.pdf',
    (SELECT id FROM classes WHERE name LIKE '4%me Ann%e Primaire' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'Intelligence Artificielle' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '4%me Ann%e Primaire');

-- Matériel 5AP: IA Multilingue
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'IA et Créativité - Guide 5AP (Trilingue)',
    'Apprendre l\'anglais avec IA, Scratch avancé, robotique Lego Mindstorms et IA générative.',
    '/storage/ia_materials/5ap_ia_creativite.pdf',
    (SELECT id FROM classes WHERE name LIKE '5%me Ann%e Primaire' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'IA Générative et Multimédia' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '5%me Ann%e Primaire');

-- Matériel 1AM: Python et IA
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'Python et IA pour Collégiens - Guide 1AM',
    'Bases de Python, Teachable Machine, création chatbots avec Dialogflow.',
    '/storage/ia_materials/1am_python_ia.pdf',
    (SELECT id FROM classes WHERE name LIKE '1%re Ann%e Moyenne' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'Programmation Python' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '1%re Ann%e Moyenne');

-- Matériel 2AM: Machine Learning
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'Machine Learning Expliqué - Guide 2AM',
    'Comprendre le ML, réseaux de neurones, vision par ordinateur avec OpenCV, IA et climat.',
    '/storage/ia_materials/2am_machine_learning.pdf',
    (SELECT id FROM classes WHERE name LIKE '2%me Ann%e Moyenne' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'Intelligence Artificielle' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '2%me Ann%e Moyenne');

-- Matériel 3AM: IA Générative
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'IA Créative - Guide Complet 3AM',
    'Maîtriser GPT-4, Claude, Midjourney, Runway ML, Suno, design UX avec IA.',
    '/storage/ia_materials/3am_ia_creative.pdf',
    (SELECT id FROM classes WHERE name LIKE '3%me Ann%e Moyenne' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'IA Générative et Multimédia' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '3%me Ann%e Moyenne');

-- Matériel 4AM: IA Appliquée BEM
INSERT INTO study_materials (title, description, file_path, class_id, subject_id, status, created_at, updated_at, branch_id)
SELECT
    'De 4AM au Secondaire avec IA - Guide BEM',
    'IA pour réviser BEM, projet entrepreneurial, certifications professionnelles, éthique IA avancée.',
    '/storage/ia_materials/4am_ia_bem.pdf',
    (SELECT id FROM classes WHERE name LIKE '4%me Ann%e Moyenne' LIMIT 1),
    (SELECT id FROM subjects WHERE name = 'Intelligence Artificielle' LIMIT 1),
    1,
    NOW(),
    NOW(),
    1
WHERE EXISTS (SELECT 1 FROM classes WHERE name LIKE '4%me Ann%e Moyenne');

SELECT 'Matériel d\'étude IA créé' as resultat;

-- ============================================
-- 4. METTRE À JOUR SETTINGS ÉCOLE
-- ============================================

SELECT '📋 ÉTAPE 4: Mise à jour informations école IA' as etape;

-- Ajouter mention IA dans description école
UPDATE settings
SET value = 'BBC School Algeria - Première école privée algérienne avec programme d\'Intelligence Artificielle intégré. Cycles Primaire et Moyen (1AP→4AM) avec préparation au BEM. Excellence académique + Innovation technologique.'
WHERE name = 'school_about' OR name = 'about';

-- Ajouter valeurs ajoutées IA
INSERT INTO settings (name, value, created_at, updated_at)
SELECT 'ia_program_enabled', '1', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM settings WHERE name = 'ia_program_enabled');

INSERT INTO settings (name, value, created_at, updated_at)
SELECT 'ia_program_description', 'Programme d\'Excellence IA unique en Algérie: robotique, programmation Python, IA générative, certifications internationales.', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM settings WHERE name = 'ia_program_description');

INSERT INTO settings (name, value, created_at, updated_at)
SELECT 'ia_partnerships', 'Anthropic Claude, OpenAI ChatGPT, Google AI, Microsoft Azure AI, Devoxx4Kids Algérie', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM settings WHERE name = 'ia_partnerships');

SELECT 'Settings IA mis à jour' as resultat;

-- ============================================
-- 5. CRÉER ACTUALITÉ PROGRAMME IA
-- ============================================

SELECT '📋 ÉTAPE 5: Création actualité lancement programme IA' as etape;

-- Créer actualité principale
INSERT INTO news (image_id, status, created_at, updated_at, branch_id)
VALUES (NULL, 1, NOW(), NOW(), 1);

SET @news_id = LAST_INSERT_ID();

-- Traduction française
INSERT INTO news_translates (news_id, locale, title, description, created_at, updated_at)
VALUES (
    @news_id,
    'fr',
    'BBC School lance le 1er Programme d\'Excellence IA en Algérie',
    'BBC School Algeria devient la première école privée algérienne à intégrer un programme complet d\'Intelligence Artificielle de 1AP à 4AM. Nos élèves bénéficient de cours de robotique, programmation Python, IA générative et peuvent obtenir des certifications internationales (Google AI, Microsoft AI-900). Avec des partenariats Anthropic Claude et OpenAI ChatGPT, BBC School prépare les leaders technologiques de demain. Objectif: 99.5% de réussite au BEM grâce à l\'IA!',
    NOW(),
    NOW()
);

-- Traduction arabe
INSERT INTO news_translates (news_id, locale, title, description, created_at, updated_at)
VALUES (
    @news_id,
    'ar',
    'BBC School تطلق أول برنامج تميز للذكاء الاصطناعي في الجزائر',
    'أصبحت BBC School Algeria أول مدرسة خاصة جزائرية تدمج برنامجًا كاملاً للذكاء الاصطناعي من السنة الأولى ابتدائي إلى الرابعة متوسط. يستفيد طلابنا من دروس الروبوتات وبرمجة Python والذكاء الاصطناعي التوليدي ويمكنهم الحصول على شهادات دولية (Google AI، Microsoft AI-900). بشراكات مع Anthropic Claude وOpenAI ChatGPT، تُعد BBC School قادة التكنولوجيا في الغد. الهدف: 99.5٪ نجاح في شهادة التعليم المتوسط بفضل الذكاء الاصطناعي!',
    NOW(),
    NOW()
);

-- Traduction anglaise
INSERT INTO news_translates (news_id, locale, title, description, created_at, updated_at)
VALUES (
    @news_id,
    'en',
    'BBC School launches Algeria\'s 1st AI Excellence Program',
    'BBC School Algeria becomes the first private Algerian school to integrate a comprehensive Artificial Intelligence program from 1st grade to 9th grade. Our students benefit from robotics, Python programming, generative AI courses and can obtain international certifications (Google AI, Microsoft AI-900). With partnerships with Anthropic Claude and OpenAI ChatGPT, BBC School prepares tomorrow\'s technology leaders. Goal: 99.5% BEM exam success rate thanks to AI!',
    NOW(),
    NOW()
);

SELECT 'Actualité programme IA créée (FR + AR + EN)' as resultat;

-- ============================================
-- 6. METTRE À JOUR COMPTEURS HOMEPAGE
-- ============================================

SELECT '📋 ÉTAPE 6: Ajout compteur Programme IA' as etape;

-- Ajouter nouveau compteur: Heures d'IA par an
INSERT INTO counter_translates (counter_id, locale, name, total_count, created_at, updated_at)
SELECT 1, 'fr', 'Heures IA par An', 400, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM counter_translates WHERE name = 'Heures IA par An');

INSERT INTO counter_translates (counter_id, locale, name, total_count, created_at, updated_at)
SELECT 1, 'ar', 'ساعات الذكاء الاصطناعي سنويًا', 400, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM counter_translates WHERE name = 'ساعات الذكاء الاصطناعي سنويًا');

INSERT INTO counter_translates (counter_id, locale, name, total_count, created_at, updated_at)
SELECT 1, 'en', 'AI Hours per Year', 400, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM counter_translates WHERE name = 'AI Hours per Year');

SELECT 'Compteur IA ajouté' as resultat;

-- ============================================
-- 7. VÉRIFICATIONS FINALES
-- ============================================

SELECT '✅ VÉRIFICATION FINALE' as status;
SELECT '================================' as separator;

SELECT 'Matières IA créées:' as type;
SELECT name, code, type, status
FROM subjects
WHERE name IN (
    'Intelligence Artificielle',
    'Robotique et Programmation',
    'Programmation Python',
    'Scratch et Créativité Numérique',
    'IA Générative et Multimédia'
)
ORDER BY name;

SELECT 'Matériel d\'étude IA:' as type;
SELECT title, class_id, subject_id, status
FROM study_materials
WHERE title LIKE '%IA%' OR title LIKE '%Robo%' OR title LIKE '%Python%'
ORDER BY title;

SELECT 'Actualités IA:' as type;
SELECT nt.locale, nt.title
FROM news_translates nt
WHERE nt.title LIKE '%IA%' OR nt.title LIKE '%Intelligence%'
ORDER BY nt.locale;

SELECT 'Settings IA:' as type;
SELECT name, value
FROM settings
WHERE name LIKE '%ia%'
ORDER BY name;

-- ============================================
-- RÉSUMÉ
-- ============================================

SELECT '================================================' as separator;
SELECT '✅ INTÉGRATION PROGRAMME IA TERMINÉE' as status;
SELECT '================================================' as separator;
SELECT '' as empty;
SELECT '🤖 MODULES CRÉÉS:' as titre;
SELECT '   • 5 nouvelles matières IA' as item_1;
SELECT '   • 9 documents pédagogiques (1AP→4AM)' as item_2;
SELECT '   • 1 actualité trilingue (AR/FR/EN)' as item_3;
SELECT '   • 3 settings configuration IA' as item_4;
SELECT '   • 1 compteur homepage IA' as item_5;
SELECT '' as empty;
SELECT '📚 MATIÈRES DISPONIBLES:' as titre;
SELECT '   1. Intelligence Artificielle (tous niveaux)' as matiere_1;
SELECT '   2. Robotique et Programmation' as matiere_2;
SELECT '   3. Programmation Python (Moyen)' as matiere_3;
SELECT '   4. Scratch et Créativité Numérique (Primaire)' as matiere_4;
SELECT '   5. IA Générative et Multimédia (3AM-4AM)' as matiere_5;
SELECT '' as empty;
SELECT '🎓 VALEUR AJOUTÉE:' as titre;
SELECT '   • 1ère école IA d\'Algérie' as valeur_1;
SELECT '   • 400h d\'IA par an (1AP→4AM)' as valeur_2;
SELECT '   • Certifications internationales' as valeur_3;
SELECT '   • Partenariats Anthropic, OpenAI, Google' as valeur_4;
SELECT '   • Objectif BEM: 99.5% réussite' as valeur_5;
SELECT '' as empty;
SELECT '🔄 PROCHAINES ÉTAPES:' as titre;
SELECT '   1. Créer emplois du temps avec heures IA' as etape_1;
SELECT '   2. Assigner enseignants matières IA' as etape_2;
SELECT '   3. Uploader documents PDF (9 guides)' as etape_3;
SELECT '   4. Configurer laboratoires IA' as etape_4;
SELECT '   5. Former enseignants au programme' as etape_5;
SELECT '' as empty;
