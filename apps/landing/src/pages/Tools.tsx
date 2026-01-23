import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '../i18n';

type Theme = 'dark' | 'light';

interface Tool {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  categoryIcon: string;
}

// Liste complète des 262 outils IA classés par catégorie
const allTools: Tool[] = [
  // ===== RÉDACTION & CONTENU (30 outils) =====
  { id: 'article-generator', name: 'Générateur d\'Articles', description: 'Créez des articles de blog optimisés SEO', icon: '📝', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'seo-writer', name: 'Rédacteur SEO', description: 'Contenu optimisé pour les moteurs de recherche', icon: '🔍', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'title-creator', name: 'Créateur de Titres', description: 'Titres accrocheurs et viraux', icon: '💡', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'text-summarizer', name: 'Résumeur de Texte', description: 'Résumez n\'importe quel texte en points clés', icon: '📋', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'paraphraser', name: 'Paraphraseur', description: 'Reformulez vos textes avec différents styles', icon: '🔄', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'grammar-checker', name: 'Correcteur Grammaire', description: 'Corrigez les fautes de grammaire et orthographe', icon: '✅', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'essay-writer', name: 'Rédacteur d\'Essais', description: 'Rédigez des essais structurés', icon: '📖', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'blog-ideas', name: 'Idées de Blog', description: 'Générez des idées de contenu pour votre blog', icon: '💭', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'content-rewriter', name: 'Réécriture de Contenu', description: 'Réécrivez du contenu existant', icon: '✏️', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'headline-analyzer', name: 'Analyseur de Titres', description: 'Analysez l\'efficacité de vos titres', icon: '📊', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'meta-description', name: 'Meta Descriptions', description: 'Créez des meta descriptions optimisées', icon: '🏷️', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'press-release', name: 'Communiqués de Presse', description: 'Rédigez des communiqués professionnels', icon: '📰', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'speech-writer', name: 'Rédacteur de Discours', description: 'Créez des discours impactants', icon: '🎤', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'storyteller', name: 'Conteur IA', description: 'Générez des histoires captivantes', icon: '📚', category: 'Rédaction', categoryIcon: '✍️' },
  { id: 'slogan-generator', name: 'Générateur de Slogans', description: 'Créez des slogans mémorables', icon: '🎯', category: 'Rédaction', categoryIcon: '✍️' },

  // ===== TRADUCTION (15 outils) =====
  { id: 'translator-fr-ar', name: 'Traducteur FR→AR', description: 'Traduction Français vers Arabe', icon: '🇫🇷🇩🇿', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'translator-ar-fr', name: 'Traducteur AR→FR', description: 'Traduction Arabe vers Français', icon: '🇩🇿🇫🇷', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'translator-en-fr', name: 'Traducteur EN→FR', description: 'Traduction Anglais vers Français', icon: '🇬🇧🇫🇷', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'translator-fr-en', name: 'Traducteur FR→EN', description: 'Traduction Français vers Anglais', icon: '🇫🇷🇬🇧', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'translator-multi', name: 'Traducteur Multi-Langues', description: 'Traduction vers 100+ langues', icon: '🌐', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'translator-darija', name: 'Traducteur Darija', description: 'Traduction dialecte algérien', icon: '🇩🇿', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'translator-tamazight', name: 'Traducteur Tamazight', description: 'Traduction berbère/kabyle', icon: 'ⵣ', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'document-translator', name: 'Traducteur Documents', description: 'Traduisez des documents entiers', icon: '📄', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'website-translator', name: 'Traducteur Sites Web', description: 'Localisez votre site web', icon: '🖥️', category: 'Traduction', categoryIcon: '🌍' },
  { id: 'subtitle-translator', name: 'Traducteur Sous-titres', description: 'Traduisez des fichiers SRT/VTT', icon: '🎬', category: 'Traduction', categoryIcon: '🌍' },

  // ===== RÉSEAUX SOCIAUX (25 outils) =====
  { id: 'instagram-posts', name: 'Posts Instagram', description: 'Créez des posts Instagram engageants', icon: '📸', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'instagram-reels', name: 'Scripts Reels', description: 'Scripts pour Instagram Reels', icon: '🎞️', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'instagram-stories', name: 'Stories Instagram', description: 'Idées et textes pour Stories', icon: '⭕', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'twitter-threads', name: 'Threads Twitter/X', description: 'Créez des threads viraux', icon: '🐦', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'twitter-posts', name: 'Posts Twitter/X', description: 'Tweets optimisés pour l\'engagement', icon: '✖️', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'linkedin-posts', name: 'Posts LinkedIn', description: 'Contenu professionnel pour LinkedIn', icon: '💼', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'linkedin-articles', name: 'Articles LinkedIn', description: 'Articles longs pour LinkedIn', icon: '📰', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'tiktok-scripts', name: 'Scripts TikTok', description: 'Scripts pour vidéos TikTok virales', icon: '🎵', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'tiktok-captions', name: 'Légendes TikTok', description: 'Descriptions accrocheuses TikTok', icon: '📝', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'facebook-posts', name: 'Posts Facebook', description: 'Publications Facebook optimisées', icon: '👍', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'facebook-ads', name: 'Publicités Facebook', description: 'Textes publicitaires Facebook', icon: '💰', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'hashtag-generator', name: 'Générateur Hashtags', description: 'Hashtags pertinents et tendance', icon: '#️⃣', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'bio-generator', name: 'Générateur Bio', description: 'Bios professionnelles pour profils', icon: '👤', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'social-calendar', name: 'Calendrier Social', description: 'Planifiez votre contenu social', icon: '📅', category: 'Réseaux Sociaux', categoryIcon: '📱' },
  { id: 'engagement-booster', name: 'Booster Engagement', description: 'Augmentez l\'engagement de vos posts', icon: '🚀', category: 'Réseaux Sociaux', categoryIcon: '📱' },

  // ===== YOUTUBE (20 outils) =====
  { id: 'youtube-titles', name: 'Titres YouTube', description: 'Titres viraux pour vos vidéos', icon: '🎬', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-descriptions', name: 'Descriptions YouTube', description: 'Descriptions optimisées SEO', icon: '📝', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-scripts', name: 'Scripts Vidéo', description: 'Scripts complets pour vidéos', icon: '📜', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-tags', name: 'Tags YouTube', description: 'Tags optimisés pour le référencement', icon: '🏷️', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-thumbnails', name: 'Idées Miniatures', description: 'Concepts de miniatures accrocheuses', icon: '🖼️', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-ideas', name: 'Idées de Vidéos', description: 'Générez des idées de contenu', icon: '💡', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-shorts', name: 'Scripts Shorts', description: 'Scripts pour YouTube Shorts', icon: '📱', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-hooks', name: 'Hooks Vidéo', description: 'Accroches captivantes pour débuts', icon: '🪝', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-cta', name: 'Appels à l\'Action', description: 'CTAs efficaces pour vos vidéos', icon: '🎯', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-analytics', name: 'Analyse YouTube', description: 'Analysez vos performances', icon: '📊', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-chapters', name: 'Chapitres Vidéo', description: 'Créez des chapitres automatiques', icon: '📑', category: 'YouTube', categoryIcon: '▶️' },
  { id: 'youtube-comments', name: 'Réponses Commentaires', description: 'Répondez aux commentaires rapidement', icon: '💬', category: 'YouTube', categoryIcon: '▶️' },

  // ===== E-COMMERCE (25 outils) =====
  { id: 'product-descriptions', name: 'Descriptions Produits', description: 'Fiches produits qui vendent', icon: '🛍️', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'product-titles', name: 'Titres Produits', description: 'Titres optimisés marketplace', icon: '📦', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'sales-copy', name: 'Copywriting Vente', description: 'Textes de vente persuasifs', icon: '💰', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'email-marketing', name: 'Emails Marketing', description: 'Campagnes email qui convertissent', icon: '📧', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'landing-pages', name: 'Pages de Vente', description: 'Textes pour landing pages', icon: '🎯', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'faq-generator', name: 'Générateur FAQ', description: 'FAQs automatiques pour produits', icon: '❓', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'review-responder', name: 'Réponses Avis', description: 'Répondez aux avis clients', icon: '⭐', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'abandoned-cart', name: 'Emails Panier Abandonné', description: 'Récupérez les paniers abandonnés', icon: '🛒', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'upsell-copy', name: 'Textes Upsell', description: 'Augmentez le panier moyen', icon: '📈', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'category-descriptions', name: 'Descriptions Catégories', description: 'Textes pour pages catégories', icon: '📂', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'promo-announcements', name: 'Annonces Promos', description: 'Communications promotionnelles', icon: '🎉', category: 'E-Commerce', categoryIcon: '🛒' },
  { id: 'shipping-policies', name: 'Politiques Livraison', description: 'Textes de politique de livraison', icon: '🚚', category: 'E-Commerce', categoryIcon: '🛒' },

  // ===== ADMINISTRATION ALGÉRIE (20 outils) =====
  { id: 'cnas-agent', name: 'Agent CNAS', description: 'Aide pour démarches CNAS', icon: '🏥', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'casnos-agent', name: 'Agent CASNOS', description: 'Guide CASNOS pour indépendants', icon: '👷', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'tax-agent', name: 'Agent Impôts', description: 'Déclarations fiscales IRG/IBS', icon: '💵', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'cnrc-agent', name: 'Agent CNRC', description: 'Registre du commerce algérien', icon: '📋', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'customs-agent', name: 'Agent Douanes', description: 'Procédures douanières', icon: '🛃', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'anem-agent', name: 'Agent ANEM', description: 'Aide à l\'emploi ANEM', icon: '💼', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'ansej-agent', name: 'Agent ANSEJ/ANADE', description: 'Création d\'entreprise jeunes', icon: '🚀', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'andi-agent', name: 'Agent ANDI', description: 'Investissements en Algérie', icon: '📈', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'sonelgaz-agent', name: 'Agent Sonelgaz', description: 'Démarches électricité/gaz', icon: '⚡', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'seaal-agent', name: 'Agent SEAAL', description: 'Démarches eau', icon: '💧', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'cpa-agent', name: 'Agent CPA', description: 'Services bancaires CPA', icon: '🏦', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'bna-agent', name: 'Agent BNA', description: 'Services bancaires BNA', icon: '🏦', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'passport-agent', name: 'Agent Passeport', description: 'Demande de passeport biométrique', icon: '🛂', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'cni-agent', name: 'Agent CNI', description: 'Carte nationale d\'identité', icon: '🪪', category: 'Admin Algérie', categoryIcon: '🇩🇿' },
  { id: 'permis-agent', name: 'Agent Permis', description: 'Permis de conduire', icon: '🚗', category: 'Admin Algérie', categoryIcon: '🇩🇿' },

  // ===== ÉDUCATION ALGÉRIE (20 outils) =====
  { id: 'bac-revision', name: 'Révision BAC', description: 'Préparation au baccalauréat', icon: '🎓', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'bem-prep', name: 'Prépa BEM', description: 'Préparation au BEM', icon: '📝', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'cinq-prep', name: 'Prépa 5ème', description: 'Examen de 5ème année primaire', icon: '✏️', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'qcm-generator', name: 'Générateur QCM', description: 'Créez des QCM automatiques', icon: '✅', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'course-sheets', name: 'Fiches de Cours', description: 'Fiches de révision synthétiques', icon: '📋', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'corrected-exercises', name: 'Exercices Corrigés', description: 'Exercices avec corrections détaillées', icon: '✍️', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'math-solver', name: 'Solveur Maths', description: 'Résolution de problèmes mathématiques', icon: '🔢', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'physics-helper', name: 'Aide Physique', description: 'Explications physique-chimie', icon: '⚗️', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'arabic-grammar', name: 'Grammaire Arabe', description: 'Règles de grammaire arabe', icon: '🔤', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'french-grammar', name: 'Grammaire Française', description: 'Cours de français', icon: '🇫🇷', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'english-learning', name: 'Apprentissage Anglais', description: 'Cours d\'anglais interactifs', icon: '🇬🇧', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'history-geo', name: 'Histoire-Géo', description: 'Cours histoire et géographie', icon: '🌍', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'islamic-studies', name: 'Sciences Islamiques', description: 'Cours de sciences islamiques', icon: '☪️', category: 'Éducation DZ', categoryIcon: '📚' },
  { id: 'dissertation-helper', name: 'Aide Dissertation', description: 'Structure et rédaction dissertations', icon: '📄', category: 'Éducation DZ', categoryIcon: '📚' },

  // ===== GÉNÉRATION D'IMAGES (20 outils) =====
  { id: 'image-generator', name: 'Générateur Images', description: 'Créez des images avec l\'IA', icon: '🎨', category: 'Images', categoryIcon: '🖼️' },
  { id: 'logo-maker', name: 'Créateur de Logos', description: 'Logos professionnels en secondes', icon: '✨', category: 'Images', categoryIcon: '🖼️' },
  { id: 'avatar-generator', name: 'Générateur Avatars', description: 'Avatars personnalisés', icon: '👤', category: 'Images', categoryIcon: '🖼️' },
  { id: 'background-remover', name: 'Suppression Fond', description: 'Retirez l\'arrière-plan des images', icon: '🔲', category: 'Images', categoryIcon: '🖼️' },
  { id: 'image-upscaler', name: 'Agrandisseur Images', description: 'Augmentez la résolution', icon: '🔍', category: 'Images', categoryIcon: '🖼️' },
  { id: 'image-editor', name: 'Éditeur Images IA', description: 'Retouchez avec l\'intelligence artificielle', icon: '🖌️', category: 'Images', categoryIcon: '🖼️' },
  { id: 'mockup-generator', name: 'Générateur Mockups', description: 'Mockups pour vos designs', icon: '📱', category: 'Images', categoryIcon: '🖼️' },
  { id: 'infographic-maker', name: 'Créateur Infographies', description: 'Infographies automatiques', icon: '📊', category: 'Images', categoryIcon: '🖼️' },
  { id: 'social-graphics', name: 'Visuels Réseaux Sociaux', description: 'Images pour posts sociaux', icon: '📸', category: 'Images', categoryIcon: '🖼️' },
  { id: 'banner-maker', name: 'Créateur Bannières', description: 'Bannières web et publicitaires', icon: '🏳️', category: 'Images', categoryIcon: '🖼️' },
  { id: 'thumbnail-maker', name: 'Créateur Miniatures', description: 'Miniatures YouTube et vidéos', icon: '🎬', category: 'Images', categoryIcon: '🖼️' },
  { id: 'qr-generator', name: 'Générateur QR Code', description: 'QR codes personnalisés', icon: '📲', category: 'Images', categoryIcon: '🖼️' },

  // ===== AUDIO & VOIX (15 outils) =====
  { id: 'text-to-speech', name: 'Texte vers Voix', description: 'Convertissez du texte en audio', icon: '🔊', category: 'Audio', categoryIcon: '🎵' },
  { id: 'speech-to-text', name: 'Voix vers Texte', description: 'Transcription audio automatique', icon: '🎤', category: 'Audio', categoryIcon: '🎵' },
  { id: 'voice-cloning', name: 'Clonage Vocal', description: 'Clonez une voix pour vos contenus', icon: '👥', category: 'Audio', categoryIcon: '🎵' },
  { id: 'podcast-generator', name: 'Générateur Podcast', description: 'Créez des podcasts automatiques', icon: '🎙️', category: 'Audio', categoryIcon: '🎵' },
  { id: 'audio-enhancer', name: 'Amélioration Audio', description: 'Améliorez la qualité audio', icon: '✨', category: 'Audio', categoryIcon: '🎵' },
  { id: 'noise-remover', name: 'Suppression Bruit', description: 'Retirez le bruit de fond', icon: '🔇', category: 'Audio', categoryIcon: '🎵' },
  { id: 'music-generator', name: 'Générateur Musique', description: 'Créez de la musique avec l\'IA', icon: '🎶', category: 'Audio', categoryIcon: '🎵' },
  { id: 'audiobook-creator', name: 'Créateur Audiobooks', description: 'Transformez livres en audio', icon: '📖', category: 'Audio', categoryIcon: '🎵' },
  { id: 'voice-changer', name: 'Changeur de Voix', description: 'Modifiez le ton et le style vocal', icon: '🎭', category: 'Audio', categoryIcon: '🎵' },
  { id: 'jingle-maker', name: 'Créateur Jingles', description: 'Jingles et musiques courtes', icon: '🔔', category: 'Audio', categoryIcon: '🎵' },

  // ===== VIDÉO (15 outils) =====
  { id: 'video-generator', name: 'Générateur Vidéo', description: 'Créez des vidéos avec l\'IA', icon: '🎬', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'video-editor', name: 'Éditeur Vidéo IA', description: 'Montage vidéo automatique', icon: '✂️', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'subtitle-generator', name: 'Générateur Sous-titres', description: 'Sous-titres automatiques', icon: '💬', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'video-summarizer', name: 'Résumeur Vidéo', description: 'Résumez des vidéos longues', icon: '📋', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'clip-maker', name: 'Créateur de Clips', description: 'Extraits viraux automatiques', icon: '📱', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'avatar-video', name: 'Vidéo Avatar', description: 'Vidéos avec avatars IA', icon: '🤖', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'video-translator', name: 'Traducteur Vidéo', description: 'Traduisez vos vidéos', icon: '🌐', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'intro-maker', name: 'Créateur Intros', description: 'Intros professionnelles', icon: '🎭', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'outro-maker', name: 'Créateur Outros', description: 'Outros et écrans de fin', icon: '🔚', category: 'Vidéo', categoryIcon: '🎥' },
  { id: 'video-effects', name: 'Effets Vidéo IA', description: 'Effets visuels automatiques', icon: '✨', category: 'Vidéo', categoryIcon: '🎥' },

  // ===== CODE & DÉVELOPPEMENT (20 outils) =====
  { id: 'code-generator', name: 'Générateur de Code', description: 'Générez du code en langage naturel', icon: '💻', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'code-reviewer', name: 'Revue de Code', description: 'Analysez et améliorez votre code', icon: '🔍', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'bug-fixer', name: 'Correcteur de Bugs', description: 'Trouvez et corrigez les bugs', icon: '🐛', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'code-explainer', name: 'Expliqueur de Code', description: 'Comprenez du code complexe', icon: '📖', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'sql-generator', name: 'Générateur SQL', description: 'Requêtes SQL automatiques', icon: '🗄️', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'api-generator', name: 'Générateur API', description: 'Créez des APIs rapidement', icon: '🔌', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'regex-helper', name: 'Aide Regex', description: 'Expressions régulières simplifiées', icon: '🔤', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'unit-test-generator', name: 'Générateur Tests', description: 'Tests unitaires automatiques', icon: '✅', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'documentation-generator', name: 'Générateur Docs', description: 'Documentation automatique', icon: '📚', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'code-converter', name: 'Convertisseur Code', description: 'Convertissez entre langages', icon: '🔄', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'json-formatter', name: 'Formateur JSON', description: 'Formatez et validez JSON', icon: '📋', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'html-generator', name: 'Générateur HTML', description: 'HTML depuis une description', icon: '🌐', category: 'Code', categoryIcon: '👨‍💻' },
  { id: 'css-generator', name: 'Générateur CSS', description: 'Styles CSS automatiques', icon: '🎨', category: 'Code', categoryIcon: '👨‍💻' },

  // ===== BUSINESS & PROFESSIONNEL (25 outils) =====
  { id: 'business-plan', name: 'Plan d\'Affaires', description: 'Générez un business plan complet', icon: '📊', category: 'Business', categoryIcon: '💼' },
  { id: 'market-study', name: 'Étude de Marché', description: 'Analysez votre marché cible', icon: '📈', category: 'Business', categoryIcon: '💼' },
  { id: 'swot-analysis', name: 'Analyse SWOT', description: 'Forces, faiblesses, opportunités, menaces', icon: '🎯', category: 'Business', categoryIcon: '💼' },
  { id: 'pitch-deck', name: 'Pitch Deck', description: 'Présentations pour investisseurs', icon: '🎤', category: 'Business', categoryIcon: '💼' },
  { id: 'meeting-notes', name: 'Notes de Réunion', description: 'Résumés automatiques de réunions', icon: '📝', category: 'Business', categoryIcon: '💼' },
  { id: 'project-proposal', name: 'Proposition Projet', description: 'Propositions commerciales', icon: '📄', category: 'Business', categoryIcon: '💼' },
  { id: 'contract-generator', name: 'Générateur Contrats', description: 'Contrats types personnalisables', icon: '📜', category: 'Business', categoryIcon: '💼' },
  { id: 'invoice-maker', name: 'Créateur Factures', description: 'Factures professionnelles', icon: '🧾', category: 'Business', categoryIcon: '💼' },
  { id: 'report-generator', name: 'Générateur Rapports', description: 'Rapports d\'activité automatiques', icon: '📊', category: 'Business', categoryIcon: '💼' },
  { id: 'kpi-dashboard', name: 'Tableau de Bord KPI', description: 'Suivez vos indicateurs clés', icon: '📉', category: 'Business', categoryIcon: '💼' },
  { id: 'competitor-analysis', name: 'Analyse Concurrence', description: 'Analysez vos concurrents', icon: '🔍', category: 'Business', categoryIcon: '💼' },
  { id: 'pricing-strategy', name: 'Stratégie Prix', description: 'Optimisez votre pricing', icon: '💰', category: 'Business', categoryIcon: '💼' },
  { id: 'brand-voice', name: 'Voix de Marque', description: 'Définissez votre identité verbale', icon: '🗣️', category: 'Business', categoryIcon: '💼' },

  // ===== JURIDIQUE (15 outils) =====
  { id: 'legal-contract', name: 'Contrats Juridiques', description: 'Rédigez des contrats légaux', icon: '⚖️', category: 'Juridique', categoryIcon: '📜' },
  { id: 'nda-generator', name: 'Générateur NDA', description: 'Accords de confidentialité', icon: '🤐', category: 'Juridique', categoryIcon: '📜' },
  { id: 'terms-conditions', name: 'CGU/CGV', description: 'Conditions générales', icon: '📋', category: 'Juridique', categoryIcon: '📜' },
  { id: 'privacy-policy', name: 'Politique Confidentialité', description: 'RGPD et protection des données', icon: '🔒', category: 'Juridique', categoryIcon: '📜' },
  { id: 'legal-letter', name: 'Lettres Juridiques', description: 'Mises en demeure et courriers', icon: '✉️', category: 'Juridique', categoryIcon: '📜' },
  { id: 'trademark-search', name: 'Recherche Marque', description: 'Vérifiez la disponibilité d\'une marque', icon: '®️', category: 'Juridique', categoryIcon: '📜' },
  { id: 'legal-summary', name: 'Résumé Juridique', description: 'Simplifiez des textes de loi', icon: '📖', category: 'Juridique', categoryIcon: '📜' },
  { id: 'complaint-letter', name: 'Lettres de Réclamation', description: 'Réclamations formelles', icon: '📨', category: 'Juridique', categoryIcon: '📜' },

  // ===== RESSOURCES HUMAINES (15 outils) =====
  { id: 'job-description', name: 'Offres d\'Emploi', description: 'Rédigez des offres attractives', icon: '📢', category: 'RH', categoryIcon: '👥' },
  { id: 'cv-analyzer', name: 'Analyseur CV', description: 'Analysez les candidatures', icon: '📄', category: 'RH', categoryIcon: '👥' },
  { id: 'interview-questions', name: 'Questions Entretien', description: 'Questions d\'entretien pertinentes', icon: '❓', category: 'RH', categoryIcon: '👥' },
  { id: 'onboarding-plan', name: 'Plan Onboarding', description: 'Intégration nouveaux employés', icon: '🎯', category: 'RH', categoryIcon: '👥' },
  { id: 'performance-review', name: 'Évaluation Performance', description: 'Évaluations annuelles', icon: '⭐', category: 'RH', categoryIcon: '👥' },
  { id: 'training-plan', name: 'Plan Formation', description: 'Programmes de formation', icon: '📚', category: 'RH', categoryIcon: '👥' },
  { id: 'employee-handbook', name: 'Livret Employé', description: 'Manuel d\'entreprise', icon: '📘', category: 'RH', categoryIcon: '👥' },
  { id: 'termination-letter', name: 'Lettres de Fin Contrat', description: 'Fins de contrat professionnelles', icon: '📝', category: 'RH', categoryIcon: '👥' },

  // ===== EMAILS & COMMUNICATION (15 outils) =====
  { id: 'email-writer', name: 'Rédacteur Emails', description: 'Emails professionnels parfaits', icon: '📧', category: 'Emails', categoryIcon: '✉️' },
  { id: 'cold-email', name: 'Cold Emails', description: 'Emails de prospection', icon: '❄️', category: 'Emails', categoryIcon: '✉️' },
  { id: 'follow-up-email', name: 'Emails de Relance', description: 'Relances efficaces', icon: '🔄', category: 'Emails', categoryIcon: '✉️' },
  { id: 'thank-you-email', name: 'Emails Remerciement', description: 'Remerciements professionnels', icon: '🙏', category: 'Emails', categoryIcon: '✉️' },
  { id: 'newsletter-writer', name: 'Rédacteur Newsletter', description: 'Newsletters engageantes', icon: '📰', category: 'Emails', categoryIcon: '✉️' },
  { id: 'email-subject', name: 'Objets d\'Email', description: 'Sujets qui font ouvrir', icon: '📌', category: 'Emails', categoryIcon: '✉️' },
  { id: 'apology-email', name: 'Emails d\'Excuse', description: 'Excuses professionnelles', icon: '🙇', category: 'Emails', categoryIcon: '✉️' },
  { id: 'invitation-email', name: 'Emails d\'Invitation', description: 'Invitations événements', icon: '🎉', category: 'Emails', categoryIcon: '✉️' },

  // ===== CHAT & ASSISTANTS (10 outils) =====
  { id: 'chatbot-builder', name: 'Créateur Chatbot', description: 'Créez votre chatbot personnalisé', icon: '🤖', category: 'Chat', categoryIcon: '💬' },
  { id: 'customer-support', name: 'Support Client IA', description: 'Répondez aux clients 24/7', icon: '🎧', category: 'Chat', categoryIcon: '💬' },
  { id: 'faq-chatbot', name: 'Chatbot FAQ', description: 'Réponses automatiques FAQ', icon: '❓', category: 'Chat', categoryIcon: '💬' },
  { id: 'sales-assistant', name: 'Assistant Vente', description: 'Aidez vos prospects à acheter', icon: '💰', category: 'Chat', categoryIcon: '💬' },
  { id: 'booking-assistant', name: 'Assistant Réservation', description: 'Gérez les réservations', icon: '📅', category: 'Chat', categoryIcon: '💬' },
  { id: 'lead-qualifier', name: 'Qualificateur Leads', description: 'Qualifiez automatiquement les leads', icon: '🎯', category: 'Chat', categoryIcon: '💬' },

  // ===== ANALYSE & DONNÉES (15 outils) =====
  { id: 'data-analyzer', name: 'Analyseur Données', description: 'Analysez vos données avec l\'IA', icon: '📊', category: 'Données', categoryIcon: '📈' },
  { id: 'sentiment-analyzer', name: 'Analyse Sentiments', description: 'Analysez les opinions et avis', icon: '😊', category: 'Données', categoryIcon: '📈' },
  { id: 'trend-detector', name: 'Détecteur Tendances', description: 'Identifiez les tendances', icon: '📈', category: 'Données', categoryIcon: '📈' },
  { id: 'survey-analyzer', name: 'Analyseur Sondages', description: 'Analysez les réponses sondages', icon: '📋', category: 'Données', categoryIcon: '📈' },
  { id: 'review-analyzer', name: 'Analyseur Avis', description: 'Synthétisez les avis clients', icon: '⭐', category: 'Données', categoryIcon: '📈' },
  { id: 'keyword-research', name: 'Recherche Mots-clés', description: 'Trouvez les meilleurs mots-clés', icon: '🔑', category: 'Données', categoryIcon: '📈' },
  { id: 'competitor-monitor', name: 'Veille Concurrentielle', description: 'Surveillez vos concurrents', icon: '👁️', category: 'Données', categoryIcon: '📈' },
  { id: 'price-tracker', name: 'Suivi Prix', description: 'Surveillez les prix du marché', icon: '💵', category: 'Données', categoryIcon: '📈' },
];

// Catégories uniques pour le filtre
const categories = [...new Set(allTools.map(t => t.category))];

export default function Tools() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [theme, setTheme] = useState<Theme>('dark');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isLoggedIn] = useState(() => {
    return localStorage.getItem('isLoggedIn') === 'true';
  });

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

  // Filtrer les outils
  const filteredTools = allTools.filter(tool => {
    const matchesSearch = tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          tool.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || tool.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Gérer le clic sur "Connecter"
  const handleConnect = (toolId: string) => {
    if (!isLoggedIn) {
      // Sauvegarder l'outil demandé pour redirection après login
      localStorage.setItem('redirectTool', toolId);
      navigate('/login', { replace: true });
    } else {
      // Ouvrir l'outil dans le chat
      navigate(`/chat?tool=${toolId}`);
    }
  };

  const isDark = theme === 'dark';
  const bgColor = isDark ? '#1a1a1a' : '#FAF9F7';
  const cardBg = isDark ? '#262626' : '#ffffff';
  const textColor = isDark ? '#f0f0f0' : '#1F1F1F';
  const textMuted = isDark ? '#A3A3A3' : '#5D5D5D';
  const borderColor = isDark ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.08)';
  const inputBg = isDark ? '#1f1f1f' : '#ffffff';

  return (
    <div
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
            {t('tools_title') || '262 Outils IA'}
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto',
            }}
          >
            {t('tools_subtitle') || 'Tous les outils IA dont vous avez besoin, accessibles en un clic'}
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
              placeholder="Rechercher un outil..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '14px 20px 14px 50px',
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
                left: '18px',
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
                border: `1px solid ${selectedCategory === 'all' ? '#00A86B' : borderColor}`,
                background: selectedCategory === 'all' ? 'rgba(0, 168, 107, 0.15)' : 'transparent',
                color: selectedCategory === 'all' ? '#00A86B' : textMuted,
                fontSize: '14px',
                fontWeight: 500,
                cursor: 'pointer',
              }}
            >
              Tous ({allTools.length})
            </button>
            {categories.map((cat) => {
              const count = allTools.filter(t => t.category === cat).length;
              const catIcon = allTools.find(t => t.category === cat)?.categoryIcon || '📁';
              return (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setSelectedCategory(cat)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '20px',
                    border: `1px solid ${selectedCategory === cat ? '#00A86B' : borderColor}`,
                    background: selectedCategory === cat ? 'rgba(0, 168, 107, 0.15)' : 'transparent',
                    color: selectedCategory === cat ? '#00A86B' : textMuted,
                    fontSize: '14px',
                    fontWeight: 500,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <span>{catIcon}</span>
                  {cat} ({count})
                </button>
              );
            })}
          </div>
        </div>

        {/* Results Count */}
        <p style={{ color: textMuted, marginBottom: '24px', textAlign: 'center' }}>
          {filteredTools.length} outil{filteredTools.length > 1 ? 's' : ''} trouvé{filteredTools.length > 1 ? 's' : ''}
        </p>

        {/* Tools Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '20px',
          }}
        >
          {filteredTools.map((tool) => (
            <div
              key={tool.id}
              style={{
                background: cardBg,
                borderRadius: '16px',
                padding: '24px',
                border: `1px solid ${borderColor}`,
                transition: 'all 0.3s ease',
                cursor: 'pointer',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.borderColor = '#00A86B';
                e.currentTarget.style.boxShadow = '0 12px 24px rgba(0, 168, 107, 0.15)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.borderColor = borderColor;
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              {/* Icon & Category */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: '16px',
                }}
              >
                <div
                  style={{
                    width: '56px',
                    height: '56px',
                    borderRadius: '14px',
                    background: isDark ? 'rgba(0, 168, 107, 0.1)' : 'rgba(0, 168, 107, 0.08)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '28px',
                  }}
                >
                  {tool.icon}
                </div>
                <span
                  style={{
                    background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
                    padding: '4px 10px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    color: textMuted,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                  }}
                >
                  {tool.categoryIcon} {tool.category}
                </span>
              </div>

              {/* Name & Description */}
              <h3
                style={{
                  fontSize: 'clamp(16px, 2.5vw, 18px)',
                  fontWeight: 600,
                  color: textColor,
                  marginBottom: '8px',
                }}
              >
                {tool.name}
              </h3>
              <p
                style={{
                  color: textMuted,
                  fontSize: '14px',
                  lineHeight: 1.5,
                  marginBottom: '20px',
                  minHeight: '42px',
                }}
              >
                {tool.description}
              </p>

              {/* Connect Button */}
              <button
                type="button"
                onClick={() => handleConnect(tool.id)}
                style={{
                  width: '100%',
                  padding: '12px',
                  background: 'linear-gradient(135deg, #00A86B, #2ECC71)',
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
                    <span>Utiliser</span>
                    <span>→</span>
                  </>
                ) : (
                  <>
                    <span>🔗</span>
                    <span>Connecter</span>
                  </>
                )}
              </button>
            </div>
          ))}
        </div>

        {/* No Results */}
        {filteredTools.length === 0 && (
          <div
            style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: textMuted,
            }}
          >
            <span style={{ fontSize: 'clamp(36px, 6vw, 48px)', display: 'block', marginBottom: '16px' }}>🔍</span>
            <p style={{ fontSize: 'clamp(16px, 2.5vw, 18px)' }}>{t('tools_no_result') || 'Aucun outil trouvé pour'} "{searchQuery}"</p>
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
              Réinitialiser les filtres
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
            border: `2px solid #00A86B`,
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
            {isLoggedIn ? t('tools_cta_logged') || 'Accédez à tous les outils' : t('tools_cta_guest') || 'Connectez-vous pour utiliser les outils'}
          </h2>
          <p
            style={{
              color: textMuted,
              fontSize: 'clamp(14px, 2.5vw, 16px)',
              maxWidth: '500px',
              margin: '0 auto 24px',
            }}
          >
            {isLoggedIn
              ? t('tools_cta_logged_desc') || 'Profitez de 262 outils IA pour booster votre productivité'
              : t('tools_cta_guest_desc') || 'Créez un compte gratuit et accédez à tous nos outils IA'}
          </p>
          <a
            href={isLoggedIn ? '/chat' : '/login'}
            style={{
              display: 'inline-block',
              padding: 'clamp(12px, 2vw, 16px) clamp(24px, 4vw, 32px)',
              background: 'linear-gradient(135deg, #00A86B, #2ECC71)',
              color: '#fff',
              fontSize: 'clamp(14px, 2.5vw, 18px)',
              fontWeight: 600,
              textDecoration: 'none',
              borderRadius: '12px',
              boxShadow: '0 4px 16px rgba(0, 168, 107, 0.3)',
            }}
          >
            {isLoggedIn ? t('tools_open_chat') || 'Ouvrir le Chat IA' : t('tools_create_account') || 'Créer un compte gratuit'}
          </a>
        </div>
      </div>
    </div>
  );
}
