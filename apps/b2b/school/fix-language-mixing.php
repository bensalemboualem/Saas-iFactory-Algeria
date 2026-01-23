<?php
echo "=== Correction du mélange de langues BBC School Algeria ===" . PHP_EOL;

try {
    $pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');
    
    // Traductions complètes pour chaque section
    $translations = [
        // Section 4 - Explore
        4 => [
            'en' => [
                'name' => 'Discover BBC School Algeria',
                'description' => 'Explore our modern educational environment designed for excellence and innovation.',
                'data' => json_encode([
                    'title' => 'Discover BBC School Algeria',
                    'subtitle' => 'Excellence in Education',
                    'content' => 'Explore our modern educational environment designed for excellence and innovation.'
                ])
            ],
            'fr' => [
                'name' => 'Découvrir BBC School Algeria',
                'description' => 'Explorez notre environnement éducatif moderne conçu pour l\'excellence et l\'innovation.',
                'data' => json_encode([
                    'title' => 'Découvrir BBC School Algeria',
                    'subtitle' => 'Excellence en Éducation',
                    'content' => 'Explorez notre environnement éducatif moderne conçu pour l\'excellence et l\'innovation.'
                ])
            ],
            'ar' => [
                'name' => 'اكتشف مدرسة بي بي سي الجزائر',
                'description' => 'استكشف بيئتنا التعليمية الحديثة المصممة للتميز والابتكار.',
                'data' => json_encode([
                    'title' => 'اكتشف مدرسة بي بي سي الجزائر',
                    'subtitle' => 'التميز في التعليم',
                    'content' => 'استكشف بيئتنا التعليمية الحديثة المصممة للتميز والابتكار.'
                ])
            ]
        ],
        
        // Section 5 - Why Choose Us
        5 => [
            'en' => [
                'name' => 'Why Choose BBC School Algeria',
                'description' => 'Discover what makes our school unique and exceptional.',
                'data' => json_encode([
                    'title' => 'Why Choose BBC School Algeria',
                    'subtitle' => 'Excellence & Innovation',
                    'content' => 'Discover what makes our school unique and exceptional.'
                ])
            ],
            'fr' => [
                'name' => 'Pourquoi Choisir BBC School Algeria',
                'description' => 'Découvrez ce qui rend notre école unique et exceptionnelle.',
                'data' => json_encode([
                    'title' => 'Pourquoi Choisir BBC School Algeria',
                    'subtitle' => 'Excellence et Innovation',
                    'content' => 'Découvrez ce qui rend notre école unique et exceptionnelle.'
                ])
            ],
            'ar' => [
                'name' => 'لماذا تختار مدرسة بي بي سي الجزائر',
                'description' => 'اكتشف ما يجعل مدرستنا فريدة واستثنائية.',
                'data' => json_encode([
                    'title' => 'لماذا تختار مدرسة بي بي سي الجزائر',
                    'subtitle' => 'التميز والابتكار',
                    'content' => 'اكتشف ما يجعل مدرستنا فريدة واستثنائية.'
                ])
            ]
        ],
        
        // Section 6 - Academic Curriculum
        6 => [
            'en' => [
                'name' => 'Academic Programs BBC School Algeria',
                'description' => 'Comprehensive educational programs designed for student success.',
                'data' => json_encode([
                    'title' => 'Academic Programs BBC School Algeria',
                    'subtitle' => 'Quality Education',
                    'content' => 'Comprehensive educational programs designed for student success.'
                ])
            ],
            'fr' => [
                'name' => 'Programmes Académiques BBC School Algeria',
                'description' => 'Programmes éducatifs complets conçus pour la réussite des étudiants.',
                'data' => json_encode([
                    'title' => 'Programmes Académiques BBC School Algeria',
                    'subtitle' => 'Éducation de Qualité',
                    'content' => 'Programmes éducatifs complets conçus pour la réussite des étudiants.'
                ])
            ],
            'ar' => [
                'name' => 'البرامج الأكاديمية مدرسة بي بي سي الجزائر',
                'description' => 'برامج تعليمية شاملة مصممة لنجاح الطلاب.',
                'data' => json_encode([
                    'title' => 'البرامج الأكاديمية مدرسة بي بي سي الجزائر',
                    'subtitle' => 'تعليم عالي الجودة',
                    'content' => 'برامج تعليمية شاملة مصممة لنجاح الطلاب.'
                ])
            ]
        ],
        
        // Section 7 - Coming Up
        7 => [
            'en' => [
                'name' => 'What\'s Coming Up?',
                'description' => 'Stay updated with upcoming events and activities.',
                'data' => json_encode([
                    'title' => 'What\'s Coming Up?',
                    'subtitle' => 'Upcoming Events',
                    'content' => 'Stay updated with upcoming events and activities.'
                ])
            ],
            'fr' => [
                'name' => 'Quoi de Neuf ?',
                'description' => 'Restez informé des événements et activités à venir.',
                'data' => json_encode([
                    'title' => 'Quoi de Neuf ?',
                    'subtitle' => 'Événements à Venir',
                    'content' => 'Restez informé des événements et activités à venir.'
                ])
            ],
            'ar' => [
                'name' => 'ما الجديد؟',
                'description' => 'ابق على اطلاع على الأحداث والأنشطة القادمة.',
                'data' => json_encode([
                    'title' => 'ما الجديد؟',
                    'subtitle' => 'الأحداث القادمة',
                    'content' => 'ابق على اطلاع على الأحداث والأنشطة القادمة.'
                ])
            ]
        ],
        
        // Section 8 - News
        8 => [
            'en' => [
                'name' => 'Latest From Our Blog',
                'description' => 'Read the latest news and updates from BBC School Algeria.',
                'data' => json_encode([
                    'title' => 'Latest From Our Blog',
                    'subtitle' => 'News & Updates',
                    'content' => 'Read the latest news and updates from BBC School Algeria.'
                ])
            ],
            'fr' => [
                'name' => 'Dernières de Notre Blog',
                'description' => 'Lisez les dernières nouvelles et mises à jour de BBC School Algeria.',
                'data' => json_encode([
                    'title' => 'Dernières de Notre Blog',
                    'subtitle' => 'Nouvelles et Mises à Jour',
                    'content' => 'Lisez les dernières nouvelles et mises à jour de BBC School Algeria.'
                ])
            ],
            'ar' => [
                'name' => 'آخر من مدونتنا',
                'description' => 'اقرأ آخر الأخبار والتحديثات من مدرسة بي بي سي الجزائر.',
                'data' => json_encode([
                    'title' => 'آخر من مدونتنا',
                    'subtitle' => 'الأخبار والتحديثات',
                    'content' => 'اقرأ آخر الأخبار والتحديثات من مدرسة بي بي سي الجزائر.'
                ])
            ]
        ],
        
        // Section 9 - Gallery
        9 => [
            'en' => [
                'name' => 'Our Gallery',
                'description' => 'Explore photos and videos from BBC School Algeria.',
                'data' => json_encode([
                    'title' => 'Our Gallery',
                    'subtitle' => 'Photos & Videos',
                    'content' => 'Explore photos and videos from BBC School Algeria.'
                ])
            ],
            'fr' => [
                'name' => 'Notre Galerie',
                'description' => 'Explorez les photos et vidéos de BBC School Algeria.',
                'data' => json_encode([
                    'title' => 'Notre Galerie',
                    'subtitle' => 'Photos et Vidéos',
                    'content' => 'Explorez les photos et vidéos de BBC School Algeria.'
                ])
            ],
            'ar' => [
                'name' => 'معرض الصور',
                'description' => 'استكشف الصور ومقاطع الفيديو من مدرسة بي بي سي الجزائر.',
                'data' => json_encode([
                    'title' => 'معرض الصور',
                    'subtitle' => 'الصور ومقاطع الفيديو',
                    'content' => 'استكشف الصور ومقاطع الفيديو من مدرسة بي بي سي الجزائر.'
                ])
            ]
        ],
        
        // Section 10 - Contact Information
        10 => [
            'en' => [
                'name' => 'Find Our Contact Information',
                'description' => 'Get in touch with BBC School Algeria.',
                'data' => json_encode([
                    'title' => 'Find Our <br> Contact Information',
                    'subtitle' => 'Get in Touch',
                    'content' => 'Get in touch with BBC School Algeria.'
                ])
            ],
            'fr' => [
                'name' => 'Trouvez Nos Informations de Contact',
                'description' => 'Contactez BBC School Algeria.',
                'data' => json_encode([
                    'title' => 'Trouvez Nos <br> Informations de Contact',
                    'subtitle' => 'Contactez-nous',
                    'content' => 'Contactez BBC School Algeria.'
                ])
            ],
            'ar' => [
                'name' => 'ابحث عن معلومات الاتصال',
                'description' => 'تواصل مع مدرسة بي بي سي الجزائر.',
                'data' => json_encode([
                    'title' => 'ابحث عن <br> معلومات الاتصال',
                    'subtitle' => 'تواصل معنا',
                    'content' => 'تواصل مع مدرسة بي بي سي الجزائر.'
                ])
            ]
        ],
        
        // Section 11 - Department Contact
        11 => [
            'en' => [
                'name' => 'Contact By Department',
                'description' => 'Contact specific departments at BBC School Algeria.',
                'data' => json_encode([
                    'title' => 'Contact By Department',
                    'subtitle' => 'Department Contacts',
                    'content' => 'Contact specific departments at BBC School Algeria.'
                ])
            ],
            'fr' => [
                'name' => 'Contact par Département',
                'description' => 'Contactez des départements spécifiques de BBC School Algeria.',
                'data' => json_encode([
                    'title' => 'Contact par Département',
                    'subtitle' => 'Contacts Départementaux',
                    'content' => 'Contactez des départements spécifiques de BBC School Algeria.'
                ])
            ],
            'ar' => [
                'name' => 'الاتصال حسب القسم',
                'description' => 'اتصل بأقسام محددة في مدرسة بي بي سي الجزائر.',
                'data' => json_encode([
                    'title' => 'الاتصال حسب القسم',
                    'subtitle' => 'جهات اتصال الأقسام',
                    'content' => 'اتصل بأقسام محددة في مدرسة بي بي سي الجزائر.'
                ])
            ]
        ],
        
        // Section 12 - Our Teachers
        12 => [
            'en' => [
                'name' => 'Our Featured Teachers',
                'description' => 'Meet our dedicated and qualified teachers.',
                'data' => json_encode([
                    'title' => 'Our Featured Teachers',
                    'subtitle' => 'Qualified Educators',
                    'content' => 'Meet our dedicated and qualified teachers.'
                ])
            ],
            'fr' => [
                'name' => 'Nos Enseignants Vedettes',
                'description' => 'Rencontrez nos enseignants dévoués et qualifiés.',
                'data' => json_encode([
                    'title' => 'Nos Enseignants Vedettes',
                    'subtitle' => 'Éducateurs Qualifiés',
                    'content' => 'Rencontrez nos enseignants dévoués et qualifiés.'
                ])
            ],
            'ar' => [
                'name' => 'معلمونا المميزون',
                'description' => 'تعرف على معلمينا المتفانيين والمؤهلين.',
                'data' => json_encode([
                    'title' => 'معلمونا المميزون',
                    'subtitle' => 'مربون مؤهلون',
                    'content' => 'تعرف على معلمينا المتفانيين والمؤهلين.'
                ])
            ]
        ]
    ];
    
    $updated_count = 0;
    
    foreach($translations as $section_id => $langs) {
        foreach($langs as $locale => $translation) {
            // Vérifier si la traduction existe déjà
            $existing = $pdo->prepare("SELECT id FROM section_translates WHERE section_id = ? AND locale = ?");
            $existing->execute([$section_id, $locale]);
            $exists = $existing->fetch();
            
            if($exists) {
                // Mettre à jour
                $update = $pdo->prepare("
                    UPDATE section_translates 
                    SET name = ?, description = ?, data = ?, updated_at = NOW()
                    WHERE section_id = ? AND locale = ?
                ");
                $update->execute([
                    $translation['name'],
                    $translation['description'],
                    $translation['data'],
                    $section_id,
                    $locale
                ]);
                echo "✅ Mis à jour section $section_id ($locale): " . $translation['name'] . PHP_EOL;
            } else {
                // Insérer nouvelle traduction
                $insert = $pdo->prepare("
                    INSERT INTO section_translates (section_id, locale, name, description, data, created_at, updated_at, branch_id)
                    VALUES (?, ?, ?, ?, ?, NOW(), NOW(), 1)
                ");
                $insert->execute([
                    $section_id,
                    $locale,
                    $translation['name'],
                    $translation['description'],
                    $translation['data']
                ]);
                echo "✅ Ajouté section $section_id ($locale): " . $translation['name'] . PHP_EOL;
            }
            $updated_count++;
        }
    }
    
    echo PHP_EOL . "🎉 Correction terminée ! $updated_count traductions traitées." . PHP_EOL;
    echo "📊 Vérification des langues disponibles:" . PHP_EOL;
    
    // Vérification finale
    $verification = $pdo->query("
        SELECT s.id as section_id, st.locale, st.name
        FROM sections s
        LEFT JOIN section_translates st ON s.id = st.section_id
        ORDER BY s.id, st.locale
    ")->fetchAll();
    
    $section_stats = [];
    foreach($verification as $v) {
        $section_stats[$v['section_id']][$v['locale']] = $v['name'];
    }
    
    foreach($section_stats as $section_id => $locales) {
        $available_langs = array_keys(array_filter($locales));
        echo "Section $section_id: " . implode(', ', $available_langs) . PHP_EOL;
    }
    
} catch(Exception $e) {
    echo "❌ Erreur: " . $e->getMessage() . PHP_EOL;
}
?>