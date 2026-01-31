import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '../i18n';
import { useTheme } from '../hooks';

// ============================================================================
// TYPES
// ============================================================================
interface Tool {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  categoryIcon: string;
  featured?: boolean;
}

// Données des outils par langue (FR)
const toolsFR: Tool[] = [
  // ===== RÉDACTION & CONTENU (30 outils) =====
  { id: 'article-generator', name: 'Générateur d\'Articles', description: 'Créez des articles de blog optimisés SEO', icon: '📝', category: 'Rédaction', categoryIcon: '✍️', featured: true },
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
  { id: 'image-generator', name: 'Générateur Images', description: 'Créez des images avec l\'IA', icon: '🎨', category: 'Images', categoryIcon: '🖼️', featured: true },
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
  { id: 'code-generator', name: 'Générateur de Code', description: 'Générez du code en langage naturel', icon: '💻', category: 'Code', categoryIcon: '👨‍💻', featured: true },
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

// Traduction des catégories
const categoryTranslations: Record<string, Record<string, string>> = {
  'Rédaction': { ar: 'الكتابة', en: 'Writing' },
  'Traduction': { ar: 'الترجمة', en: 'Translation' },
  'Réseaux Sociaux': { ar: 'وسائل التواصل', en: 'Social Media' },
  'YouTube': { ar: 'يوتيوب', en: 'YouTube' },
  'E-Commerce': { ar: 'التجارة الإلكترونية', en: 'E-Commerce' },
  'Admin Algérie': { ar: 'الإدارة الجزائرية', en: 'Algeria Admin' },
  'Éducation DZ': { ar: 'التعليم الجزائري', en: 'DZ Education' },
  'Images': { ar: 'الصور', en: 'Images' },
  'Audio': { ar: 'الصوت', en: 'Audio' },
  'Vidéo': { ar: 'الفيديو', en: 'Video' },
  'Code': { ar: 'البرمجة', en: 'Code' },
  'Business': { ar: 'الأعمال', en: 'Business' },
  'Juridique': { ar: 'القانون', en: 'Legal' },
  'RH': { ar: 'الموارد البشرية', en: 'HR' },
  'Emails': { ar: 'البريد الإلكتروني', en: 'Emails' },
  'Chat': { ar: 'الدردشة', en: 'Chat' },
  'Données': { ar: 'البيانات', en: 'Data' },
};

// Traduction des noms et descriptions des outils
const toolTranslations: Record<string, { ar: { name: string; description: string }; en: { name: string; description: string } }> = {
  'article-generator': { ar: { name: 'منشئ المقالات', description: 'أنشئ مقالات مدونة محسنة لمحركات البحث' }, en: { name: 'Article Generator', description: 'Create SEO-optimized blog articles' } },
  'seo-writer': { ar: { name: 'كاتب SEO', description: 'محتوى محسن لمحركات البحث' }, en: { name: 'SEO Writer', description: 'Search engine optimized content' } },
  'title-creator': { ar: { name: 'منشئ العناوين', description: 'عناوين جذابة وفيروسية' }, en: { name: 'Title Creator', description: 'Catchy and viral titles' } },
  'text-summarizer': { ar: { name: 'ملخص النصوص', description: 'لخص أي نص في نقاط رئيسية' }, en: { name: 'Text Summarizer', description: 'Summarize any text into key points' } },
  'paraphraser': { ar: { name: 'معيد الصياغة', description: 'أعد صياغة نصوصك بأساليب مختلفة' }, en: { name: 'Paraphraser', description: 'Rephrase your texts with different styles' } },
  'grammar-checker': { ar: { name: 'مصحح القواعد', description: 'صحح الأخطاء النحوية والإملائية' }, en: { name: 'Grammar Checker', description: 'Fix grammar and spelling mistakes' } },
  'essay-writer': { ar: { name: 'كاتب المقالات', description: 'اكتب مقالات منظمة' }, en: { name: 'Essay Writer', description: 'Write structured essays' } },
  'blog-ideas': { ar: { name: 'أفكار المدونة', description: 'أنشئ أفكار محتوى لمدونتك' }, en: { name: 'Blog Ideas', description: 'Generate content ideas for your blog' } },
  'content-rewriter': { ar: { name: 'إعادة كتابة المحتوى', description: 'أعد كتابة المحتوى الموجود' }, en: { name: 'Content Rewriter', description: 'Rewrite existing content' } },
  'headline-analyzer': { ar: { name: 'محلل العناوين', description: 'حلل فعالية عناوينك' }, en: { name: 'Headline Analyzer', description: 'Analyze headline effectiveness' } },
  'meta-description': { ar: { name: 'وصف الميتا', description: 'أنشئ أوصاف ميتا محسنة' }, en: { name: 'Meta Descriptions', description: 'Create optimized meta descriptions' } },
  'press-release': { ar: { name: 'البيانات الصحفية', description: 'اكتب بيانات صحفية احترافية' }, en: { name: 'Press Releases', description: 'Write professional press releases' } },
  'speech-writer': { ar: { name: 'كاتب الخطابات', description: 'أنشئ خطابات مؤثرة' }, en: { name: 'Speech Writer', description: 'Create impactful speeches' } },
  'storyteller': { ar: { name: 'راوي القصص', description: 'أنشئ قصصاً جذابة' }, en: { name: 'AI Storyteller', description: 'Generate captivating stories' } },
  'slogan-generator': { ar: { name: 'منشئ الشعارات', description: 'أنشئ شعارات لا تُنسى' }, en: { name: 'Slogan Generator', description: 'Create memorable slogans' } },
  'translator-fr-ar': { ar: { name: 'مترجم فرنسي-عربي', description: 'ترجمة من الفرنسية إلى العربية' }, en: { name: 'FR→AR Translator', description: 'French to Arabic translation' } },
  'translator-ar-fr': { ar: { name: 'مترجم عربي-فرنسي', description: 'ترجمة من العربية إلى الفرنسية' }, en: { name: 'AR→FR Translator', description: 'Arabic to French translation' } },
  'translator-en-fr': { ar: { name: 'مترجم إنجليزي-فرنسي', description: 'ترجمة من الإنجليزية إلى الفرنسية' }, en: { name: 'EN→FR Translator', description: 'English to French translation' } },
  'translator-fr-en': { ar: { name: 'مترجم فرنسي-إنجليزي', description: 'ترجمة من الفرنسية إلى الإنجليزية' }, en: { name: 'FR→EN Translator', description: 'French to English translation' } },
  'translator-multi': { ar: { name: 'مترجم متعدد اللغات', description: 'ترجمة إلى أكثر من 100 لغة' }, en: { name: 'Multi-Language Translator', description: 'Translation to 100+ languages' } },
  'translator-darija': { ar: { name: 'مترجم الدارجة', description: 'ترجمة اللهجة الجزائرية' }, en: { name: 'Darija Translator', description: 'Algerian dialect translation' } },
  'translator-tamazight': { ar: { name: 'مترجم الأمازيغية', description: 'ترجمة البربرية/القبائلية' }, en: { name: 'Tamazight Translator', description: 'Berber/Kabyle translation' } },
  'document-translator': { ar: { name: 'مترجم المستندات', description: 'ترجم مستندات كاملة' }, en: { name: 'Document Translator', description: 'Translate entire documents' } },
  'website-translator': { ar: { name: 'مترجم المواقع', description: 'ترجم موقعك الإلكتروني' }, en: { name: 'Website Translator', description: 'Localize your website' } },
  'subtitle-translator': { ar: { name: 'مترجم الترجمات', description: 'ترجم ملفات SRT/VTT' }, en: { name: 'Subtitle Translator', description: 'Translate SRT/VTT files' } },
  'instagram-posts': { ar: { name: 'منشورات إنستغرام', description: 'أنشئ منشورات إنستغرام جذابة' }, en: { name: 'Instagram Posts', description: 'Create engaging Instagram posts' } },
  'instagram-reels': { ar: { name: 'نصوص Reels', description: 'نصوص لـ Instagram Reels' }, en: { name: 'Reels Scripts', description: 'Scripts for Instagram Reels' } },
  'instagram-stories': { ar: { name: 'قصص إنستغرام', description: 'أفكار ونصوص للقصص' }, en: { name: 'Instagram Stories', description: 'Ideas and texts for Stories' } },
  'twitter-threads': { ar: { name: 'سلاسل تويتر', description: 'أنشئ سلاسل فيروسية' }, en: { name: 'Twitter/X Threads', description: 'Create viral threads' } },
  'twitter-posts': { ar: { name: 'منشورات تويتر', description: 'تغريدات محسنة للتفاعل' }, en: { name: 'Twitter/X Posts', description: 'Engagement-optimized tweets' } },
  'linkedin-posts': { ar: { name: 'منشورات لينكد إن', description: 'محتوى احترافي للينكد إن' }, en: { name: 'LinkedIn Posts', description: 'Professional LinkedIn content' } },
  'linkedin-articles': { ar: { name: 'مقالات لينكد إن', description: 'مقالات طويلة للينكد إن' }, en: { name: 'LinkedIn Articles', description: 'Long-form LinkedIn articles' } },
  'tiktok-scripts': { ar: { name: 'نصوص تيك توك', description: 'نصوص لفيديوهات تيك توك الفيروسية' }, en: { name: 'TikTok Scripts', description: 'Scripts for viral TikTok videos' } },
  'tiktok-captions': { ar: { name: 'تعليقات تيك توك', description: 'أوصاف جذابة لتيك توك' }, en: { name: 'TikTok Captions', description: 'Catchy TikTok descriptions' } },
  'facebook-posts': { ar: { name: 'منشورات فيسبوك', description: 'منشورات فيسبوك محسنة' }, en: { name: 'Facebook Posts', description: 'Optimized Facebook posts' } },
  'facebook-ads': { ar: { name: 'إعلانات فيسبوك', description: 'نصوص إعلانية لفيسبوك' }, en: { name: 'Facebook Ads', description: 'Facebook advertising copy' } },
  'hashtag-generator': { ar: { name: 'منشئ الهاشتاغات', description: 'هاشتاغات ذات صلة ورائجة' }, en: { name: 'Hashtag Generator', description: 'Relevant and trending hashtags' } },
  'bio-generator': { ar: { name: 'منشئ السيرة', description: 'سير احترافية للملفات الشخصية' }, en: { name: 'Bio Generator', description: 'Professional profile bios' } },
  'social-calendar': { ar: { name: 'التقويم الاجتماعي', description: 'خطط محتواك الاجتماعي' }, en: { name: 'Social Calendar', description: 'Plan your social content' } },
  'engagement-booster': { ar: { name: 'معزز التفاعل', description: 'زد تفاعل منشوراتك' }, en: { name: 'Engagement Booster', description: 'Increase post engagement' } },
  'youtube-titles': { ar: { name: 'عناوين يوتيوب', description: 'عناوين فيروسية لفيديوهاتك' }, en: { name: 'YouTube Titles', description: 'Viral titles for your videos' } },
  'youtube-descriptions': { ar: { name: 'أوصاف يوتيوب', description: 'أوصاف محسنة لمحركات البحث' }, en: { name: 'YouTube Descriptions', description: 'SEO-optimized descriptions' } },
  'youtube-scripts': { ar: { name: 'نصوص الفيديو', description: 'نصوص كاملة للفيديوهات' }, en: { name: 'Video Scripts', description: 'Complete video scripts' } },
  'youtube-tags': { ar: { name: 'وسوم يوتيوب', description: 'وسوم محسنة للظهور' }, en: { name: 'YouTube Tags', description: 'Optimized tags for ranking' } },
  'youtube-thumbnails': { ar: { name: 'أفكار الصور المصغرة', description: 'مفاهيم صور مصغرة جذابة' }, en: { name: 'Thumbnail Ideas', description: 'Catchy thumbnail concepts' } },
  'youtube-ideas': { ar: { name: 'أفكار الفيديوهات', description: 'أنشئ أفكار محتوى' }, en: { name: 'Video Ideas', description: 'Generate content ideas' } },
  'youtube-shorts': { ar: { name: 'نصوص Shorts', description: 'نصوص لـ YouTube Shorts' }, en: { name: 'Shorts Scripts', description: 'Scripts for YouTube Shorts' } },
  'youtube-hooks': { ar: { name: 'مقدمات الفيديو', description: 'مقدمات جذابة للبدايات' }, en: { name: 'Video Hooks', description: 'Captivating intro hooks' } },
  'youtube-cta': { ar: { name: 'دعوات للعمل', description: 'CTAs فعالة لفيديوهاتك' }, en: { name: 'Calls to Action', description: 'Effective CTAs for videos' } },
  'youtube-analytics': { ar: { name: 'تحليل يوتيوب', description: 'حلل أداءك' }, en: { name: 'YouTube Analytics', description: 'Analyze your performance' } },
  'youtube-chapters': { ar: { name: 'فصول الفيديو', description: 'أنشئ فصولاً تلقائية' }, en: { name: 'Video Chapters', description: 'Create automatic chapters' } },
  'youtube-comments': { ar: { name: 'ردود التعليقات', description: 'رد على التعليقات بسرعة' }, en: { name: 'Comment Responses', description: 'Respond to comments quickly' } },
  'product-descriptions': { ar: { name: 'أوصاف المنتجات', description: 'بطاقات منتجات تبيع' }, en: { name: 'Product Descriptions', description: 'Product cards that sell' } },
  'product-titles': { ar: { name: 'عناوين المنتجات', description: 'عناوين محسنة للسوق' }, en: { name: 'Product Titles', description: 'Marketplace-optimized titles' } },
  'sales-copy': { ar: { name: 'نصوص البيع', description: 'نصوص بيع مقنعة' }, en: { name: 'Sales Copy', description: 'Persuasive sales texts' } },
  'email-marketing': { ar: { name: 'التسويق بالبريد', description: 'حملات بريد تحول' }, en: { name: 'Email Marketing', description: 'Campaigns that convert' } },
  'landing-pages': { ar: { name: 'صفحات الهبوط', description: 'نصوص لصفحات الهبوط' }, en: { name: 'Landing Pages', description: 'Landing page texts' } },
  'faq-generator': { ar: { name: 'منشئ الأسئلة الشائعة', description: 'أسئلة شائعة تلقائية للمنتجات' }, en: { name: 'FAQ Generator', description: 'Auto FAQs for products' } },
  'review-responder': { ar: { name: 'ردود المراجعات', description: 'رد على مراجعات العملاء' }, en: { name: 'Review Responses', description: 'Respond to customer reviews' } },
  'abandoned-cart': { ar: { name: 'رسائل السلة المتروكة', description: 'استعد السلات المتروكة' }, en: { name: 'Abandoned Cart Emails', description: 'Recover abandoned carts' } },
  'upsell-copy': { ar: { name: 'نصوص البيع الإضافي', description: 'زد متوسط السلة' }, en: { name: 'Upsell Copy', description: 'Increase average cart' } },
  'category-descriptions': { ar: { name: 'أوصاف الفئات', description: 'نصوص لصفحات الفئات' }, en: { name: 'Category Descriptions', description: 'Category page texts' } },
  'promo-announcements': { ar: { name: 'إعلانات العروض', description: 'اتصالات ترويجية' }, en: { name: 'Promo Announcements', description: 'Promotional communications' } },
  'shipping-policies': { ar: { name: 'سياسات الشحن', description: 'نصوص سياسة التوصيل' }, en: { name: 'Shipping Policies', description: 'Delivery policy texts' } },
  'cnas-agent': { ar: { name: 'وكيل الضمان الاجتماعي', description: 'مساعدة لإجراءات CNAS' }, en: { name: 'CNAS Agent', description: 'Help with CNAS procedures' } },
  'casnos-agent': { ar: { name: 'وكيل كاسنوس', description: 'دليل CASNOS للمستقلين' }, en: { name: 'CASNOS Agent', description: 'CASNOS guide for freelancers' } },
  'tax-agent': { ar: { name: 'وكيل الضرائب', description: 'تصريحات ضريبية IRG/IBS' }, en: { name: 'Tax Agent', description: 'IRG/IBS tax returns' } },
  'cnrc-agent': { ar: { name: 'وكيل السجل التجاري', description: 'السجل التجاري الجزائري' }, en: { name: 'CNRC Agent', description: 'Algerian trade registry' } },
  'customs-agent': { ar: { name: 'وكيل الجمارك', description: 'الإجراءات الجمركية' }, en: { name: 'Customs Agent', description: 'Customs procedures' } },
  'anem-agent': { ar: { name: 'وكيل أنام', description: 'مساعدة التوظيف من أنام' }, en: { name: 'ANEM Agent', description: 'ANEM employment help' } },
  'ansej-agent': { ar: { name: 'وكيل أناد', description: 'إنشاء مؤسسات الشباب' }, en: { name: 'ANADE Agent', description: 'Youth business creation' } },
  'andi-agent': { ar: { name: 'وكيل أندي', description: 'الاستثمارات في الجزائر' }, en: { name: 'ANDI Agent', description: 'Investments in Algeria' } },
  'sonelgaz-agent': { ar: { name: 'وكيل سونلغاز', description: 'إجراءات الكهرباء/الغاز' }, en: { name: 'Sonelgaz Agent', description: 'Electricity/gas procedures' } },
  'seaal-agent': { ar: { name: 'وكيل سيال', description: 'إجراءات المياه' }, en: { name: 'SEAAL Agent', description: 'Water procedures' } },
  'cpa-agent': { ar: { name: 'وكيل CPA', description: 'خدمات بنك CPA' }, en: { name: 'CPA Agent', description: 'CPA banking services' } },
  'bna-agent': { ar: { name: 'وكيل BNA', description: 'خدمات بنك BNA' }, en: { name: 'BNA Agent', description: 'BNA banking services' } },
  'passport-agent': { ar: { name: 'وكيل جواز السفر', description: 'طلب جواز السفر البيومتري' }, en: { name: 'Passport Agent', description: 'Biometric passport request' } },
  'cni-agent': { ar: { name: 'وكيل بطاقة الهوية', description: 'بطاقة التعريف الوطنية' }, en: { name: 'ID Card Agent', description: 'National ID card' } },
  'permis-agent': { ar: { name: 'وكيل رخصة القيادة', description: 'رخصة القيادة' }, en: { name: 'License Agent', description: 'Driving license' } },
  'bac-revision': { ar: { name: 'مراجعة البكالوريا', description: 'التحضير لشهادة البكالوريا' }, en: { name: 'BAC Revision', description: 'Baccalaureate preparation' } },
  'bem-prep': { ar: { name: 'تحضير شهادة التعليم المتوسط', description: 'التحضير لشهادة BEM' }, en: { name: 'BEM Prep', description: 'BEM preparation' } },
  'cinq-prep': { ar: { name: 'تحضير السنة الخامسة', description: 'امتحان السنة الخامسة ابتدائي' }, en: { name: '5th Year Prep', description: '5th year primary exam' } },
  'qcm-generator': { ar: { name: 'منشئ الاختيارات المتعددة', description: 'أنشئ اختبارات QCM تلقائية' }, en: { name: 'MCQ Generator', description: 'Create automatic MCQs' } },
  'course-sheets': { ar: { name: 'ملخصات الدروس', description: 'ملخصات مراجعة مركزة' }, en: { name: 'Course Sheets', description: 'Synthetic revision sheets' } },
  'corrected-exercises': { ar: { name: 'تمارين محلولة', description: 'تمارين مع حلول مفصلة' }, en: { name: 'Corrected Exercises', description: 'Exercises with detailed solutions' } },
  'math-solver': { ar: { name: 'حلال الرياضيات', description: 'حل المسائل الرياضية' }, en: { name: 'Math Solver', description: 'Math problem solving' } },
  'physics-helper': { ar: { name: 'مساعد الفيزياء', description: 'شروحات الفيزياء والكيمياء' }, en: { name: 'Physics Helper', description: 'Physics-chemistry explanations' } },
  'arabic-grammar': { ar: { name: 'قواعد العربية', description: 'قواعد اللغة العربية' }, en: { name: 'Arabic Grammar', description: 'Arabic grammar rules' } },
  'french-grammar': { ar: { name: 'قواعد الفرنسية', description: 'دروس اللغة الفرنسية' }, en: { name: 'French Grammar', description: 'French language courses' } },
  'english-learning': { ar: { name: 'تعلم الإنجليزية', description: 'دروس إنجليزية تفاعلية' }, en: { name: 'English Learning', description: 'Interactive English courses' } },
  'history-geo': { ar: { name: 'التاريخ والجغرافيا', description: 'دروس التاريخ والجغرافيا' }, en: { name: 'History-Geo', description: 'History and geography courses' } },
  'islamic-studies': { ar: { name: 'العلوم الإسلامية', description: 'دروس العلوم الإسلامية' }, en: { name: 'Islamic Studies', description: 'Islamic studies courses' } },
  'dissertation-helper': { ar: { name: 'مساعد المقالات', description: 'هيكلة وكتابة المقالات' }, en: { name: 'Dissertation Helper', description: 'Essay structure and writing' } },
  'image-generator': { ar: { name: 'منشئ الصور', description: 'أنشئ صوراً بالذكاء الاصطناعي' }, en: { name: 'Image Generator', description: 'Create images with AI' } },
  'logo-maker': { ar: { name: 'منشئ الشعارات', description: 'شعارات احترافية في ثوانٍ' }, en: { name: 'Logo Maker', description: 'Professional logos in seconds' } },
  'avatar-generator': { ar: { name: 'منشئ الأفاتار', description: 'أفاتارات مخصصة' }, en: { name: 'Avatar Generator', description: 'Customized avatars' } },
  'background-remover': { ar: { name: 'إزالة الخلفية', description: 'أزل خلفية الصور' }, en: { name: 'Background Remover', description: 'Remove image backgrounds' } },
  'image-upscaler': { ar: { name: 'مكبر الصور', description: 'زد دقة الصور' }, en: { name: 'Image Upscaler', description: 'Increase resolution' } },
  'image-editor': { ar: { name: 'محرر الصور الذكي', description: 'عدّل بالذكاء الاصطناعي' }, en: { name: 'AI Image Editor', description: 'Edit with AI' } },
  'mockup-generator': { ar: { name: 'منشئ النماذج', description: 'نماذج لتصاميمك' }, en: { name: 'Mockup Generator', description: 'Mockups for your designs' } },
  'infographic-maker': { ar: { name: 'منشئ الإنفوغرافيك', description: 'إنفوغرافيك تلقائي' }, en: { name: 'Infographic Maker', description: 'Automatic infographics' } },
  'social-graphics': { ar: { name: 'صور التواصل الاجتماعي', description: 'صور للمنشورات الاجتماعية' }, en: { name: 'Social Graphics', description: 'Images for social posts' } },
  'banner-maker': { ar: { name: 'منشئ البانرات', description: 'بانرات ويب وإعلانية' }, en: { name: 'Banner Maker', description: 'Web and ad banners' } },
  'thumbnail-maker': { ar: { name: 'منشئ الصور المصغرة', description: 'صور مصغرة يوتيوب وفيديو' }, en: { name: 'Thumbnail Maker', description: 'YouTube and video thumbnails' } },
  'qr-generator': { ar: { name: 'منشئ رمز QR', description: 'رموز QR مخصصة' }, en: { name: 'QR Code Generator', description: 'Customized QR codes' } },
  'text-to-speech': { ar: { name: 'نص إلى صوت', description: 'حوّل النص إلى صوت' }, en: { name: 'Text to Speech', description: 'Convert text to audio' } },
  'speech-to-text': { ar: { name: 'صوت إلى نص', description: 'نسخ صوتي تلقائي' }, en: { name: 'Speech to Text', description: 'Automatic audio transcription' } },
  'voice-cloning': { ar: { name: 'استنساخ الصوت', description: 'استنسخ صوتاً لمحتواك' }, en: { name: 'Voice Cloning', description: 'Clone a voice for your content' } },
  'podcast-generator': { ar: { name: 'منشئ البودكاست', description: 'أنشئ بودكاست تلقائي' }, en: { name: 'Podcast Generator', description: 'Create automatic podcasts' } },
  'audio-enhancer': { ar: { name: 'محسّن الصوت', description: 'حسّن جودة الصوت' }, en: { name: 'Audio Enhancer', description: 'Improve audio quality' } },
  'noise-remover': { ar: { name: 'إزالة الضوضاء', description: 'أزل الضوضاء الخلفية' }, en: { name: 'Noise Remover', description: 'Remove background noise' } },
  'music-generator': { ar: { name: 'منشئ الموسيقى', description: 'أنشئ موسيقى بالذكاء الاصطناعي' }, en: { name: 'Music Generator', description: 'Create music with AI' } },
  'audiobook-creator': { ar: { name: 'منشئ الكتب الصوتية', description: 'حوّل الكتب إلى صوت' }, en: { name: 'Audiobook Creator', description: 'Transform books to audio' } },
  'voice-changer': { ar: { name: 'مغيّر الصوت', description: 'غيّر نبرة وأسلوب الصوت' }, en: { name: 'Voice Changer', description: 'Change voice tone and style' } },
  'jingle-maker': { ar: { name: 'منشئ الجلجل', description: 'جلجل وموسيقى قصيرة' }, en: { name: 'Jingle Maker', description: 'Jingles and short music' } },
  'video-generator': { ar: { name: 'منشئ الفيديو', description: 'أنشئ فيديوهات بالذكاء الاصطناعي' }, en: { name: 'Video Generator', description: 'Create videos with AI' } },
  'video-editor': { ar: { name: 'محرر الفيديو الذكي', description: 'مونتاج فيديو تلقائي' }, en: { name: 'AI Video Editor', description: 'Automatic video editing' } },
  'subtitle-generator': { ar: { name: 'منشئ الترجمات', description: 'ترجمات تلقائية' }, en: { name: 'Subtitle Generator', description: 'Automatic subtitles' } },
  'video-summarizer': { ar: { name: 'ملخص الفيديو', description: 'لخّص فيديوهات طويلة' }, en: { name: 'Video Summarizer', description: 'Summarize long videos' } },
  'clip-maker': { ar: { name: 'منشئ المقاطع', description: 'مقاطع فيروسية تلقائية' }, en: { name: 'Clip Maker', description: 'Automatic viral clips' } },
  'avatar-video': { ar: { name: 'فيديو الأفاتار', description: 'فيديوهات بأفاتارات ذكية' }, en: { name: 'Avatar Video', description: 'Videos with AI avatars' } },
  'video-translator': { ar: { name: 'مترجم الفيديو', description: 'ترجم فيديوهاتك' }, en: { name: 'Video Translator', description: 'Translate your videos' } },
  'intro-maker': { ar: { name: 'منشئ المقدمات', description: 'مقدمات احترافية' }, en: { name: 'Intro Maker', description: 'Professional intros' } },
  'outro-maker': { ar: { name: 'منشئ الخاتمات', description: 'خاتمات وشاشات نهاية' }, en: { name: 'Outro Maker', description: 'Outros and end screens' } },
  'video-effects': { ar: { name: 'مؤثرات الفيديو', description: 'مؤثرات بصرية تلقائية' }, en: { name: 'Video Effects', description: 'Automatic visual effects' } },
  'code-generator': { ar: { name: 'منشئ الكود', description: 'أنشئ كوداً بلغة طبيعية' }, en: { name: 'Code Generator', description: 'Generate code in natural language' } },
  'code-reviewer': { ar: { name: 'مراجع الكود', description: 'حلّل وحسّن كودك' }, en: { name: 'Code Reviewer', description: 'Analyze and improve your code' } },
  'bug-fixer': { ar: { name: 'مصلح الأخطاء', description: 'اعثر على الأخطاء وأصلحها' }, en: { name: 'Bug Fixer', description: 'Find and fix bugs' } },
  'code-explainer': { ar: { name: 'شارح الكود', description: 'افهم كوداً معقداً' }, en: { name: 'Code Explainer', description: 'Understand complex code' } },
  'sql-generator': { ar: { name: 'منشئ SQL', description: 'استعلامات SQL تلقائية' }, en: { name: 'SQL Generator', description: 'Automatic SQL queries' } },
  'api-generator': { ar: { name: 'منشئ API', description: 'أنشئ APIs بسرعة' }, en: { name: 'API Generator', description: 'Create APIs quickly' } },
  'regex-helper': { ar: { name: 'مساعد Regex', description: 'تعبيرات منتظمة مبسطة' }, en: { name: 'Regex Helper', description: 'Simplified regular expressions' } },
  'unit-test-generator': { ar: { name: 'منشئ الاختبارات', description: 'اختبارات وحدة تلقائية' }, en: { name: 'Test Generator', description: 'Automatic unit tests' } },
  'documentation-generator': { ar: { name: 'منشئ التوثيق', description: 'توثيق تلقائي' }, en: { name: 'Docs Generator', description: 'Automatic documentation' } },
  'code-converter': { ar: { name: 'محوّل الكود', description: 'حوّل بين اللغات' }, en: { name: 'Code Converter', description: 'Convert between languages' } },
  'json-formatter': { ar: { name: 'منسق JSON', description: 'نسّق وتحقق من JSON' }, en: { name: 'JSON Formatter', description: 'Format and validate JSON' } },
  'html-generator': { ar: { name: 'منشئ HTML', description: 'HTML من الوصف' }, en: { name: 'HTML Generator', description: 'HTML from description' } },
  'css-generator': { ar: { name: 'منشئ CSS', description: 'أنماط CSS تلقائية' }, en: { name: 'CSS Generator', description: 'Automatic CSS styles' } },
  'business-plan': { ar: { name: 'خطة العمل', description: 'أنشئ خطة عمل كاملة' }, en: { name: 'Business Plan', description: 'Generate a complete business plan' } },
  'market-study': { ar: { name: 'دراسة السوق', description: 'حلّل سوقك المستهدف' }, en: { name: 'Market Study', description: 'Analyze your target market' } },
  'swot-analysis': { ar: { name: 'تحليل SWOT', description: 'نقاط القوة والضعف والفرص والتهديدات' }, en: { name: 'SWOT Analysis', description: 'Strengths, weaknesses, opportunities, threats' } },
  'pitch-deck': { ar: { name: 'عرض المشروع', description: 'عروض للمستثمرين' }, en: { name: 'Pitch Deck', description: 'Presentations for investors' } },
  'meeting-notes': { ar: { name: 'ملاحظات الاجتماع', description: 'ملخصات اجتماعات تلقائية' }, en: { name: 'Meeting Notes', description: 'Automatic meeting summaries' } },
  'project-proposal': { ar: { name: 'اقتراح المشروع', description: 'عروض تجارية' }, en: { name: 'Project Proposal', description: 'Commercial proposals' } },
  'contract-generator': { ar: { name: 'منشئ العقود', description: 'عقود نموذجية قابلة للتخصيص' }, en: { name: 'Contract Generator', description: 'Customizable contract templates' } },
  'invoice-maker': { ar: { name: 'منشئ الفواتير', description: 'فواتير احترافية' }, en: { name: 'Invoice Maker', description: 'Professional invoices' } },
  'report-generator': { ar: { name: 'منشئ التقارير', description: 'تقارير نشاط تلقائية' }, en: { name: 'Report Generator', description: 'Automatic activity reports' } },
  'kpi-dashboard': { ar: { name: 'لوحة مؤشرات الأداء', description: 'تتبع مؤشراتك الرئيسية' }, en: { name: 'KPI Dashboard', description: 'Track your key indicators' } },
  'competitor-analysis': { ar: { name: 'تحليل المنافسة', description: 'حلّل منافسيك' }, en: { name: 'Competitor Analysis', description: 'Analyze your competitors' } },
  'pricing-strategy': { ar: { name: 'استراتيجية التسعير', description: 'حسّن تسعيرك' }, en: { name: 'Pricing Strategy', description: 'Optimize your pricing' } },
  'brand-voice': { ar: { name: 'صوت العلامة', description: 'حدد هويتك اللفظية' }, en: { name: 'Brand Voice', description: 'Define your verbal identity' } },
  'legal-contract': { ar: { name: 'العقود القانونية', description: 'اكتب عقوداً قانونية' }, en: { name: 'Legal Contracts', description: 'Write legal contracts' } },
  'nda-generator': { ar: { name: 'منشئ اتفاقية السرية', description: 'اتفاقيات السرية' }, en: { name: 'NDA Generator', description: 'Confidentiality agreements' } },
  'terms-conditions': { ar: { name: 'الشروط والأحكام', description: 'الشروط العامة' }, en: { name: 'Terms & Conditions', description: 'General conditions' } },
  'privacy-policy': { ar: { name: 'سياسة الخصوصية', description: 'حماية البيانات الشخصية' }, en: { name: 'Privacy Policy', description: 'Personal data protection' } },
  'legal-letter': { ar: { name: 'الرسائل القانونية', description: 'إنذارات ومراسلات' }, en: { name: 'Legal Letters', description: 'Notices and correspondence' } },
  'trademark-search': { ar: { name: 'بحث العلامة التجارية', description: 'تحقق من توفر العلامة' }, en: { name: 'Trademark Search', description: 'Check trademark availability' } },
  'legal-summary': { ar: { name: 'الملخص القانوني', description: 'بسّط النصوص القانونية' }, en: { name: 'Legal Summary', description: 'Simplify legal texts' } },
  'complaint-letter': { ar: { name: 'رسائل الشكوى', description: 'شكاوى رسمية' }, en: { name: 'Complaint Letters', description: 'Formal complaints' } },
  'job-description': { ar: { name: 'عروض العمل', description: 'اكتب عروضاً جذابة' }, en: { name: 'Job Descriptions', description: 'Write attractive offers' } },
  'cv-analyzer': { ar: { name: 'محلل السيرة الذاتية', description: 'حلّل الترشيحات' }, en: { name: 'CV Analyzer', description: 'Analyze applications' } },
  'interview-questions': { ar: { name: 'أسئلة المقابلة', description: 'أسئلة مقابلة ذات صلة' }, en: { name: 'Interview Questions', description: 'Relevant interview questions' } },
  'onboarding-plan': { ar: { name: 'خطة الإدماج', description: 'إدماج الموظفين الجدد' }, en: { name: 'Onboarding Plan', description: 'New employee integration' } },
  'performance-review': { ar: { name: 'تقييم الأداء', description: 'التقييمات السنوية' }, en: { name: 'Performance Review', description: 'Annual evaluations' } },
  'training-plan': { ar: { name: 'خطة التدريب', description: 'برامج التدريب' }, en: { name: 'Training Plan', description: 'Training programs' } },
  'employee-handbook': { ar: { name: 'دليل الموظف', description: 'دليل الشركة' }, en: { name: 'Employee Handbook', description: 'Company manual' } },
  'termination-letter': { ar: { name: 'رسائل إنهاء العقد', description: 'إنهاء عقود احترافي' }, en: { name: 'Termination Letters', description: 'Professional contract endings' } },
  'email-writer': { ar: { name: 'كاتب البريد الإلكتروني', description: 'رسائل احترافية مثالية' }, en: { name: 'Email Writer', description: 'Perfect professional emails' } },
  'cold-email': { ar: { name: 'رسائل التنقيب', description: 'رسائل تنقيب' }, en: { name: 'Cold Emails', description: 'Prospecting emails' } },
  'follow-up-email': { ar: { name: 'رسائل المتابعة', description: 'متابعات فعالة' }, en: { name: 'Follow-up Emails', description: 'Effective follow-ups' } },
  'thank-you-email': { ar: { name: 'رسائل الشكر', description: 'شكر احترافي' }, en: { name: 'Thank You Emails', description: 'Professional thanks' } },
  'newsletter-writer': { ar: { name: 'كاتب النشرة الإخبارية', description: 'نشرات إخبارية جذابة' }, en: { name: 'Newsletter Writer', description: 'Engaging newsletters' } },
  'email-subject': { ar: { name: 'مواضيع البريد', description: 'مواضيع تفتح الرسائل' }, en: { name: 'Email Subjects', description: 'Subjects that get opened' } },
  'apology-email': { ar: { name: 'رسائل الاعتذار', description: 'اعتذارات احترافية' }, en: { name: 'Apology Emails', description: 'Professional apologies' } },
  'invitation-email': { ar: { name: 'رسائل الدعوة', description: 'دعوات الفعاليات' }, en: { name: 'Invitation Emails', description: 'Event invitations' } },
  'chatbot-builder': { ar: { name: 'منشئ روبوت المحادثة', description: 'أنشئ روبوت محادثة مخصص' }, en: { name: 'Chatbot Builder', description: 'Create your custom chatbot' } },
  'customer-support': { ar: { name: 'دعم العملاء الذكي', description: 'رد على العملاء 24/7' }, en: { name: 'AI Customer Support', description: 'Respond to customers 24/7' } },
  'faq-chatbot': { ar: { name: 'روبوت الأسئلة الشائعة', description: 'ردود تلقائية للأسئلة' }, en: { name: 'FAQ Chatbot', description: 'Automatic FAQ responses' } },
  'sales-assistant': { ar: { name: 'مساعد المبيعات', description: 'ساعد عملاءك المحتملين على الشراء' }, en: { name: 'Sales Assistant', description: 'Help your prospects buy' } },
  'booking-assistant': { ar: { name: 'مساعد الحجز', description: 'أدر الحجوزات' }, en: { name: 'Booking Assistant', description: 'Manage reservations' } },
  'lead-qualifier': { ar: { name: 'مؤهل العملاء المحتملين', description: 'أهّل العملاء المحتملين تلقائياً' }, en: { name: 'Lead Qualifier', description: 'Automatically qualify leads' } },
  'data-analyzer': { ar: { name: 'محلل البيانات', description: 'حلّل بياناتك بالذكاء الاصطناعي' }, en: { name: 'Data Analyzer', description: 'Analyze your data with AI' } },
  'sentiment-analyzer': { ar: { name: 'محلل المشاعر', description: 'حلّل الآراء والتعليقات' }, en: { name: 'Sentiment Analyzer', description: 'Analyze opinions and reviews' } },
  'trend-detector': { ar: { name: 'كاشف الاتجاهات', description: 'حدد الاتجاهات' }, en: { name: 'Trend Detector', description: 'Identify trends' } },
  'survey-analyzer': { ar: { name: 'محلل الاستبيانات', description: 'حلّل ردود الاستبيانات' }, en: { name: 'Survey Analyzer', description: 'Analyze survey responses' } },
  'review-analyzer': { ar: { name: 'محلل المراجعات', description: 'لخّص مراجعات العملاء' }, en: { name: 'Review Analyzer', description: 'Synthesize customer reviews' } },
  'keyword-research': { ar: { name: 'بحث الكلمات المفتاحية', description: 'اعثر على أفضل الكلمات المفتاحية' }, en: { name: 'Keyword Research', description: 'Find the best keywords' } },
  'competitor-monitor': { ar: { name: 'مراقبة المنافسين', description: 'راقب منافسيك' }, en: { name: 'Competitor Monitor', description: 'Monitor your competitors' } },
  'price-tracker': { ar: { name: 'تتبع الأسعار', description: 'راقب أسعار السوق' }, en: { name: 'Price Tracker', description: 'Monitor market prices' } },
};

// Fonction pour obtenir les outils traduits selon la langue
const getTools = (lang: string): Tool[] => {
  return toolsFR.map(tool => {
    const translation = toolTranslations[tool.id];
    const catTranslation = categoryTranslations[tool.category];

    if (lang === 'ar' && translation && catTranslation) {
      return {
        ...tool,
        name: translation.ar.name,
        description: translation.ar.description,
        category: catTranslation.ar,
      };
    } else if (lang === 'en' && translation && catTranslation) {
      return {
        ...tool,
        name: translation.en.name,
        description: translation.en.description,
        category: catTranslation.en,
      };
    }
    return tool;
  });
};

// Fonction pour obtenir les catégories selon la langue
const getCategories = (lang: string): string[] => {
  const tools = getTools(lang);
  return [...new Set(tools.map((t: Tool) => t.category))];
};

export default function Tools() {
  const { t, lang } = useTranslation();
  const navigate = useNavigate();
  const { isDark } = useTheme();
  const isRTL = lang === 'ar';
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isLoggedIn] = useState(() => {
    return localStorage.getItem('isLoggedIn') === 'true';
  });

  // Obtenir les outils et catégories selon la langue
  const allTools = getTools(lang);
  const categories = getCategories(lang);

  // Filtrer les outils
  const filteredTools = allTools.filter((tool: Tool) => {
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
              placeholder={t('tools_search_placeholder') || 'Rechercher un outil...'}
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
                background: selectedCategory === 'all' ? `${accentColor}20` : 'transparent',
                color: selectedCategory === 'all' ? accentColor : textMuted,
                fontSize: '14px',
                fontWeight: 500,
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              {t('tools_all') || 'Tous'} ({allTools.length})
            </button>
            {categories.map((cat: string) => {
              const count = allTools.filter((t: Tool) => t.category === cat).length;
              const catIcon = allTools.find((t: Tool) => t.category === cat)?.categoryIcon || '';
              return (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setSelectedCategory(cat)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '20px',
                    border: `1px solid ${selectedCategory === cat ? accentColor : borderColor}`,
                    background: selectedCategory === cat ? `${accentColor}20` : 'transparent',
                    color: selectedCategory === cat ? accentColor : textMuted,
                    fontSize: '14px',
                    fontWeight: 500,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    transition: 'all 0.2s ease',
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
          {filteredTools.length} {filteredTools.length > 1 ? (t('tools_found_plural') || 'outils trouvés') : (t('tools_found') || 'outil trouvé')}
        </p>

        {/* Tools Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '20px',
          }}
        >
          {filteredTools.map((tool: Tool) => (
            <div
              key={tool.id}
              style={{
                background: cardBg,
                borderRadius: '16px',
                padding: '20px',
                border: `1px solid ${tool.featured ? accentColor : borderColor}`,
                transition: 'all 0.3s ease',
                cursor: 'pointer',
                position: 'relative',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.borderColor = accentColor;
                e.currentTarget.style.boxShadow = `0 12px 24px ${isDark ? 'rgba(34, 197, 94, 0.15)' : 'rgba(0, 98, 51, 0.15)'}`;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.borderColor = tool.featured ? accentColor : borderColor;
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              {/* Featured Badge */}
              {tool.featured && (
                <div
                  style={{
                    position: 'absolute',
                    top: '12px',
                    right: '12px',
                    background: accentGradient,
                    color: '#fff',
                    padding: '4px 10px',
                    borderRadius: '12px',
                    fontSize: '10px',
                    fontWeight: 600,
                    textTransform: 'uppercase',
                    letterSpacing: '0.5px',
                  }}
                >
                  {t('tools_popular') || 'Popular'}
                </div>
              )}

              {/* Icon & Category */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: '12px',
                }}
              >
                <div
                  style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: isDark ? `${accentColor}15` : `${accentColor}10`,
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

              {/* Action Buttons */}
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleConnect(tool.id);
                  }}
                  style={{
                    flex: 1,
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
                      <span>{t('tools_use') || 'Utiliser'}</span>
                      <span>{isRTL ? '←' : '→'}</span>
                    </>
                  ) : (
                    <>
                      <span>{t('tools_connect') || 'Connecter'}</span>
                    </>
                  )}
                </button>
              </div>
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
              {t('tools_reset_filters') || 'Réinitialiser les filtres'}
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
            {isLoggedIn ? t('tools_cta_logged') || 'Accedez a tous les outils' : t('tools_cta_guest') || 'Connectez-vous pour utiliser les outils'}
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
              ? t('tools_cta_logged_desc') || 'Profitez de 262 outils IA pour booster votre productivite'
              : t('tools_cta_guest_desc') || 'Creez un compte gratuit et accedez a tous nos outils IA'}
          </p>
          <a
            href={isLoggedIn ? '/chat' : '/login'}
            style={{
              display: 'inline-block',
              padding: 'clamp(12px, 2vw, 16px) clamp(24px, 4vw, 32px)',
              background: accentGradient,
              color: '#fff',
              fontSize: 'clamp(14px, 2.5vw, 18px)',
              fontWeight: 600,
              textDecoration: 'none',
              borderRadius: '12px',
              boxShadow: `0 4px 16px ${isDark ? 'rgba(34, 197, 94, 0.3)' : 'rgba(0, 98, 51, 0.3)'}`,
            }}
          >
            {isLoggedIn ? t('tools_open_chat') || 'Ouvrir le Chat IA' : t('tools_create_account') || 'Creer un compte gratuit'}
          </a>
        </div>
      </div>

    </div>
  );
}
