import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '../i18n';

type Theme = 'dark' | 'light';

interface Agent {
  id: string;
  name: string;
  icon: string;
  description: string;
  capabilities: string[];
  category: string;
}

// Données des agents par langue
const agentsData: Record<string, Agent[]> = {
  fr: [
    // ===== BUSINESS =====
    { id: 'business-consultant', name: 'Consultant Business', icon: '💼', description: 'Stratégie d\'entreprise, études de marché et plans d\'affaires', capabilities: ['Études de marché', 'Business plans', 'Analyse concurrentielle', 'Stratégie croissance'], category: 'Business' },
    { id: 'marketing-expert', name: 'Expert Marketing', icon: '📣', description: 'Stratégies marketing digital et campagnes publicitaires', capabilities: ['SEO/SEM', 'Social Media', 'Content Marketing', 'Publicité'], category: 'Business' },
    { id: 'sales-coach', name: 'Coach Commercial', icon: '🎯', description: 'Techniques de vente et négociation commerciale', capabilities: ['Prospection', 'Négociation', 'Closing', 'CRM'], category: 'Business' },
    { id: 'startup-advisor', name: 'Conseiller Startup', icon: '🚀', description: 'Accompagnement création et développement startup', capabilities: ['Pitch deck', 'Levée de fonds', 'MVP', 'Growth hacking'], category: 'Business' },
    // ===== FINANCE =====
    { id: 'finance-analyst', name: 'Analyste Finance', icon: '📈', description: 'Analyse financière, comptabilité et gestion de trésorerie', capabilities: ['Bilan comptable', 'Déclarations fiscales', 'Trésorerie', 'Ratios financiers'], category: 'Finance' },
    { id: 'tax-advisor', name: 'Conseiller Fiscal', icon: '💵', description: 'Optimisation fiscale et déclarations d\'impôts', capabilities: ['IRG/IBS', 'TVA', 'Optimisation', 'Déclarations'], category: 'Finance' },
    { id: 'investment-advisor', name: 'Conseiller Investissement', icon: '💰', description: 'Stratégies d\'investissement et gestion de patrimoine', capabilities: ['Actions', 'Immobilier', 'Crypto', 'Diversification'], category: 'Finance' },
    { id: 'budget-planner', name: 'Planificateur Budget', icon: '📊', description: 'Gestion budgétaire personnelle et professionnelle', capabilities: ['Budget mensuel', 'Épargne', 'Dépenses', 'Prévisions'], category: 'Finance' },
    // ===== JURIDIQUE =====
    { id: 'legal-advisor', name: 'Conseiller Juridique', icon: '⚖️', description: 'Conseil juridique et rédaction de contrats', capabilities: ['Contrats', 'Conseils légaux', 'Veille juridique', 'Litiges'], category: 'Juridique' },
    { id: 'contract-specialist', name: 'Spécialiste Contrats', icon: '📜', description: 'Rédaction et analyse de contrats commerciaux', capabilities: ['NDA', 'CGV/CGU', 'Contrats travail', 'Partenariats'], category: 'Juridique' },
    { id: 'ip-lawyer', name: 'Expert Propriété Intellectuelle', icon: '®️', description: 'Protection marques, brevets et droits d\'auteur', capabilities: ['Marques', 'Brevets', 'Copyright', 'Licences'], category: 'Juridique' },
    { id: 'gdpr-expert', name: 'Expert RGPD', icon: '🔒', description: 'Conformité protection des données personnelles', capabilities: ['Audit RGPD', 'Politique confidentialité', 'DPO', 'Registre'], category: 'Juridique' },
    // ===== ÉDUCATION =====
    { id: 'tutor-general', name: 'Tuteur Général', icon: '🎓', description: 'Aide aux devoirs et cours particuliers tous niveaux', capabilities: ['Cours personnalisés', 'Exercices', 'Prépa examens', 'Méthodologie'], category: 'Éducation' },
    { id: 'bac-coach', name: 'Coach BAC', icon: '📚', description: 'Préparation intensive au baccalauréat algérien', capabilities: ['Révisions', 'Annales', 'Fiches', 'Simulations'], category: 'Éducation' },
    { id: 'bem-coach', name: 'Coach BEM', icon: '📝', description: 'Préparation au Brevet d\'Enseignement Moyen', capabilities: ['Maths', 'Français', 'Arabe', 'Sciences'], category: 'Éducation' },
    { id: 'language-teacher', name: 'Prof de Langues', icon: '🌍', description: 'Apprentissage des langues étrangères', capabilities: ['Anglais', 'Français', 'Espagnol', 'Allemand'], category: 'Éducation' },
    { id: 'math-tutor', name: 'Tuteur Maths', icon: '🔢', description: 'Mathématiques tous niveaux', capabilities: ['Algèbre', 'Géométrie', 'Analyse', 'Statistiques'], category: 'Éducation' },
    { id: 'science-tutor', name: 'Tuteur Sciences', icon: '🔬', description: 'Physique, Chimie et Sciences naturelles', capabilities: ['Physique', 'Chimie', 'SVT', 'Expériences'], category: 'Éducation' },
    // ===== ADMINISTRATION ALGÉRIE =====
    { id: 'cnas-agent', name: 'Agent CNAS', icon: '🏥', description: 'Guide complet pour les démarches CNAS', capabilities: ['Affiliation', 'Remboursements', 'Arrêts maladie', 'Maternité'], category: 'Admin DZ' },
    { id: 'casnos-agent', name: 'Agent CASNOS', icon: '👷', description: 'Aide pour les travailleurs non-salariés', capabilities: ['Cotisations', 'Retraite', 'Couverture santé', 'Déclarations'], category: 'Admin DZ' },
    { id: 'cnrc-agent', name: 'Agent CNRC', icon: '📋', description: 'Registre du commerce et création d\'entreprise', capabilities: ['Immatriculation', 'Modifications', 'Radiation', 'Attestations'], category: 'Admin DZ' },
    { id: 'impots-agent', name: 'Agent Impôts', icon: '🏛️', description: 'Déclarations fiscales et taxes', capabilities: ['G50', 'IRG', 'IBS', 'TAP'], category: 'Admin DZ' },
    { id: 'douanes-agent', name: 'Agent Douanes', icon: '🛃', description: 'Procédures d\'import/export', capabilities: ['Dédouanement', 'Tarifs', 'Documents', 'Franchise'], category: 'Admin DZ' },
    { id: 'anem-agent', name: 'Agent ANEM', icon: '💼', description: 'Aide à l\'emploi et recherche de travail', capabilities: ['Offres emploi', 'CV', 'Formation', 'DAIP'], category: 'Admin DZ' },
    { id: 'ansej-agent', name: 'Agent ANADE', icon: '🚀', description: 'Création d\'entreprise pour jeunes', capabilities: ['Dossier', 'Financement', 'Accompagnement', 'Avantages'], category: 'Admin DZ' },
    { id: 'passport-agent', name: 'Agent Passeport', icon: '🛂', description: 'Demande de passeport biométrique', capabilities: ['Documents', 'Rendez-vous', 'Renouvellement', 'Urgence'], category: 'Admin DZ' },
    // ===== TECHNIQUE =====
    { id: 'dev-assistant', name: 'Assistant Développeur', icon: '💻', description: 'Aide au développement et debugging', capabilities: ['Code review', 'Debug', 'Architecture', 'Best practices'], category: 'Tech' },
    { id: 'devops-expert', name: 'Expert DevOps', icon: '🔧', description: 'CI/CD, cloud et infrastructure', capabilities: ['Docker', 'Kubernetes', 'AWS/GCP', 'Terraform'], category: 'Tech' },
    { id: 'data-scientist', name: 'Data Scientist', icon: '📊', description: 'Analyse de données et machine learning', capabilities: ['Python', 'ML/AI', 'Visualisation', 'Big Data'], category: 'Tech' },
    { id: 'cybersecurity', name: 'Expert Cybersécurité', icon: '🔐', description: 'Sécurité informatique et audit', capabilities: ['Audit', 'Pentest', 'SIEM', 'Compliance'], category: 'Tech' },
    // ===== CRÉATIF =====
    { id: 'content-creator', name: 'Créateur de Contenu', icon: '✍️', description: 'Rédaction web, blogs et réseaux sociaux', capabilities: ['Articles', 'Posts sociaux', 'Scripts', 'Newsletters'], category: 'Créatif' },
    { id: 'copywriter', name: 'Copywriter', icon: '📝', description: 'Textes publicitaires et pages de vente', capabilities: ['Landing pages', 'Emails', 'Slogans', 'Storytelling'], category: 'Créatif' },
    { id: 'seo-expert', name: 'Expert SEO', icon: '🔍', description: 'Optimisation pour les moteurs de recherche', capabilities: ['Mots-clés', 'Backlinks', 'Technique', 'Contenu'], category: 'Créatif' },
    { id: 'social-manager', name: 'Community Manager', icon: '📱', description: 'Gestion des réseaux sociaux', capabilities: ['Planning', 'Engagement', 'Modération', 'Analytics'], category: 'Créatif' },
    // ===== SANTÉ & BIEN-ÊTRE =====
    { id: 'health-advisor', name: 'Conseiller Santé', icon: '🏥', description: 'Conseils santé et bien-être général', capabilities: ['Prévention', 'Nutrition', 'Sommeil', 'Exercice'], category: 'Santé' },
    { id: 'nutrition-coach', name: 'Coach Nutrition', icon: '🥗', description: 'Plans alimentaires et conseils nutritionnels', capabilities: ['Régimes', 'Menus', 'Compléments', 'Allergies'], category: 'Santé' },
    { id: 'fitness-coach', name: 'Coach Fitness', icon: '💪', description: 'Programmes d\'entraînement personnalisés', capabilities: ['Musculation', 'Cardio', 'Stretching', 'HIIT'], category: 'Santé' },
    { id: 'mental-coach', name: 'Coach Mental', icon: '🧘', description: 'Gestion du stress et développement personnel', capabilities: ['Méditation', 'Productivité', 'Confiance', 'Motivation'], category: 'Santé' },
    // ===== SUPPORT =====
    { id: 'customer-support', name: 'Support Client', icon: '🎧', description: 'Assistance client et résolution de problèmes', capabilities: ['FAQ', 'Réclamations', 'Suivi', 'Satisfaction'], category: 'Support' },
    { id: 'tech-support', name: 'Support Technique', icon: '🔧', description: 'Aide technique et dépannage', capabilities: ['Diagnostic', 'Installation', 'Configuration', 'Maintenance'], category: 'Support' },
    { id: 'hr-assistant', name: 'Assistant RH', icon: '👥', description: 'Ressources humaines et recrutement', capabilities: ['Recrutement', 'Onboarding', 'Formation', 'Paie'], category: 'Support' },
    { id: 'project-manager', name: 'Chef de Projet', icon: '📋', description: 'Gestion de projet et méthodologies agiles', capabilities: ['Planning', 'Scrum', 'Kanban', 'Reporting'], category: 'Support' },
  ],
  ar: [
    // ===== الأعمال =====
    { id: 'business-consultant', name: 'مستشار الأعمال', icon: '💼', description: 'استراتيجية المؤسسات ودراسات السوق وخطط الأعمال', capabilities: ['دراسات السوق', 'خطط الأعمال', 'تحليل المنافسة', 'استراتيجية النمو'], category: 'الأعمال' },
    { id: 'marketing-expert', name: 'خبير التسويق', icon: '📣', description: 'استراتيجيات التسويق الرقمي والحملات الإعلانية', capabilities: ['تحسين محركات البحث', 'وسائل التواصل', 'تسويق المحتوى', 'الإعلان'], category: 'الأعمال' },
    { id: 'sales-coach', name: 'مدرب المبيعات', icon: '🎯', description: 'تقنيات البيع والتفاوض التجاري', capabilities: ['التنقيب', 'التفاوض', 'إغلاق الصفقات', 'إدارة العملاء'], category: 'الأعمال' },
    { id: 'startup-advisor', name: 'مستشار الشركات الناشئة', icon: '🚀', description: 'مرافقة إنشاء وتطوير الشركات الناشئة', capabilities: ['عرض المشروع', 'جمع التمويل', 'المنتج الأولي', 'النمو السريع'], category: 'الأعمال' },
    // ===== المالية =====
    { id: 'finance-analyst', name: 'محلل مالي', icon: '📈', description: 'التحليل المالي والمحاسبة وإدارة الخزينة', capabilities: ['الميزانية', 'التصريحات الضريبية', 'الخزينة', 'النسب المالية'], category: 'المالية' },
    { id: 'tax-advisor', name: 'مستشار ضريبي', icon: '💵', description: 'التحسين الضريبي والتصريحات الضريبية', capabilities: ['الضريبة على الدخل', 'الرسم على القيمة المضافة', 'التحسين', 'التصريحات'], category: 'المالية' },
    { id: 'investment-advisor', name: 'مستشار الاستثمار', icon: '💰', description: 'استراتيجيات الاستثمار وإدارة الثروة', capabilities: ['الأسهم', 'العقارات', 'العملات الرقمية', 'التنويع'], category: 'المالية' },
    { id: 'budget-planner', name: 'مخطط الميزانية', icon: '📊', description: 'إدارة الميزانية الشخصية والمهنية', capabilities: ['الميزانية الشهرية', 'الادخار', 'المصاريف', 'التوقعات'], category: 'المالية' },
    // ===== القانون =====
    { id: 'legal-advisor', name: 'مستشار قانوني', icon: '⚖️', description: 'الاستشارة القانونية وصياغة العقود', capabilities: ['العقود', 'النصائح القانونية', 'المتابعة القانونية', 'النزاعات'], category: 'القانون' },
    { id: 'contract-specialist', name: 'متخصص العقود', icon: '📜', description: 'صياغة وتحليل العقود التجارية', capabilities: ['اتفاقية السرية', 'الشروط العامة', 'عقود العمل', 'الشراكات'], category: 'القانون' },
    { id: 'ip-lawyer', name: 'خبير الملكية الفكرية', icon: '®️', description: 'حماية العلامات التجارية وبراءات الاختراع وحقوق المؤلف', capabilities: ['العلامات التجارية', 'براءات الاختراع', 'حقوق النشر', 'التراخيص'], category: 'القانون' },
    { id: 'gdpr-expert', name: 'خبير حماية البيانات', icon: '🔒', description: 'الامتثال لحماية البيانات الشخصية', capabilities: ['تدقيق حماية البيانات', 'سياسة الخصوصية', 'مسؤول البيانات', 'السجل'], category: 'القانون' },
    // ===== التعليم =====
    { id: 'tutor-general', name: 'معلم خصوصي', icon: '🎓', description: 'المساعدة في الواجبات والدروس الخصوصية لجميع المستويات', capabilities: ['دروس مخصصة', 'تمارين', 'تحضير الامتحانات', 'المنهجية'], category: 'التعليم' },
    { id: 'bac-coach', name: 'مدرب البكالوريا', icon: '📚', description: 'التحضير المكثف لشهادة البكالوريا الجزائرية', capabilities: ['المراجعات', 'المواضيع السابقة', 'الملخصات', 'المحاكاة'], category: 'التعليم' },
    { id: 'bem-coach', name: 'مدرب شهادة التعليم المتوسط', icon: '📝', description: 'التحضير لشهادة التعليم المتوسط', capabilities: ['الرياضيات', 'الفرنسية', 'العربية', 'العلوم'], category: 'التعليم' },
    { id: 'language-teacher', name: 'أستاذ اللغات', icon: '🌍', description: 'تعلم اللغات الأجنبية', capabilities: ['الإنجليزية', 'الفرنسية', 'الإسبانية', 'الألمانية'], category: 'التعليم' },
    { id: 'math-tutor', name: 'معلم الرياضيات', icon: '🔢', description: 'الرياضيات لجميع المستويات', capabilities: ['الجبر', 'الهندسة', 'التحليل', 'الإحصاء'], category: 'التعليم' },
    { id: 'science-tutor', name: 'معلم العلوم', icon: '🔬', description: 'الفيزياء والكيمياء والعلوم الطبيعية', capabilities: ['الفيزياء', 'الكيمياء', 'علوم الطبيعة', 'التجارب'], category: 'التعليم' },
    // ===== الإدارة الجزائرية =====
    { id: 'cnas-agent', name: 'وكيل الضمان الاجتماعي', icon: '🏥', description: 'دليل شامل لإجراءات الصندوق الوطني للتأمينات الاجتماعية', capabilities: ['الانتساب', 'التعويضات', 'الإجازات المرضية', 'الأمومة'], category: 'الإدارة الجزائرية' },
    { id: 'casnos-agent', name: 'وكيل صندوق غير الأجراء', icon: '👷', description: 'مساعدة للعمال غير الأجراء', capabilities: ['الاشتراكات', 'التقاعد', 'التغطية الصحية', 'التصريحات'], category: 'الإدارة الجزائرية' },
    { id: 'cnrc-agent', name: 'وكيل السجل التجاري', icon: '📋', description: 'السجل التجاري وإنشاء المؤسسات', capabilities: ['التسجيل', 'التعديلات', 'الشطب', 'الشهادات'], category: 'الإدارة الجزائرية' },
    { id: 'impots-agent', name: 'وكيل الضرائب', icon: '🏛️', description: 'التصريحات الضريبية والرسوم', capabilities: ['G50', 'الضريبة على الدخل', 'الضريبة على الأرباح', 'الرسم على النشاط'], category: 'الإدارة الجزائرية' },
    { id: 'douanes-agent', name: 'وكيل الجمارك', icon: '🛃', description: 'إجراءات الاستيراد والتصدير', capabilities: ['التخليص الجمركي', 'التعريفات', 'الوثائق', 'الإعفاءات'], category: 'الإدارة الجزائرية' },
    { id: 'anem-agent', name: 'وكيل الوكالة الوطنية للتشغيل', icon: '💼', description: 'المساعدة في التوظيف والبحث عن عمل', capabilities: ['عروض العمل', 'السيرة الذاتية', 'التكوين', 'عقود الإدماج'], category: 'الإدارة الجزائرية' },
    { id: 'ansej-agent', name: 'وكيل الوكالة الوطنية لدعم الشباب', icon: '🚀', description: 'إنشاء المؤسسات للشباب', capabilities: ['الملف', 'التمويل', 'المرافقة', 'الامتيازات'], category: 'الإدارة الجزائرية' },
    { id: 'passport-agent', name: 'وكيل جواز السفر', icon: '🛂', description: 'طلب جواز السفر البيومتري', capabilities: ['الوثائق', 'المواعيد', 'التجديد', 'الاستعجال'], category: 'الإدارة الجزائرية' },
    // ===== التقنية =====
    { id: 'dev-assistant', name: 'مساعد المطور', icon: '💻', description: 'المساعدة في التطوير وإصلاح الأخطاء', capabilities: ['مراجعة الكود', 'إصلاح الأخطاء', 'الهندسة', 'أفضل الممارسات'], category: 'التقنية' },
    { id: 'devops-expert', name: 'خبير DevOps', icon: '🔧', description: 'التكامل والنشر المستمر والبنية التحتية السحابية', capabilities: ['Docker', 'Kubernetes', 'AWS/GCP', 'Terraform'], category: 'التقنية' },
    { id: 'data-scientist', name: 'عالم البيانات', icon: '📊', description: 'تحليل البيانات والتعلم الآلي', capabilities: ['Python', 'الذكاء الاصطناعي', 'التصور', 'البيانات الضخمة'], category: 'التقنية' },
    { id: 'cybersecurity', name: 'خبير الأمن السيبراني', icon: '🔐', description: 'أمن المعلومات والتدقيق', capabilities: ['التدقيق', 'اختبار الاختراق', 'SIEM', 'الامتثال'], category: 'التقنية' },
    // ===== الإبداع =====
    { id: 'content-creator', name: 'صانع المحتوى', icon: '✍️', description: 'كتابة محتوى الويب والمدونات ووسائل التواصل', capabilities: ['المقالات', 'منشورات التواصل', 'النصوص', 'النشرات'], category: 'الإبداع' },
    { id: 'copywriter', name: 'كاتب إعلاني', icon: '📝', description: 'النصوص الإعلانية وصفحات البيع', capabilities: ['صفحات الهبوط', 'البريد الإلكتروني', 'الشعارات', 'القصص'], category: 'الإبداع' },
    { id: 'seo-expert', name: 'خبير تحسين محركات البحث', icon: '🔍', description: 'تحسين ظهور المواقع في محركات البحث', capabilities: ['الكلمات المفتاحية', 'الروابط الخلفية', 'التقنية', 'المحتوى'], category: 'الإبداع' },
    { id: 'social-manager', name: 'مدير وسائل التواصل', icon: '📱', description: 'إدارة شبكات التواصل الاجتماعي', capabilities: ['التخطيط', 'التفاعل', 'الإشراف', 'التحليلات'], category: 'الإبداع' },
    // ===== الصحة =====
    { id: 'health-advisor', name: 'مستشار الصحة', icon: '🏥', description: 'نصائح صحية وعافية عامة', capabilities: ['الوقاية', 'التغذية', 'النوم', 'الرياضة'], category: 'الصحة' },
    { id: 'nutrition-coach', name: 'مدرب التغذية', icon: '🥗', description: 'برامج غذائية ونصائح تغذوية', capabilities: ['الحميات', 'القوائم', 'المكملات', 'الحساسية'], category: 'الصحة' },
    { id: 'fitness-coach', name: 'مدرب اللياقة البدنية', icon: '💪', description: 'برامج تدريب مخصصة', capabilities: ['بناء العضلات', 'الكارديو', 'التمدد', 'التمارين المكثفة'], category: 'الصحة' },
    { id: 'mental-coach', name: 'مدرب التنمية الذاتية', icon: '🧘', description: 'إدارة التوتر والتطوير الشخصي', capabilities: ['التأمل', 'الإنتاجية', 'الثقة', 'التحفيز'], category: 'الصحة' },
    // ===== الدعم =====
    { id: 'customer-support', name: 'دعم العملاء', icon: '🎧', description: 'مساعدة العملاء وحل المشاكل', capabilities: ['الأسئلة الشائعة', 'الشكاوى', 'المتابعة', 'رضا العملاء'], category: 'الدعم' },
    { id: 'tech-support', name: 'الدعم الفني', icon: '🔧', description: 'المساعدة التقنية وإصلاح الأعطال', capabilities: ['التشخيص', 'التثبيت', 'الإعداد', 'الصيانة'], category: 'الدعم' },
    { id: 'hr-assistant', name: 'مساعد الموارد البشرية', icon: '👥', description: 'الموارد البشرية والتوظيف', capabilities: ['التوظيف', 'الإدماج', 'التكوين', 'الرواتب'], category: 'الدعم' },
    { id: 'project-manager', name: 'مدير المشاريع', icon: '📋', description: 'إدارة المشاريع والمنهجيات الرشيقة', capabilities: ['التخطيط', 'سكروم', 'كانبان', 'التقارير'], category: 'الدعم' },
  ],
  en: [
    // ===== BUSINESS =====
    { id: 'business-consultant', name: 'Business Consultant', icon: '💼', description: 'Business strategy, market research and business plans', capabilities: ['Market Research', 'Business Plans', 'Competitive Analysis', 'Growth Strategy'], category: 'Business' },
    { id: 'marketing-expert', name: 'Marketing Expert', icon: '📣', description: 'Digital marketing strategies and advertising campaigns', capabilities: ['SEO/SEM', 'Social Media', 'Content Marketing', 'Advertising'], category: 'Business' },
    { id: 'sales-coach', name: 'Sales Coach', icon: '🎯', description: 'Sales techniques and business negotiation', capabilities: ['Prospecting', 'Negotiation', 'Closing', 'CRM'], category: 'Business' },
    { id: 'startup-advisor', name: 'Startup Advisor', icon: '🚀', description: 'Startup creation and development support', capabilities: ['Pitch Deck', 'Fundraising', 'MVP', 'Growth Hacking'], category: 'Business' },
    // ===== FINANCE =====
    { id: 'finance-analyst', name: 'Finance Analyst', icon: '📈', description: 'Financial analysis, accounting and treasury management', capabilities: ['Balance Sheet', 'Tax Returns', 'Treasury', 'Financial Ratios'], category: 'Finance' },
    { id: 'tax-advisor', name: 'Tax Advisor', icon: '💵', description: 'Tax optimization and tax returns', capabilities: ['Income Tax', 'VAT', 'Optimization', 'Returns'], category: 'Finance' },
    { id: 'investment-advisor', name: 'Investment Advisor', icon: '💰', description: 'Investment strategies and wealth management', capabilities: ['Stocks', 'Real Estate', 'Crypto', 'Diversification'], category: 'Finance' },
    { id: 'budget-planner', name: 'Budget Planner', icon: '📊', description: 'Personal and professional budget management', capabilities: ['Monthly Budget', 'Savings', 'Expenses', 'Forecasts'], category: 'Finance' },
    // ===== LEGAL =====
    { id: 'legal-advisor', name: 'Legal Advisor', icon: '⚖️', description: 'Legal advice and contract drafting', capabilities: ['Contracts', 'Legal Advice', 'Legal Watch', 'Litigation'], category: 'Legal' },
    { id: 'contract-specialist', name: 'Contract Specialist', icon: '📜', description: 'Commercial contract drafting and analysis', capabilities: ['NDA', 'Terms & Conditions', 'Employment Contracts', 'Partnerships'], category: 'Legal' },
    { id: 'ip-lawyer', name: 'IP Expert', icon: '®️', description: 'Trademark, patent and copyright protection', capabilities: ['Trademarks', 'Patents', 'Copyright', 'Licenses'], category: 'Legal' },
    { id: 'gdpr-expert', name: 'Data Protection Expert', icon: '🔒', description: 'Personal data protection compliance', capabilities: ['Data Audit', 'Privacy Policy', 'DPO', 'Registry'], category: 'Legal' },
    // ===== EDUCATION =====
    { id: 'tutor-general', name: 'General Tutor', icon: '🎓', description: 'Homework help and private lessons for all levels', capabilities: ['Custom Lessons', 'Exercises', 'Exam Prep', 'Methodology'], category: 'Education' },
    { id: 'bac-coach', name: 'Baccalaureate Coach', icon: '📚', description: 'Intensive preparation for Algerian baccalaureate', capabilities: ['Revisions', 'Past Papers', 'Summaries', 'Simulations'], category: 'Education' },
    { id: 'bem-coach', name: 'BEM Coach', icon: '📝', description: 'Middle School Certificate preparation', capabilities: ['Math', 'French', 'Arabic', 'Science'], category: 'Education' },
    { id: 'language-teacher', name: 'Language Teacher', icon: '🌍', description: 'Foreign language learning', capabilities: ['English', 'French', 'Spanish', 'German'], category: 'Education' },
    { id: 'math-tutor', name: 'Math Tutor', icon: '🔢', description: 'Mathematics for all levels', capabilities: ['Algebra', 'Geometry', 'Analysis', 'Statistics'], category: 'Education' },
    { id: 'science-tutor', name: 'Science Tutor', icon: '🔬', description: 'Physics, Chemistry and Natural Sciences', capabilities: ['Physics', 'Chemistry', 'Biology', 'Experiments'], category: 'Education' },
    // ===== ALGERIAN ADMINISTRATION =====
    { id: 'cnas-agent', name: 'Social Security Agent', icon: '🏥', description: 'Complete guide for CNAS procedures', capabilities: ['Registration', 'Reimbursements', 'Sick Leave', 'Maternity'], category: 'Admin DZ' },
    { id: 'casnos-agent', name: 'Self-Employed Fund Agent', icon: '👷', description: 'Help for self-employed workers', capabilities: ['Contributions', 'Retirement', 'Health Coverage', 'Declarations'], category: 'Admin DZ' },
    { id: 'cnrc-agent', name: 'Trade Registry Agent', icon: '📋', description: 'Commercial registry and business creation', capabilities: ['Registration', 'Modifications', 'Deletion', 'Certificates'], category: 'Admin DZ' },
    { id: 'impots-agent', name: 'Tax Agent', icon: '🏛️', description: 'Tax returns and taxes', capabilities: ['G50', 'Income Tax', 'Corporate Tax', 'Activity Tax'], category: 'Admin DZ' },
    { id: 'douanes-agent', name: 'Customs Agent', icon: '🛃', description: 'Import/export procedures', capabilities: ['Customs Clearance', 'Tariffs', 'Documents', 'Exemptions'], category: 'Admin DZ' },
    { id: 'anem-agent', name: 'Employment Agency Agent', icon: '💼', description: 'Job search and employment assistance', capabilities: ['Job Offers', 'CV', 'Training', 'Integration'], category: 'Admin DZ' },
    { id: 'ansej-agent', name: 'Youth Support Agency Agent', icon: '🚀', description: 'Business creation for young people', capabilities: ['Application', 'Funding', 'Support', 'Benefits'], category: 'Admin DZ' },
    { id: 'passport-agent', name: 'Passport Agent', icon: '🛂', description: 'Biometric passport application', capabilities: ['Documents', 'Appointments', 'Renewal', 'Urgent'], category: 'Admin DZ' },
    // ===== TECH =====
    { id: 'dev-assistant', name: 'Developer Assistant', icon: '💻', description: 'Development help and debugging', capabilities: ['Code Review', 'Debug', 'Architecture', 'Best Practices'], category: 'Tech' },
    { id: 'devops-expert', name: 'DevOps Expert', icon: '🔧', description: 'CI/CD, cloud and infrastructure', capabilities: ['Docker', 'Kubernetes', 'AWS/GCP', 'Terraform'], category: 'Tech' },
    { id: 'data-scientist', name: 'Data Scientist', icon: '📊', description: 'Data analysis and machine learning', capabilities: ['Python', 'ML/AI', 'Visualization', 'Big Data'], category: 'Tech' },
    { id: 'cybersecurity', name: 'Cybersecurity Expert', icon: '🔐', description: 'IT security and audit', capabilities: ['Audit', 'Pentest', 'SIEM', 'Compliance'], category: 'Tech' },
    // ===== CREATIVE =====
    { id: 'content-creator', name: 'Content Creator', icon: '✍️', description: 'Web content, blogs and social media writing', capabilities: ['Articles', 'Social Posts', 'Scripts', 'Newsletters'], category: 'Creative' },
    { id: 'copywriter', name: 'Copywriter', icon: '📝', description: 'Advertising copy and sales pages', capabilities: ['Landing Pages', 'Emails', 'Slogans', 'Storytelling'], category: 'Creative' },
    { id: 'seo-expert', name: 'SEO Expert', icon: '🔍', description: 'Search engine optimization', capabilities: ['Keywords', 'Backlinks', 'Technical', 'Content'], category: 'Creative' },
    { id: 'social-manager', name: 'Community Manager', icon: '📱', description: 'Social media management', capabilities: ['Planning', 'Engagement', 'Moderation', 'Analytics'], category: 'Creative' },
    // ===== HEALTH =====
    { id: 'health-advisor', name: 'Health Advisor', icon: '🏥', description: 'Health tips and general wellness', capabilities: ['Prevention', 'Nutrition', 'Sleep', 'Exercise'], category: 'Health' },
    { id: 'nutrition-coach', name: 'Nutrition Coach', icon: '🥗', description: 'Meal plans and nutritional advice', capabilities: ['Diets', 'Menus', 'Supplements', 'Allergies'], category: 'Health' },
    { id: 'fitness-coach', name: 'Fitness Coach', icon: '💪', description: 'Personalized training programs', capabilities: ['Weight Training', 'Cardio', 'Stretching', 'HIIT'], category: 'Health' },
    { id: 'mental-coach', name: 'Mental Coach', icon: '🧘', description: 'Stress management and personal development', capabilities: ['Meditation', 'Productivity', 'Confidence', 'Motivation'], category: 'Health' },
    // ===== SUPPORT =====
    { id: 'customer-support', name: 'Customer Support', icon: '🎧', description: 'Customer assistance and problem solving', capabilities: ['FAQ', 'Complaints', 'Follow-up', 'Satisfaction'], category: 'Support' },
    { id: 'tech-support', name: 'Technical Support', icon: '🔧', description: 'Technical help and troubleshooting', capabilities: ['Diagnosis', 'Installation', 'Configuration', 'Maintenance'], category: 'Support' },
    { id: 'hr-assistant', name: 'HR Assistant', icon: '👥', description: 'Human resources and recruitment', capabilities: ['Recruitment', 'Onboarding', 'Training', 'Payroll'], category: 'Support' },
    { id: 'project-manager', name: 'Project Manager', icon: '📋', description: 'Project management and agile methodologies', capabilities: ['Planning', 'Scrum', 'Kanban', 'Reporting'], category: 'Support' },
  ],
};

// Fonction pour obtenir les agents selon la langue
const getAgents = (lang: string): Agent[] => {
  return agentsData[lang] || agentsData['fr'];
};

// Fonction pour obtenir les catégories selon la langue
const getCategories = (lang: string): string[] => {
  const agents = getAgents(lang);
  return [...new Set(agents.map(a => a.category))];
};

export default function Agents() {
  const { t, lang } = useTranslation();
  const navigate = useNavigate();
  const [theme, setTheme] = useState<Theme>('dark');
  const isRTL = lang === 'ar';
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isLoggedIn] = useState(() => localStorage.getItem('isLoggedIn') === 'true');

  // Obtenir les agents et catégories selon la langue
  const allAgents = getAgents(lang);
  const categories = getCategories(lang);

  useEffect(() => {
    const savedTheme = (localStorage.getItem('theme') as Theme) || 'dark';
    setTheme(savedTheme);

    const observer = new MutationObserver(() => {
      const currentTheme = document.documentElement.dataset.theme as Theme;
      if (currentTheme) setTheme(currentTheme);
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme'],
    });

    return () => observer.disconnect();
  }, []);

  // Filtrer les agents
  const filteredAgents = allAgents.filter((agent: Agent) => {
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          agent.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || agent.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Gérer le clic sur "Connecter"
  const handleConnect = (agentId: string) => {
    if (!isLoggedIn) {
      localStorage.setItem('redirectTool', `agent-${agentId}`);
      navigate('/login');
    } else {
      navigate(`/chat?agent=${agentId}`);
    }
  };

  const isDark = theme === 'dark';
  // Couleurs synchronisées avec Home.tsx
  const bgColor = isDark ? '#0A0F1A' : '#F6F3EE';
  const cardBg = isDark ? 'rgba(255,255,255,0.06)' : '#EDE9E3';
  const textColor = isDark ? '#F8FAFC' : '#141414';
  const textMuted = isDark ? 'rgba(248,250,252,0.65)' : 'rgba(20,20,20,0.62)';
  const borderColor = isDark ? 'rgba(255,255,255,0.10)' : 'rgba(20,20,20,0.10)';
  const inputBg = isDark ? 'rgba(255,255,255,0.06)' : '#EDE9E3';
  const accentColor = isDark ? '#22C55E' : '#1C7A5F';
  const accentGradient = `linear-gradient(135deg, ${isDark ? '#22C55E' : '#1C7A5F'}, ${isDark ? '#57D6AA' : '#22C55E'})`;

  return (
    <div
      dir={isRTL ? 'rtl' : 'ltr'}
      style={{
        paddingTop: '120px',
        paddingBottom: '80px',
        minHeight: '100vh',
        background: bgColor,
      }}
    >
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 24px' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1
            style={{
              fontSize: 'clamp(32px, 5vw, 48px)',
              fontWeight: 700,
              color: textColor,
              marginBottom: '16px',
            }}
          >
            {t('agents_page_title')}
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto',
            }}
          >
            {allAgents.length} {t('agents_page_subtitle')}
          </p>
        </div>

        {/* Search & Filters */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '16px',
            marginBottom: '40px',
            alignItems: 'center',
          }}
        >
          {/* Search Bar */}
          <div style={{ position: 'relative', width: '100%', maxWidth: '500px' }}>
            <input
              type="text"
              placeholder={t('agents_search')}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: isRTL ? '14px 50px 14px 20px' : '14px 20px 14px 50px',
                borderRadius: '12px',
                border: `1px solid ${borderColor}`,
                background: inputBg,
                color: textColor,
                fontSize: '16px',
                outline: 'none',
              }}
            />
            <span
              style={{
                position: 'absolute',
                left: isRTL ? 'auto' : '18px',
                right: isRTL ? '18px' : 'auto',
                top: '50%',
                transform: 'translateY(-50%)',
                fontSize: '20px',
              }}
            >
              🔍
            </span>
          </div>

          {/* Category Filters */}
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '8px',
              justifyContent: 'center',
            }}
          >
            <button
              type="button"
              onClick={() => setSelectedCategory('all')}
              style={{
                padding: '8px 16px',
                borderRadius: '20px',
                border: `1px solid ${selectedCategory === 'all' ? accentColor : borderColor}`,
                background: selectedCategory === 'all' ? (isDark ? 'rgba(34, 197, 94, 0.15)' : 'rgba(0, 98, 51, 0.15)') : 'transparent',
                color: selectedCategory === 'all' ? accentColor : textMuted,
                fontSize: '14px',
                fontWeight: 500,
                cursor: 'pointer',
              }}
            >
              {t('all')} ({allAgents.length})
            </button>
            {categories.map((cat: string) => {
              const count = allAgents.filter((a: Agent) => a.category === cat).length;
              return (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setSelectedCategory(cat)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '20px',
                    border: `1px solid ${selectedCategory === cat ? accentColor : borderColor}`,
                    background: selectedCategory === cat ? (isDark ? 'rgba(34, 197, 94, 0.15)' : 'rgba(0, 98, 51, 0.15)') : 'transparent',
                    color: selectedCategory === cat ? accentColor : textMuted,
                    fontSize: '14px',
                    fontWeight: 500,
                    cursor: 'pointer',
                  }}
                >
                  {cat} ({count})
                </button>
              );
            })}
          </div>
        </div>

        {/* Results Count */}
        <p style={{ color: textMuted, marginBottom: '24px', textAlign: 'center' }}>
          {filteredAgents.length} {filteredAgents.length > 1 ? t('agents_found_plural') : t('agents_found')} {t('found')}
        </p>

        {/* Agents Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '20px',
          }}
        >
          {filteredAgents.map((agent: Agent) => (
            <div
              key={agent.id}
              style={{
                background: cardBg,
                borderRadius: '16px',
                padding: '24px',
                border: `1px solid ${borderColor}`,
                transition: 'all 0.3s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.borderColor = accentColor;
                e.currentTarget.style.boxShadow = isDark ? '0 12px 24px rgba(34, 197, 94, 0.15)' : '0 12px 24px rgba(0, 98, 51, 0.15)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.borderColor = borderColor;
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              {/* Header */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '16px',
                  marginBottom: '16px',
                }}
              >
                <div
                  style={{
                    width: '56px',
                    height: '56px',
                    borderRadius: '14px',
                    background: isDark ? 'rgba(34, 197, 94, 0.1)' : 'rgba(0, 98, 51, 0.08)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '28px',
                  }}
                >
                  {agent.icon}
                </div>
                <div>
                  <h3
                    style={{
                      fontSize: 'clamp(16px, 2.5vw, 18px)',
                      fontWeight: 600,
                      color: textColor,
                      margin: 0,
                    }}
                  >
                    {agent.name}
                  </h3>
                  <span
                    style={{
                      fontSize: '12px',
                      color: accentColor,
                      fontWeight: 500,
                    }}
                  >
                    {agent.category}
                  </span>
                </div>
              </div>

              {/* Description */}
              <p
                style={{
                  color: textMuted,
                  fontSize: '14px',
                  lineHeight: 1.6,
                  marginBottom: '16px',
                  minHeight: '44px',
                }}
              >
                {agent.description}
              </p>

              {/* Capabilities */}
              <div style={{ marginBottom: '20px' }}>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {agent.capabilities.map((cap: string) => (
                    <span
                      key={cap}
                      style={{
                        background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        color: textMuted,
                      }}
                    >
                      {cap}
                    </span>
                  ))}
                </div>
              </div>

              {/* Connect Button */}
              <button
                type="button"
                onClick={() => handleConnect(agent.id)}
                style={{
                  width: '100%',
                  padding: '12px',
                  background: accentGradient,
                  border: 'none',
                  borderRadius: '10px',
                  color: '#fff',
                  fontSize: '14px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                }}
              >
                {isLoggedIn ? (
                  <>
                    <span>{t('agents_discuss')}</span>
                    <span>{isRTL ? '←' : '→'}</span>
                  </>
                ) : (
                  <>
                    <span>🔗</span>
                    <span>{t('connect')}</span>
                  </>
                )}
              </button>
            </div>
          ))}
        </div>

        {/* No Results */}
        {filteredAgents.length === 0 && (
          <div
            style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: textMuted,
            }}
          >
            <span style={{ fontSize: 'clamp(36px, 6vw, 48px)', display: 'block', marginBottom: '16px' }}>🤖</span>
            <p style={{ fontSize: 'clamp(16px, 2.5vw, 18px)' }}>{t('agents_no_result')} "{searchQuery}"</p>
            <button
              type="button"
              onClick={() => {
                setSearchQuery('');
                setSelectedCategory('all');
              }}
              style={{
                marginTop: '16px',
                padding: '10px 20px',
                background: 'transparent',
                border: `1px solid ${borderColor}`,
                borderRadius: '8px',
                color: textColor,
                cursor: 'pointer',
              }}
            >
              {t('reset_filters')}
            </button>
          </div>
        )}

        {/* CTA Section */}
        <div
          style={{
            marginTop: '60px',
            background: cardBg,
            borderRadius: '20px',
            padding: 'clamp(24px, 5vw, 48px)',
            textAlign: 'center',
            border: `2px solid ${accentColor}`,
          }}
        >
          <h2
            style={{
              fontSize: 'clamp(22px, 4vw, 28px)',
              fontWeight: 600,
              color: textColor,
              marginBottom: '16px',
            }}
          >
            {t('agents_custom_title')}
          </h2>
          <p
            style={{
              color: textMuted,
              fontSize: 'clamp(14px, 2.5vw, 16px)',
              maxWidth: '500px',
              margin: '0 auto 24px',
            }}
          >
            {t('agents_custom_desc')}
          </p>
          <button
            type="button"
            onClick={() => navigate(isLoggedIn ? '/chat' : '/login')}
            style={{
              padding: '16px 32px',
              background: accentGradient,
              color: '#fff',
              fontSize: 'clamp(16px, 2.5vw, 18px)',
              fontWeight: 600,
              border: 'none',
              borderRadius: '12px',
              cursor: 'pointer',
              boxShadow: isDark ? '0 4px 16px rgba(34, 197, 94, 0.3)' : '0 4px 16px rgba(0, 98, 51, 0.3)',
            }}
          >
            {isLoggedIn ? t('agents_create') : t('apps_start_free')}
          </button>
        </div>
      </div>
    </div>
  );
}
