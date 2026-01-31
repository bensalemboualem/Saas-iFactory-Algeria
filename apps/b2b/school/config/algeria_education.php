<?php

/**
 * Configuration du Système Éducatif Algérien
 *
 * Conforme au programme du Ministère de l'Éducation Nationale
 */

return [

    /*
    |--------------------------------------------------------------------------
    | Cycles et Niveaux
    |--------------------------------------------------------------------------
    */
    'cycles' => [
        'primaire' => [
            'name' => 'Enseignement Primaire',
            'name_ar' => 'التعليم الابتدائي',
            'duration' => 5,
            'levels' => [
                '1AP' => ['name' => '1ère Année Primaire', 'name_ar' => 'السنة الأولى ابتدائي', 'order' => 1],
                '2AP' => ['name' => '2ème Année Primaire', 'name_ar' => 'السنة الثانية ابتدائي', 'order' => 2],
                '3AP' => ['name' => '3ème Année Primaire', 'name_ar' => 'السنة الثالثة ابتدائي', 'order' => 3],
                '4AP' => ['name' => '4ème Année Primaire', 'name_ar' => 'السنة الرابعة ابتدائي', 'order' => 4],
                '5AP' => ['name' => '5ème Année Primaire', 'name_ar' => 'السنة الخامسة ابتدائي', 'order' => 5],
            ],
        ],
        'moyen' => [
            'name' => 'Enseignement Moyen',
            'name_ar' => 'التعليم المتوسط',
            'duration' => 4,
            'levels' => [
                '1AM' => ['name' => '1ère Année Moyenne', 'name_ar' => 'السنة الأولى متوسط', 'order' => 6],
                '2AM' => ['name' => '2ème Année Moyenne', 'name_ar' => 'السنة الثانية متوسط', 'order' => 7],
                '3AM' => ['name' => '3ème Année Moyenne', 'name_ar' => 'السنة الثالثة متوسط', 'order' => 8],
                '4AM' => ['name' => '4ème Année Moyenne', 'name_ar' => 'السنة الرابعة متوسط', 'order' => 9],
            ],
        ],
        'secondaire' => [
            'name' => 'Enseignement Secondaire',
            'name_ar' => 'التعليم الثانوي',
            'duration' => 3,
            'levels' => [
                '1AS' => ['name' => '1ère Année Secondaire', 'name_ar' => 'السنة الأولى ثانوي', 'order' => 10],
                '2AS' => ['name' => '2ème Année Secondaire', 'name_ar' => 'السنة الثانية ثانوي', 'order' => 11],
                '3AS' => ['name' => '3ème Année Secondaire', 'name_ar' => 'السنة الثالثة ثانوي', 'order' => 12],
            ],
        ],
    ],

    /*
    |--------------------------------------------------------------------------
    | Filières Secondaire
    |--------------------------------------------------------------------------
    */
    'filieres' => [
        'sciences' => ['name' => 'Sciences Expérimentales', 'name_ar' => 'علوم تجريبية'],
        'maths' => ['name' => 'Mathématiques', 'name_ar' => 'رياضيات'],
        'tech_maths' => ['name' => 'Technique Mathématiques', 'name_ar' => 'تقني رياضي'],
        'gestion' => ['name' => 'Gestion et Économie', 'name_ar' => 'تسيير واقتصاد'],
        'lettres' => ['name' => 'Lettres et Philosophie', 'name_ar' => 'آداب وفلسفة'],
        'langues' => ['name' => 'Langues Étrangères', 'name_ar' => 'لغات أجنبية'],
    ],

    /*
    |--------------------------------------------------------------------------
    | Matières par Cycle
    |--------------------------------------------------------------------------
    */
    'subjects' => [
        'primaire' => [
            ['code' => 'ARB', 'name' => 'Langue Arabe', 'name_ar' => 'اللغة العربية', 'coefficient' => 3],
            ['code' => 'FRA', 'name' => 'Langue Française', 'name_ar' => 'اللغة الفرنسية', 'coefficient' => 2],
            ['code' => 'MAT', 'name' => 'Mathématiques', 'name_ar' => 'الرياضيات', 'coefficient' => 2],
            ['code' => 'AMA', 'name' => 'Tamazight', 'name_ar' => 'اللغة الأمازيغية', 'coefficient' => 1],
            ['code' => 'SCI', 'name' => 'Éveil Scientifique', 'name_ar' => 'التربية العلمية', 'coefficient' => 1],
            ['code' => 'ISL', 'name' => 'Éducation Islamique', 'name_ar' => 'التربية الإسلامية', 'coefficient' => 1],
            ['code' => 'CIV', 'name' => 'Éducation Civique', 'name_ar' => 'التربية المدنية', 'coefficient' => 1],
            ['code' => 'HIS', 'name' => 'Histoire', 'name_ar' => 'التاريخ', 'coefficient' => 1],
            ['code' => 'GEO', 'name' => 'Géographie', 'name_ar' => 'الجغرافيا', 'coefficient' => 1],
            ['code' => 'ART', 'name' => 'Éducation Artistique', 'name_ar' => 'التربية الفنية', 'coefficient' => 1],
            ['code' => 'MUS', 'name' => 'Éducation Musicale', 'name_ar' => 'التربية الموسيقية', 'coefficient' => 1],
            ['code' => 'EPS', 'name' => 'Éducation Physique', 'name_ar' => 'التربية البدنية', 'coefficient' => 1],
        ],
        'moyen' => [
            ['code' => 'ARB', 'name' => 'Langue Arabe', 'name_ar' => 'اللغة العربية', 'coefficient' => 3],
            ['code' => 'FRA', 'name' => 'Langue Française', 'name_ar' => 'اللغة الفرنسية', 'coefficient' => 2],
            ['code' => 'ANG', 'name' => 'Langue Anglaise', 'name_ar' => 'اللغة الإنجليزية', 'coefficient' => 2],
            ['code' => 'MAT', 'name' => 'Mathématiques', 'name_ar' => 'الرياضيات', 'coefficient' => 3],
            ['code' => 'AMA', 'name' => 'Tamazight', 'name_ar' => 'اللغة الأمازيغية', 'coefficient' => 1],
            ['code' => 'PHY', 'name' => 'Sciences Physiques', 'name_ar' => 'العلوم الفيزيائية', 'coefficient' => 2],
            ['code' => 'SVT', 'name' => 'Sciences Naturelles', 'name_ar' => 'علوم الطبيعة والحياة', 'coefficient' => 2],
            ['code' => 'ISL', 'name' => 'Éducation Islamique', 'name_ar' => 'التربية الإسلامية', 'coefficient' => 1],
            ['code' => 'CIV', 'name' => 'Éducation Civique', 'name_ar' => 'التربية المدنية', 'coefficient' => 1],
            ['code' => 'HIS', 'name' => 'Histoire', 'name_ar' => 'التاريخ', 'coefficient' => 1],
            ['code' => 'GEO', 'name' => 'Géographie', 'name_ar' => 'الجغرافيا', 'coefficient' => 1],
            ['code' => 'INF', 'name' => 'Informatique', 'name_ar' => 'الإعلام الآلي', 'coefficient' => 1],
            ['code' => 'EPS', 'name' => 'Éducation Physique', 'name_ar' => 'التربية البدنية', 'coefficient' => 1],
        ],
        'secondaire' => [
            ['code' => 'ARB', 'name' => 'Langue Arabe', 'name_ar' => 'اللغة العربية', 'coefficient' => 3],
            ['code' => 'FRA', 'name' => 'Langue Française', 'name_ar' => 'اللغة الفرنسية', 'coefficient' => 2],
            ['code' => 'ANG', 'name' => 'Langue Anglaise', 'name_ar' => 'اللغة الإنجليزية', 'coefficient' => 2],
            ['code' => 'MAT', 'name' => 'Mathématiques', 'name_ar' => 'الرياضيات', 'coefficient' => 4],
            ['code' => 'PHY', 'name' => 'Sciences Physiques', 'name_ar' => 'العلوم الفيزيائية', 'coefficient' => 3],
            ['code' => 'SVT', 'name' => 'Sciences Naturelles', 'name_ar' => 'علوم الطبيعة والحياة', 'coefficient' => 3],
            ['code' => 'PHI', 'name' => 'Philosophie', 'name_ar' => 'الفلسفة', 'coefficient' => 2],
            ['code' => 'ISL', 'name' => 'Sciences Islamiques', 'name_ar' => 'العلوم الإسلامية', 'coefficient' => 1],
            ['code' => 'HIS', 'name' => 'Histoire', 'name_ar' => 'التاريخ', 'coefficient' => 2],
            ['code' => 'GEO', 'name' => 'Géographie', 'name_ar' => 'الجغرافيا', 'coefficient' => 2],
            ['code' => 'INF', 'name' => 'Informatique', 'name_ar' => 'الإعلام الآلي', 'coefficient' => 2],
            ['code' => 'EPS', 'name' => 'Éducation Physique', 'name_ar' => 'التربية البدنية', 'coefficient' => 1],
        ],
    ],

    /*
    |--------------------------------------------------------------------------
    | Système de Notation (0-20)
    |--------------------------------------------------------------------------
    */
    'grading' => [
        'max_score' => 20,
        'pass_score' => 10,
        'grades' => [
            ['min' => 16, 'max' => 20, 'grade' => 'Excellent', 'grade_ar' => 'ممتاز', 'color' => '#28a745'],
            ['min' => 14, 'max' => 15.99, 'grade' => 'Très Bien', 'grade_ar' => 'جيد جدا', 'color' => '#20c997'],
            ['min' => 12, 'max' => 13.99, 'grade' => 'Bien', 'grade_ar' => 'جيد', 'color' => '#17a2b8'],
            ['min' => 10, 'max' => 11.99, 'grade' => 'Assez Bien', 'grade_ar' => 'حسن', 'color' => '#ffc107'],
            ['min' => 0, 'max' => 9.99, 'grade' => 'Insuffisant', 'grade_ar' => 'ضعيف', 'color' => '#dc3545'],
        ],
    ],

    /*
    |--------------------------------------------------------------------------
    | Trimestres
    |--------------------------------------------------------------------------
    */
    'trimesters' => [
        1 => ['name' => '1er Trimestre', 'name_ar' => 'الفصل الأول', 'start' => 'September', 'end' => 'December'],
        2 => ['name' => '2ème Trimestre', 'name_ar' => 'الفصل الثاني', 'start' => 'January', 'end' => 'March'],
        3 => ['name' => '3ème Trimestre', 'name_ar' => 'الفصل الثالث', 'start' => 'April', 'end' => 'June'],
    ],

    /*
    |--------------------------------------------------------------------------
    | Examens Nationaux
    |--------------------------------------------------------------------------
    */
    'national_exams' => [
        'bem' => [
            'name' => 'Brevet d\'Enseignement Moyen (BEM)',
            'name_ar' => 'شهادة التعليم المتوسط',
            'level' => '4AM',
            'period' => 'June',
        ],
        'bac' => [
            'name' => 'Baccalauréat',
            'name_ar' => 'شهادة البكالوريا',
            'level' => '3AS',
            'period' => 'June',
        ],
    ],

    /*
    |--------------------------------------------------------------------------
    | Jours Fériés Algériens
    |--------------------------------------------------------------------------
    */
    'holidays' => [
        ['name' => 'Jour de l\'An', 'name_ar' => 'رأس السنة الميلادية', 'date' => '01-01', 'type' => 'fixed'],
        ['name' => 'Fête du Travail', 'name_ar' => 'عيد العمال', 'date' => '05-01', 'type' => 'fixed'],
        ['name' => 'Fête de l\'Indépendance', 'name_ar' => 'عيد الاستقلال', 'date' => '07-05', 'type' => 'fixed'],
        ['name' => 'Fête de la Révolution', 'name_ar' => 'عيد الثورة', 'date' => '11-01', 'type' => 'fixed'],
        ['name' => 'Aïd El Fitr', 'name_ar' => 'عيد الفطر', 'date' => 'variable', 'type' => 'islamic', 'days' => 2],
        ['name' => 'Aïd El Adha', 'name_ar' => 'عيد الأضحى', 'date' => 'variable', 'type' => 'islamic', 'days' => 2],
        ['name' => 'Achoura', 'name_ar' => 'عاشوراء', 'date' => 'variable', 'type' => 'islamic', 'days' => 1],
        ['name' => 'Mawlid Ennabawi', 'name_ar' => 'المولد النبوي الشريف', 'date' => 'variable', 'type' => 'islamic', 'days' => 1],
    ],

    /*
    |--------------------------------------------------------------------------
    | Vacances Scolaires
    |--------------------------------------------------------------------------
    */
    'school_vacations' => [
        ['name' => 'Vacances d\'Automne', 'name_ar' => 'عطلة الخريف', 'duration' => '1 week', 'period' => 'October/November'],
        ['name' => 'Vacances d\'Hiver', 'name_ar' => 'عطلة الشتاء', 'duration' => '2 weeks', 'period' => 'December/January'],
        ['name' => 'Vacances de Printemps', 'name_ar' => 'عطلة الربيع', 'duration' => '2 weeks', 'period' => 'March/April'],
        ['name' => 'Vacances d\'Été', 'name_ar' => 'عطلة الصيف', 'duration' => '3 months', 'period' => 'June-September'],
    ],

    /*
    |--------------------------------------------------------------------------
    | Monnaie et Tarifs
    |--------------------------------------------------------------------------
    */
    'currency' => [
        'code' => 'DZD',
        'symbol' => 'DA',
        'name' => 'Dinar Algérien',
        'name_ar' => 'دينار جزائري',
        'decimal_places' => 2,
    ],

    /*
    |--------------------------------------------------------------------------
    | Wilayas (pour multi-branch)
    |--------------------------------------------------------------------------
    */
    'wilayas' => [
        '01' => 'Adrar', '02' => 'Chlef', '03' => 'Laghouat', '04' => 'Oum El Bouaghi',
        '05' => 'Batna', '06' => 'Béjaïa', '07' => 'Biskra', '08' => 'Béchar',
        '09' => 'Blida', '10' => 'Bouira', '11' => 'Tamanrasset', '12' => 'Tébessa',
        '13' => 'Tlemcen', '14' => 'Tiaret', '15' => 'Tizi Ouzou', '16' => 'Alger',
        '17' => 'Djelfa', '18' => 'Jijel', '19' => 'Sétif', '20' => 'Saïda',
        '21' => 'Skikda', '22' => 'Sidi Bel Abbès', '23' => 'Annaba', '24' => 'Guelma',
        '25' => 'Constantine', '26' => 'Médéa', '27' => 'Mostaganem', '28' => 'M\'Sila',
        '29' => 'Mascara', '30' => 'Ouargla', '31' => 'Oran', '32' => 'El Bayadh',
        '33' => 'Illizi', '34' => 'Bordj Bou Arréridj', '35' => 'Boumerdès', '36' => 'El Tarf',
        '37' => 'Tindouf', '38' => 'Tissemsilt', '39' => 'El Oued', '40' => 'Khenchela',
        '41' => 'Souk Ahras', '42' => 'Tipaza', '43' => 'Mila', '44' => 'Aïn Defla',
        '45' => 'Naâma', '46' => 'Aïn Témouchent', '47' => 'Ghardaïa', '48' => 'Relizane',
        '49' => 'El M\'Ghair', '50' => 'El Menia', '51' => 'Ouled Djellal', '52' => 'Bordj Badji Mokhtar',
        '53' => 'Béni Abbès', '54' => 'Timimoun', '55' => 'Touggourt', '56' => 'Djanet',
        '57' => 'In Salah', '58' => 'In Guezzam',
    ],

    /*
    |--------------------------------------------------------------------------
    | Langues Officielles
    |--------------------------------------------------------------------------
    */
    'languages' => [
        'ar' => ['name' => 'Arabe', 'name_ar' => 'العربية', 'direction' => 'rtl', 'official' => true],
        'fr' => ['name' => 'Français', 'name_ar' => 'الفرنسية', 'direction' => 'ltr', 'official' => false],
        'ber' => ['name' => 'Amazigh', 'name_ar' => 'الأمازيغية', 'direction' => 'ltr', 'official' => true],
        'en' => ['name' => 'Anglais', 'name_ar' => 'الإنجليزية', 'direction' => 'ltr', 'official' => false],
    ],
];
