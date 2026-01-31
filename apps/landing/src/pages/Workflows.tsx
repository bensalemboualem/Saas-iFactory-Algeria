import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '../i18n';

type Theme = 'dark' | 'light';

interface Workflow {
  id: string;
  name: string;
  icon: string;
  description: string;
  steps: string[];
  category: string;
  estimatedTime: string;
}

// Données des workflows par langue
const workflowsData: Record<string, Workflow[]> = {
  fr: [
    // ===== CONTENU =====
    { id: 'content-pipeline', name: 'Pipeline de Contenu', icon: '📝', description: 'Création automatisée d\'articles de blog optimisés SEO', steps: ['Recherche', 'Rédaction', 'SEO', 'Images', 'Publication'], category: 'Contenu', estimatedTime: '15 min' },
    { id: 'blog-automation', name: 'Automatisation Blog', icon: '✍️', description: 'Génération et publication automatique d\'articles', steps: ['Idées', 'Plan', 'Rédaction', 'Révision', 'Planification'], category: 'Contenu', estimatedTime: '20 min' },
    { id: 'ebook-creator', name: 'Créateur d\'Ebook', icon: '📖', description: 'Création d\'ebooks complets de A à Z', steps: ['Structure', 'Chapitres', 'Design', 'Export PDF', 'Distribution'], category: 'Contenu', estimatedTime: '2h' },
    { id: 'newsletter-flow', name: 'Flow Newsletter', icon: '📧', description: 'Création et envoi automatisé de newsletters', steps: ['Sujet', 'Contenu', 'Design', 'Test', 'Envoi'], category: 'Contenu', estimatedTime: '30 min' },
    // ===== MARKETING =====
    { id: 'lead-generation', name: 'Génération de Leads', icon: '🎯', description: 'Pipeline complet de génération et qualification de leads', steps: ['Capture', 'Qualification', 'Scoring', 'Nurturing', 'Conversion'], category: 'Marketing', estimatedTime: 'Continu' },
    { id: 'social-media-flow', name: 'Flux Réseaux Sociaux', icon: '📱', description: 'Gestion automatisée des réseaux sociaux', steps: ['Idéation', 'Création', 'Adaptation', 'Planification', 'Analytics'], category: 'Marketing', estimatedTime: '1h/semaine' },
    { id: 'ad-campaign', name: 'Campagne Publicitaire', icon: '📣', description: 'Création et optimisation de campagnes ads', steps: ['Audience', 'Créatifs', 'A/B Test', 'Optimisation', 'Reporting'], category: 'Marketing', estimatedTime: '2h' },
    { id: 'influencer-outreach', name: 'Outreach Influenceurs', icon: '🌟', description: 'Identification et contact d\'influenceurs', steps: ['Recherche', 'Sélection', 'Contact', 'Négociation', 'Suivi'], category: 'Marketing', estimatedTime: '3h' },
    { id: 'seo-audit', name: 'Audit SEO Complet', icon: '🔍', description: 'Analyse et optimisation SEO de votre site', steps: ['Crawl', 'Analyse', 'Mots-clés', 'Recommandations', 'Suivi'], category: 'Marketing', estimatedTime: '4h' },
    // ===== VENTES =====
    { id: 'sales-pipeline', name: 'Pipeline Commercial', icon: '💼', description: 'Gestion automatisée du cycle de vente', steps: ['Prospection', 'Qualification', 'Présentation', 'Négociation', 'Closing'], category: 'Ventes', estimatedTime: 'Continu' },
    { id: 'proposal-generator', name: 'Générateur Devis', icon: '📋', description: 'Création automatique de propositions commerciales', steps: ['Brief', 'Chiffrage', 'Rédaction', 'Design', 'Envoi'], category: 'Ventes', estimatedTime: '45 min' },
    { id: 'follow-up-automation', name: 'Relances Automatiques', icon: '🔄', description: 'Séquences de relance client automatisées', steps: ['Segmentation', 'Séquence', 'Personnalisation', 'Envoi', 'Analyse'], category: 'Ventes', estimatedTime: '30 min' },
    { id: 'crm-sync', name: 'Synchronisation CRM', icon: '🔗', description: 'Intégration et synchronisation avec votre CRM', steps: ['Connexion', 'Mapping', 'Import', 'Automatisation', 'Reporting'], category: 'Ventes', estimatedTime: '1h' },
    // ===== SUPPORT CLIENT =====
    { id: 'customer-support', name: 'Support Client IA', icon: '💬', description: 'Automatisation du support client avec IA', steps: ['Réception', 'Classification', 'Réponse IA', 'Escalade', 'Suivi'], category: 'Support', estimatedTime: '24/7' },
    { id: 'ticket-triage', name: 'Triage Tickets', icon: '🎫', description: 'Classification automatique des tickets support', steps: ['Réception', 'Analyse', 'Catégorie', 'Priorité', 'Attribution'], category: 'Support', estimatedTime: 'Instantané' },
    { id: 'faq-builder', name: 'Constructeur FAQ', icon: '❓', description: 'Création et mise à jour automatique de FAQ', steps: ['Analyse questions', 'Regroupement', 'Rédaction', 'Validation', 'Publication'], category: 'Support', estimatedTime: '2h' },
    { id: 'feedback-analysis', name: 'Analyse Feedback', icon: '📊', description: 'Analyse automatique des retours clients', steps: ['Collecte', 'Sentiment', 'Catégories', 'Insights', 'Actions'], category: 'Support', estimatedTime: '1h' },
    // ===== DONNÉES =====
    { id: 'data-analysis', name: 'Analyse de Données', icon: '📈', description: 'Pipeline complet d\'analyse de données', steps: ['Import', 'Nettoyage', 'Analyse', 'Visualisation', 'Rapport'], category: 'Données', estimatedTime: '2h' },
    { id: 'report-automation', name: 'Rapports Automatiques', icon: '📑', description: 'Génération automatique de rapports périodiques', steps: ['Sources', 'Agrégation', 'Analyse', 'Format', 'Distribution'], category: 'Données', estimatedTime: '30 min' },
    { id: 'competitor-monitoring', name: 'Veille Concurrentielle', icon: '👁️', description: 'Surveillance automatique de vos concurrents', steps: ['Sources', 'Scraping', 'Analyse', 'Alertes', 'Rapport'], category: 'Données', estimatedTime: 'Continu' },
    { id: 'market-research', name: 'Étude de Marché', icon: '🌍', description: 'Recherche et analyse de marché automatisée', steps: ['Définition', 'Collecte', 'Analyse', 'Tendances', 'Recommandations'], category: 'Données', estimatedTime: '4h' },
    // ===== RH =====
    { id: 'recruitment-flow', name: 'Recrutement Automatisé', icon: '👥', description: 'Pipeline de recrutement de bout en bout', steps: ['Offre', 'Sourcing', 'Screening', 'Entretiens', 'Onboarding'], category: 'RH', estimatedTime: 'Variable' },
    { id: 'cv-screening', name: 'Tri de CV', icon: '📄', description: 'Analyse et tri automatique des candidatures', steps: ['Réception', 'Parsing', 'Scoring', 'Classement', 'Shortlist'], category: 'RH', estimatedTime: '5 min/CV' },
    { id: 'onboarding-flow', name: 'Onboarding Employé', icon: '🎯', description: 'Parcours d\'intégration automatisé', steps: ['Accueil', 'Documents', 'Formation', 'Équipement', 'Suivi'], category: 'RH', estimatedTime: '1 semaine' },
    { id: 'performance-review', name: 'Évaluation Performance', icon: '⭐', description: 'Processus d\'évaluation annuelle', steps: ['Auto-éval', 'Manager', '360°', 'Synthèse', 'Plan action'], category: 'RH', estimatedTime: '2h' },
    // ===== FINANCE =====
    { id: 'invoice-processing', name: 'Traitement Factures', icon: '🧾', description: 'Automatisation du traitement des factures', steps: ['Réception', 'OCR', 'Validation', 'Comptabilisation', 'Paiement'], category: 'Finance', estimatedTime: '2 min/facture' },
    { id: 'expense-management', name: 'Gestion Notes de Frais', icon: '💳', description: 'Automatisation des notes de frais', steps: ['Soumission', 'OCR', 'Catégorie', 'Approbation', 'Remboursement'], category: 'Finance', estimatedTime: '1 min/note' },
    { id: 'budget-tracking', name: 'Suivi Budgétaire', icon: '📊', description: 'Suivi automatique des budgets', steps: ['Définition', 'Suivi', 'Alertes', 'Ajustements', 'Reporting'], category: 'Finance', estimatedTime: 'Continu' },
    { id: 'tax-preparation', name: 'Préparation Fiscale', icon: '🏛️', description: 'Préparation des déclarations fiscales', steps: ['Collecte', 'Calculs', 'Vérification', 'Déclaration', 'Archivage'], category: 'Finance', estimatedTime: '4h' },
    // ===== E-COMMERCE =====
    { id: 'product-listing', name: 'Listing Produits', icon: '🛍️', description: 'Création automatique de fiches produits', steps: ['Import', 'Descriptions', 'Images', 'SEO', 'Publication'], category: 'E-Commerce', estimatedTime: '10 min/produit' },
    { id: 'inventory-sync', name: 'Sync Inventaire', icon: '📦', description: 'Synchronisation multi-canal de l\'inventaire', steps: ['Connexion', 'Mapping', 'Sync', 'Alertes', 'Rapports'], category: 'E-Commerce', estimatedTime: 'Temps réel' },
    { id: 'abandoned-cart', name: 'Paniers Abandonnés', icon: '🛒', description: 'Récupération automatique des paniers', steps: ['Détection', 'Segmentation', 'Email 1', 'Email 2', 'Offre'], category: 'E-Commerce', estimatedTime: 'Auto' },
    { id: 'review-management', name: 'Gestion Avis', icon: '⭐', description: 'Collecte et gestion des avis clients', steps: ['Demande', 'Collecte', 'Modération', 'Réponse', 'Analyse'], category: 'E-Commerce', estimatedTime: '15 min/jour' },
    // ===== JURIDIQUE =====
    { id: 'contract-review', name: 'Révision Contrats', icon: '⚖️', description: 'Analyse automatique de contrats', steps: ['Upload', 'OCR', 'Analyse', 'Risques', 'Recommandations'], category: 'Juridique', estimatedTime: '30 min' },
    { id: 'compliance-check', name: 'Vérification Conformité', icon: '✅', description: 'Audit de conformité automatisé', steps: ['Référentiel', 'Audit', 'Écarts', 'Actions', 'Rapport'], category: 'Juridique', estimatedTime: '2h' },
    { id: 'gdpr-audit', name: 'Audit RGPD', icon: '🔒', description: 'Audit de conformité RGPD', steps: ['Inventaire', 'Analyse', 'Risques', 'Plan action', 'Documentation'], category: 'Juridique', estimatedTime: '1 jour' },
  ],
  ar: [
    // ===== المحتوى =====
    { id: 'content-pipeline', name: 'خط إنتاج المحتوى', icon: '📝', description: 'إنشاء مقالات مدونة محسنة لمحركات البحث تلقائياً', steps: ['البحث', 'الكتابة', 'SEO', 'الصور', 'النشر'], category: 'المحتوى', estimatedTime: '15 دقيقة' },
    { id: 'blog-automation', name: 'أتمتة المدونة', icon: '✍️', description: 'إنشاء ونشر المقالات تلقائياً', steps: ['الأفكار', 'الخطة', 'الكتابة', 'المراجعة', 'الجدولة'], category: 'المحتوى', estimatedTime: '20 دقيقة' },
    { id: 'ebook-creator', name: 'منشئ الكتب الإلكترونية', icon: '📖', description: 'إنشاء كتب إلكترونية كاملة من الألف إلى الياء', steps: ['الهيكل', 'الفصول', 'التصميم', 'تصدير PDF', 'التوزيع'], category: 'المحتوى', estimatedTime: 'ساعتان' },
    { id: 'newsletter-flow', name: 'تدفق النشرة الإخبارية', icon: '📧', description: 'إنشاء وإرسال النشرات الإخبارية تلقائياً', steps: ['الموضوع', 'المحتوى', 'التصميم', 'الاختبار', 'الإرسال'], category: 'المحتوى', estimatedTime: '30 دقيقة' },
    // ===== التسويق =====
    { id: 'lead-generation', name: 'توليد العملاء المحتملين', icon: '🎯', description: 'خط إنتاج كامل لتوليد وتأهيل العملاء المحتملين', steps: ['الالتقاط', 'التأهيل', 'التسجيل', 'الرعاية', 'التحويل'], category: 'التسويق', estimatedTime: 'مستمر' },
    { id: 'social-media-flow', name: 'تدفق وسائل التواصل', icon: '📱', description: 'إدارة وسائل التواصل الاجتماعي تلقائياً', steps: ['الأفكار', 'الإنشاء', 'التكييف', 'الجدولة', 'التحليلات'], category: 'التسويق', estimatedTime: 'ساعة/أسبوع' },
    { id: 'ad-campaign', name: 'الحملة الإعلانية', icon: '📣', description: 'إنشاء وتحسين حملات الإعلانات', steps: ['الجمهور', 'الإبداعات', 'اختبار A/B', 'التحسين', 'التقارير'], category: 'التسويق', estimatedTime: 'ساعتان' },
    { id: 'influencer-outreach', name: 'التواصل مع المؤثرين', icon: '🌟', description: 'تحديد والتواصل مع المؤثرين', steps: ['البحث', 'الاختيار', 'التواصل', 'التفاوض', 'المتابعة'], category: 'التسويق', estimatedTime: '3 ساعات' },
    { id: 'seo-audit', name: 'تدقيق SEO الكامل', icon: '🔍', description: 'تحليل وتحسين SEO لموقعك', steps: ['الزحف', 'التحليل', 'الكلمات المفتاحية', 'التوصيات', 'المتابعة'], category: 'التسويق', estimatedTime: '4 ساعات' },
    // ===== المبيعات =====
    { id: 'sales-pipeline', name: 'خط المبيعات', icon: '💼', description: 'إدارة دورة المبيعات تلقائياً', steps: ['التنقيب', 'التأهيل', 'العرض', 'التفاوض', 'الإغلاق'], category: 'المبيعات', estimatedTime: 'مستمر' },
    { id: 'proposal-generator', name: 'منشئ العروض', icon: '📋', description: 'إنشاء عروض تجارية تلقائياً', steps: ['الموجز', 'التسعير', 'الكتابة', 'التصميم', 'الإرسال'], category: 'المبيعات', estimatedTime: '45 دقيقة' },
    { id: 'follow-up-automation', name: 'المتابعات التلقائية', icon: '🔄', description: 'تسلسلات متابعة العملاء الآلية', steps: ['التقسيم', 'التسلسل', 'التخصيص', 'الإرسال', 'التحليل'], category: 'المبيعات', estimatedTime: '30 دقيقة' },
    { id: 'crm-sync', name: 'مزامنة CRM', icon: '🔗', description: 'التكامل والمزامنة مع CRM الخاص بك', steps: ['الاتصال', 'التعيين', 'الاستيراد', 'الأتمتة', 'التقارير'], category: 'المبيعات', estimatedTime: 'ساعة' },
    // ===== دعم العملاء =====
    { id: 'customer-support', name: 'دعم العملاء الذكي', icon: '💬', description: 'أتمتة دعم العملاء بالذكاء الاصطناعي', steps: ['الاستقبال', 'التصنيف', 'الرد الذكي', 'التصعيد', 'المتابعة'], category: 'الدعم', estimatedTime: '24/7' },
    { id: 'ticket-triage', name: 'فرز التذاكر', icon: '🎫', description: 'تصنيف تذاكر الدعم تلقائياً', steps: ['الاستقبال', 'التحليل', 'الفئة', 'الأولوية', 'التعيين'], category: 'الدعم', estimatedTime: 'فوري' },
    { id: 'faq-builder', name: 'منشئ الأسئلة الشائعة', icon: '❓', description: 'إنشاء وتحديث الأسئلة الشائعة تلقائياً', steps: ['تحليل الأسئلة', 'التجميع', 'الكتابة', 'التحقق', 'النشر'], category: 'الدعم', estimatedTime: 'ساعتان' },
    { id: 'feedback-analysis', name: 'تحليل التعليقات', icon: '📊', description: 'تحليل ملاحظات العملاء تلقائياً', steps: ['الجمع', 'المشاعر', 'الفئات', 'الرؤى', 'الإجراءات'], category: 'الدعم', estimatedTime: 'ساعة' },
    // ===== البيانات =====
    { id: 'data-analysis', name: 'تحليل البيانات', icon: '📈', description: 'خط إنتاج كامل لتحليل البيانات', steps: ['الاستيراد', 'التنظيف', 'التحليل', 'التصور', 'التقرير'], category: 'البيانات', estimatedTime: 'ساعتان' },
    { id: 'report-automation', name: 'التقارير التلقائية', icon: '📑', description: 'إنشاء تقارير دورية تلقائياً', steps: ['المصادر', 'التجميع', 'التحليل', 'التنسيق', 'التوزيع'], category: 'البيانات', estimatedTime: '30 دقيقة' },
    { id: 'competitor-monitoring', name: 'مراقبة المنافسين', icon: '👁️', description: 'مراقبة منافسيك تلقائياً', steps: ['المصادر', 'الاستخراج', 'التحليل', 'التنبيهات', 'التقرير'], category: 'البيانات', estimatedTime: 'مستمر' },
    { id: 'market-research', name: 'دراسة السوق', icon: '🌍', description: 'البحث وتحليل السوق تلقائياً', steps: ['التعريف', 'الجمع', 'التحليل', 'الاتجاهات', 'التوصيات'], category: 'البيانات', estimatedTime: '4 ساعات' },
    // ===== الموارد البشرية =====
    { id: 'recruitment-flow', name: 'التوظيف الآلي', icon: '👥', description: 'خط توظيف من البداية للنهاية', steps: ['العرض', 'البحث', 'الفرز', 'المقابلات', 'الإدماج'], category: 'الموارد البشرية', estimatedTime: 'متغير' },
    { id: 'cv-screening', name: 'فرز السير الذاتية', icon: '📄', description: 'تحليل وفرز الترشيحات تلقائياً', steps: ['الاستقبال', 'التحليل', 'التسجيل', 'الترتيب', 'القائمة المختصرة'], category: 'الموارد البشرية', estimatedTime: '5 دقائق/سيرة' },
    { id: 'onboarding-flow', name: 'إدماج الموظف', icon: '🎯', description: 'مسار الإدماج الآلي', steps: ['الترحيب', 'الوثائق', 'التدريب', 'المعدات', 'المتابعة'], category: 'الموارد البشرية', estimatedTime: 'أسبوع' },
    { id: 'performance-review', name: 'تقييم الأداء', icon: '⭐', description: 'عملية التقييم السنوي', steps: ['التقييم الذاتي', 'المدير', '360°', 'التلخيص', 'خطة العمل'], category: 'الموارد البشرية', estimatedTime: 'ساعتان' },
    // ===== المالية =====
    { id: 'invoice-processing', name: 'معالجة الفواتير', icon: '🧾', description: 'أتمتة معالجة الفواتير', steps: ['الاستقبال', 'OCR', 'التحقق', 'المحاسبة', 'الدفع'], category: 'المالية', estimatedTime: '2 دقيقة/فاتورة' },
    { id: 'expense-management', name: 'إدارة المصاريف', icon: '💳', description: 'أتمتة مذكرات المصاريف', steps: ['التقديم', 'OCR', 'الفئة', 'الموافقة', 'السداد'], category: 'المالية', estimatedTime: 'دقيقة/مذكرة' },
    { id: 'budget-tracking', name: 'تتبع الميزانية', icon: '📊', description: 'تتبع الميزانيات تلقائياً', steps: ['التعريف', 'المتابعة', 'التنبيهات', 'التعديلات', 'التقارير'], category: 'المالية', estimatedTime: 'مستمر' },
    { id: 'tax-preparation', name: 'التحضير الضريبي', icon: '🏛️', description: 'تحضير التصريحات الضريبية', steps: ['الجمع', 'الحسابات', 'التحقق', 'التصريح', 'الأرشفة'], category: 'المالية', estimatedTime: '4 ساعات' },
    // ===== التجارة الإلكترونية =====
    { id: 'product-listing', name: 'قائمة المنتجات', icon: '🛍️', description: 'إنشاء بطاقات المنتجات تلقائياً', steps: ['الاستيراد', 'الأوصاف', 'الصور', 'SEO', 'النشر'], category: 'التجارة الإلكترونية', estimatedTime: '10 دقائق/منتج' },
    { id: 'inventory-sync', name: 'مزامنة المخزون', icon: '📦', description: 'مزامنة المخزون متعددة القنوات', steps: ['الاتصال', 'التعيين', 'المزامنة', 'التنبيهات', 'التقارير'], category: 'التجارة الإلكترونية', estimatedTime: 'الوقت الفعلي' },
    { id: 'abandoned-cart', name: 'السلات المتروكة', icon: '🛒', description: 'استعادة السلات المتروكة تلقائياً', steps: ['الكشف', 'التقسيم', 'البريد 1', 'البريد 2', 'العرض'], category: 'التجارة الإلكترونية', estimatedTime: 'تلقائي' },
    { id: 'review-management', name: 'إدارة التقييمات', icon: '⭐', description: 'جمع وإدارة تقييمات العملاء', steps: ['الطلب', 'الجمع', 'المراجعة', 'الرد', 'التحليل'], category: 'التجارة الإلكترونية', estimatedTime: '15 دقيقة/يوم' },
    // ===== القانون =====
    { id: 'contract-review', name: 'مراجعة العقود', icon: '⚖️', description: 'تحليل العقود تلقائياً', steps: ['الرفع', 'OCR', 'التحليل', 'المخاطر', 'التوصيات'], category: 'القانون', estimatedTime: '30 دقيقة' },
    { id: 'compliance-check', name: 'فحص الامتثال', icon: '✅', description: 'تدقيق الامتثال الآلي', steps: ['المرجع', 'التدقيق', 'الفجوات', 'الإجراءات', 'التقرير'], category: 'القانون', estimatedTime: 'ساعتان' },
    { id: 'gdpr-audit', name: 'تدقيق حماية البيانات', icon: '🔒', description: 'تدقيق الامتثال لحماية البيانات', steps: ['الجرد', 'التحليل', 'المخاطر', 'خطة العمل', 'التوثيق'], category: 'القانون', estimatedTime: 'يوم' },
  ],
  en: [
    // ===== CONTENT =====
    { id: 'content-pipeline', name: 'Content Pipeline', icon: '📝', description: 'Automated creation of SEO-optimized blog articles', steps: ['Research', 'Writing', 'SEO', 'Images', 'Publication'], category: 'Content', estimatedTime: '15 min' },
    { id: 'blog-automation', name: 'Blog Automation', icon: '✍️', description: 'Automatic article generation and publication', steps: ['Ideas', 'Outline', 'Writing', 'Revision', 'Scheduling'], category: 'Content', estimatedTime: '20 min' },
    { id: 'ebook-creator', name: 'Ebook Creator', icon: '📖', description: 'Complete ebook creation from A to Z', steps: ['Structure', 'Chapters', 'Design', 'PDF Export', 'Distribution'], category: 'Content', estimatedTime: '2h' },
    { id: 'newsletter-flow', name: 'Newsletter Flow', icon: '📧', description: 'Automated newsletter creation and sending', steps: ['Subject', 'Content', 'Design', 'Test', 'Send'], category: 'Content', estimatedTime: '30 min' },
    // ===== MARKETING =====
    { id: 'lead-generation', name: 'Lead Generation', icon: '🎯', description: 'Complete lead generation and qualification pipeline', steps: ['Capture', 'Qualification', 'Scoring', 'Nurturing', 'Conversion'], category: 'Marketing', estimatedTime: 'Ongoing' },
    { id: 'social-media-flow', name: 'Social Media Flow', icon: '📱', description: 'Automated social media management', steps: ['Ideation', 'Creation', 'Adaptation', 'Scheduling', 'Analytics'], category: 'Marketing', estimatedTime: '1h/week' },
    { id: 'ad-campaign', name: 'Ad Campaign', icon: '📣', description: 'Ad campaign creation and optimization', steps: ['Audience', 'Creatives', 'A/B Test', 'Optimization', 'Reporting'], category: 'Marketing', estimatedTime: '2h' },
    { id: 'influencer-outreach', name: 'Influencer Outreach', icon: '🌟', description: 'Influencer identification and outreach', steps: ['Research', 'Selection', 'Contact', 'Negotiation', 'Follow-up'], category: 'Marketing', estimatedTime: '3h' },
    { id: 'seo-audit', name: 'Complete SEO Audit', icon: '🔍', description: 'SEO analysis and optimization of your site', steps: ['Crawl', 'Analysis', 'Keywords', 'Recommendations', 'Tracking'], category: 'Marketing', estimatedTime: '4h' },
    // ===== SALES =====
    { id: 'sales-pipeline', name: 'Sales Pipeline', icon: '💼', description: 'Automated sales cycle management', steps: ['Prospecting', 'Qualification', 'Presentation', 'Negotiation', 'Closing'], category: 'Sales', estimatedTime: 'Ongoing' },
    { id: 'proposal-generator', name: 'Quote Generator', icon: '📋', description: 'Automatic creation of commercial proposals', steps: ['Brief', 'Pricing', 'Writing', 'Design', 'Sending'], category: 'Sales', estimatedTime: '45 min' },
    { id: 'follow-up-automation', name: 'Automatic Follow-ups', icon: '🔄', description: 'Automated customer follow-up sequences', steps: ['Segmentation', 'Sequence', 'Personalization', 'Sending', 'Analysis'], category: 'Sales', estimatedTime: '30 min' },
    { id: 'crm-sync', name: 'CRM Synchronization', icon: '🔗', description: 'Integration and synchronization with your CRM', steps: ['Connection', 'Mapping', 'Import', 'Automation', 'Reporting'], category: 'Sales', estimatedTime: '1h' },
    // ===== CUSTOMER SUPPORT =====
    { id: 'customer-support', name: 'AI Customer Support', icon: '💬', description: 'AI-powered customer support automation', steps: ['Reception', 'Classification', 'AI Response', 'Escalation', 'Follow-up'], category: 'Support', estimatedTime: '24/7' },
    { id: 'ticket-triage', name: 'Ticket Triage', icon: '🎫', description: 'Automatic support ticket classification', steps: ['Reception', 'Analysis', 'Category', 'Priority', 'Assignment'], category: 'Support', estimatedTime: 'Instant' },
    { id: 'faq-builder', name: 'FAQ Builder', icon: '❓', description: 'Automatic FAQ creation and updates', steps: ['Question Analysis', 'Grouping', 'Writing', 'Validation', 'Publication'], category: 'Support', estimatedTime: '2h' },
    { id: 'feedback-analysis', name: 'Feedback Analysis', icon: '📊', description: 'Automatic customer feedback analysis', steps: ['Collection', 'Sentiment', 'Categories', 'Insights', 'Actions'], category: 'Support', estimatedTime: '1h' },
    // ===== DATA =====
    { id: 'data-analysis', name: 'Data Analysis', icon: '📈', description: 'Complete data analysis pipeline', steps: ['Import', 'Cleaning', 'Analysis', 'Visualization', 'Report'], category: 'Data', estimatedTime: '2h' },
    { id: 'report-automation', name: 'Automatic Reports', icon: '📑', description: 'Automatic generation of periodic reports', steps: ['Sources', 'Aggregation', 'Analysis', 'Format', 'Distribution'], category: 'Data', estimatedTime: '30 min' },
    { id: 'competitor-monitoring', name: 'Competitor Monitoring', icon: '👁️', description: 'Automatic competitor surveillance', steps: ['Sources', 'Scraping', 'Analysis', 'Alerts', 'Report'], category: 'Data', estimatedTime: 'Ongoing' },
    { id: 'market-research', name: 'Market Research', icon: '🌍', description: 'Automated market research and analysis', steps: ['Definition', 'Collection', 'Analysis', 'Trends', 'Recommendations'], category: 'Data', estimatedTime: '4h' },
    // ===== HR =====
    { id: 'recruitment-flow', name: 'Automated Recruitment', icon: '👥', description: 'End-to-end recruitment pipeline', steps: ['Posting', 'Sourcing', 'Screening', 'Interviews', 'Onboarding'], category: 'HR', estimatedTime: 'Variable' },
    { id: 'cv-screening', name: 'CV Screening', icon: '📄', description: 'Automatic application analysis and sorting', steps: ['Reception', 'Parsing', 'Scoring', 'Ranking', 'Shortlist'], category: 'HR', estimatedTime: '5 min/CV' },
    { id: 'onboarding-flow', name: 'Employee Onboarding', icon: '🎯', description: 'Automated integration journey', steps: ['Welcome', 'Documents', 'Training', 'Equipment', 'Follow-up'], category: 'HR', estimatedTime: '1 week' },
    { id: 'performance-review', name: 'Performance Review', icon: '⭐', description: 'Annual evaluation process', steps: ['Self-eval', 'Manager', '360°', 'Summary', 'Action Plan'], category: 'HR', estimatedTime: '2h' },
    // ===== FINANCE =====
    { id: 'invoice-processing', name: 'Invoice Processing', icon: '🧾', description: 'Automated invoice processing', steps: ['Reception', 'OCR', 'Validation', 'Accounting', 'Payment'], category: 'Finance', estimatedTime: '2 min/invoice' },
    { id: 'expense-management', name: 'Expense Management', icon: '💳', description: 'Automated expense reports', steps: ['Submission', 'OCR', 'Category', 'Approval', 'Reimbursement'], category: 'Finance', estimatedTime: '1 min/report' },
    { id: 'budget-tracking', name: 'Budget Tracking', icon: '📊', description: 'Automatic budget monitoring', steps: ['Definition', 'Tracking', 'Alerts', 'Adjustments', 'Reporting'], category: 'Finance', estimatedTime: 'Ongoing' },
    { id: 'tax-preparation', name: 'Tax Preparation', icon: '🏛️', description: 'Tax return preparation', steps: ['Collection', 'Calculations', 'Verification', 'Declaration', 'Archiving'], category: 'Finance', estimatedTime: '4h' },
    // ===== E-COMMERCE =====
    { id: 'product-listing', name: 'Product Listing', icon: '🛍️', description: 'Automatic product sheet creation', steps: ['Import', 'Descriptions', 'Images', 'SEO', 'Publication'], category: 'E-Commerce', estimatedTime: '10 min/product' },
    { id: 'inventory-sync', name: 'Inventory Sync', icon: '📦', description: 'Multi-channel inventory synchronization', steps: ['Connection', 'Mapping', 'Sync', 'Alerts', 'Reports'], category: 'E-Commerce', estimatedTime: 'Real-time' },
    { id: 'abandoned-cart', name: 'Abandoned Carts', icon: '🛒', description: 'Automatic cart recovery', steps: ['Detection', 'Segmentation', 'Email 1', 'Email 2', 'Offer'], category: 'E-Commerce', estimatedTime: 'Auto' },
    { id: 'review-management', name: 'Review Management', icon: '⭐', description: 'Customer review collection and management', steps: ['Request', 'Collection', 'Moderation', 'Response', 'Analysis'], category: 'E-Commerce', estimatedTime: '15 min/day' },
    // ===== LEGAL =====
    { id: 'contract-review', name: 'Contract Review', icon: '⚖️', description: 'Automatic contract analysis', steps: ['Upload', 'OCR', 'Analysis', 'Risks', 'Recommendations'], category: 'Legal', estimatedTime: '30 min' },
    { id: 'compliance-check', name: 'Compliance Check', icon: '✅', description: 'Automated compliance audit', steps: ['Framework', 'Audit', 'Gaps', 'Actions', 'Report'], category: 'Legal', estimatedTime: '2h' },
    { id: 'gdpr-audit', name: 'Data Protection Audit', icon: '🔒', description: 'GDPR compliance audit', steps: ['Inventory', 'Analysis', 'Risks', 'Action Plan', 'Documentation'], category: 'Legal', estimatedTime: '1 day' },
  ],
};

// Fonction pour obtenir les workflows selon la langue
const getWorkflows = (lang: string): Workflow[] => {
  return workflowsData[lang] || workflowsData['fr'];
};

// Fonction pour obtenir les catégories selon la langue
const getCategories = (lang: string): string[] => {
  const workflows = getWorkflows(lang);
  return [...new Set(workflows.map((w: Workflow) => w.category))];
};

export default function Workflows() {
  const { t, lang } = useTranslation();
  const navigate = useNavigate();
  const [theme, setTheme] = useState<Theme>('dark');
  const isRTL = lang === 'ar';
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isLoggedIn] = useState(() => localStorage.getItem('isLoggedIn') === 'true');

  // Obtenir les workflows et catégories selon la langue
  const allWorkflows = getWorkflows(lang);
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

  // Filtrer les workflows
  const filteredWorkflows = allWorkflows.filter((workflow: Workflow) => {
    const matchesSearch = workflow.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          workflow.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || workflow.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Gérer le clic sur "Utiliser"
  const handleConnect = (workflowId: string) => {
    if (!isLoggedIn) {
      localStorage.setItem('redirectTool', `workflow-${workflowId}`);
      navigate('/login');
    } else {
      navigate(`/chat?workflow=${workflowId}`);
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
            {t('workflows_page_title')}
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto',
            }}
          >
            {allWorkflows.length} {t('workflows_page_subtitle')}
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
              placeholder={t('workflows_search')}
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
              {t('all')} ({allWorkflows.length})
            </button>
            {categories.map((cat) => {
              const count = allWorkflows.filter(w => w.category === cat).length;
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
          {filteredWorkflows.length} {filteredWorkflows.length > 1 ? t('workflows_found_plural') : t('workflows_found')} {t('found')}
        </p>

        {/* Workflows Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
            gap: '20px',
          }}
        >
          {filteredWorkflows.map((workflow) => (
            <div
              key={workflow.id}
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
                  justifyContent: 'space-between',
                  marginBottom: '16px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ fontSize: '32px' }}>{workflow.icon}</span>
                  <div>
                    <h3
                      style={{
                        fontSize: 'clamp(16px, 2.5vw, 18px)',
                        fontWeight: 600,
                        color: textColor,
                        margin: 0,
                      }}
                    >
                      {workflow.name}
                    </h3>
                    <span
                      style={{
                        fontSize: '12px',
                        color: accentColor,
                        fontWeight: 500,
                      }}
                    >
                      {workflow.category}
                    </span>
                  </div>
                </div>
                <span
                  style={{
                    background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
                    padding: '4px 10px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    color: textMuted,
                  }}
                >
                  {workflow.estimatedTime}
                </span>
              </div>

              {/* Description */}
              <p
                style={{
                  color: textMuted,
                  fontSize: '14px',
                  lineHeight: 1.6,
                  marginBottom: '16px',
                }}
              >
                {workflow.description}
              </p>

              {/* Steps */}
              <div style={{ marginBottom: '20px' }}>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    overflowX: 'auto',
                    padding: '8px 0',
                  }}
                >
                  {workflow.steps.map((step, idx) => (
                    <div key={step} style={{ display: 'flex', alignItems: 'center' }}>
                      <div
                        style={{
                          background: isDark ? 'rgba(34, 197, 94, 0.15)' : 'rgba(0, 98, 51, 0.1)',
                          border: `1px solid ${isDark ? 'rgba(34, 197, 94, 0.3)' : 'rgba(0, 98, 51, 0.3)'}`,
                          padding: '4px 10px',
                          borderRadius: '6px',
                          fontSize: '11px',
                          color: accentColor,
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {step}
                      </div>
                      {idx < workflow.steps.length - 1 && (
                        <span style={{ color: textMuted, margin: '0 2px', fontSize: '12px' }}>{isRTL ? '←' : '→'}</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Connect Button */}
              <button
                type="button"
                onClick={() => handleConnect(workflow.id)}
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
                    <span>{t('workflows_use_btn')}</span>
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
        {filteredWorkflows.length === 0 && (
          <div
            style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: textMuted,
            }}
          >
            <span style={{ fontSize: 'clamp(36px, 6vw, 48px)', display: 'block', marginBottom: '16px' }}>🔄</span>
            <p style={{ fontSize: 'clamp(16px, 2.5vw, 18px)' }}>{t('workflows_no_result')} "{searchQuery}"</p>
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
            background: isDark ? 'rgba(34, 197, 94, 0.08)' : 'rgba(0, 98, 51, 0.06)',
            borderRadius: '20px',
            padding: 'clamp(24px, 5vw, 48px)',
            textAlign: 'center',
            border: `1px solid ${borderColor}`,
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
            {t('workflows_custom_title')}
          </h2>
          <p
            style={{
              color: textMuted,
              fontSize: 'clamp(14px, 2.5vw, 16px)',
              maxWidth: '500px',
              margin: '0 auto 24px',
            }}
          >
            {t('workflows_custom_desc')}
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
            {isLoggedIn ? t('workflows_create') : t('workflows_request')}
          </button>
        </div>
      </div>
    </div>
  );
}
