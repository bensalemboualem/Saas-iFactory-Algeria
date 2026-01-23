from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

from app.schemas import TemplateResponse

router = APIRouter()


class TemplateCategory(str, Enum):
    ECOMMERCE = "e-commerce"
    SOCIAL_MEDIA = "social-media"
    YOUTUBE = "youtube"
    SPORT = "sport"
    IMMOBILIER = "immobilier"
    FOOD = "food"
    EDUCATION = "education"
    CORPORATE = "corporate"
    EVENT = "event"
    FESTIVE = "festive"
    NEWS = "news"
    TRAVEL = "travel"


class TemplateLocale(str, Enum):
    FR = "fr"
    AR = "ar"
    EN = "en"
    DARIJA = "darija"


class TemplateCreate(BaseModel):
    name: Dict[str, str]
    description: Dict[str, str]
    category: TemplateCategory
    duration: int = Field(ge=5, le=300)
    credits: int = Field(ge=1)
    parameters: Dict
    ai_hints: Optional[Dict[str, str]] = None


# Predefined templates with multilingual support
TEMPLATES = [
    {
        "id": "1",
        "name": {
            "fr": "Pub Produit E-commerce",
            "ar": "إعلان منتج إلكتروني",
            "en": "E-commerce Product Ad",
            "darija": "إشهار ديال المنتوج"
        },
        "description": {
            "fr": "Présentez vos produits avec des animations modernes et dynamiques",
            "ar": "اعرض منتجاتك مع رسوم متحركة حديثة وديناميكية",
            "en": "Showcase your products with modern dynamic animations",
            "darija": "عرض المنتوجات ديالك بطريقة عصرية و ديناميكية"
        },
        "category": "e-commerce",
        "thumbnail_url": "/templates/ecommerce.jpg",
        "duration": 15,
        "credits": 15,
        "is_premium": False,
        "popularity": 95,
        "parameters": {
            "product_image": {"type": "image", "required": True, "label": {"fr": "Image produit", "ar": "صورة المنتج", "darija": "تصويرة ديال المنتوج"}},
            "product_name": {"type": "text", "required": True, "label": {"fr": "Nom du produit", "ar": "اسم المنتج", "darija": "سمية ديال المنتوج"}},
            "price": {"type": "text", "required": False, "label": {"fr": "Prix", "ar": "السعر", "darija": "التمن"}},
            "call_to_action": {"type": "text", "default": "Achetez maintenant!", "label": {"fr": "Appel à l'action", "ar": "دعوة للإجراء", "darija": "شري دابا!"}}
        },
        "ai_hints": {
            "style": "modern, product showcase, clean background",
            "transitions": "smooth zoom, reveal",
            "mood": "professional, energetic"
        }
    },
    {
        "id": "2",
        "name": {
            "fr": "Story Instagram Promo",
            "ar": "قصة انستغرام ترويجية",
            "en": "Instagram Story Promo",
            "darija": "ستوري إنستا ديال البروموسيون"
        },
        "description": {
            "fr": "Format vertical optimisé pour les stories avec call-to-action",
            "ar": "تنسيق عمودي محسن للقصص مع دعوة للإجراء",
            "en": "Vertical format optimized for stories with call-to-action",
            "darija": "فورما عمودية مخصصة للستوري مع CTA"
        },
        "category": "social-media",
        "thumbnail_url": "/templates/story.jpg",
        "duration": 10,
        "credits": 10,
        "is_premium": False,
        "popularity": 88,
        "parameters": {
            "background_image": {"type": "image", "required": True},
            "title": {"type": "text", "required": True},
            "subtitle": {"type": "text", "required": False}
        },
        "ai_hints": {
            "aspect_ratio": "9:16",
            "style": "trendy, eye-catching, mobile-first",
            "transitions": "swipe, bounce"
        }
    },
    {
        "id": "3",
        "name": {
            "fr": "Intro YouTube",
            "ar": "مقدمة يوتيوب",
            "en": "YouTube Intro",
            "darija": "أونترو يوتوب"
        },
        "description": {
            "fr": "Intro professionnelle pour chaîne YouTube avec logo animé",
            "ar": "مقدمة احترافية لقناة يوتيوب مع شعار متحرك",
            "en": "Professional YouTube channel intro with animated logo",
            "darija": "أونترو بروفيسيونال للشان ديال يوتوب"
        },
        "category": "youtube",
        "thumbnail_url": "/templates/youtube.jpg",
        "duration": 5,
        "credits": 8,
        "is_premium": False,
        "popularity": 92,
        "parameters": {
            "logo": {"type": "image", "required": True},
            "channel_name": {"type": "text", "required": True}
        },
        "ai_hints": {
            "style": "dynamic, logo reveal, 3D effect",
            "audio": "impact sound, whoosh"
        }
    },
    {
        "id": "4",
        "name": {
            "fr": "CAN 2025 - Match Preview",
            "ar": "كأس أفريقيا 2025 - معاينة المباراة",
            "en": "CAN 2025 - Match Preview",
            "darija": "كان 2025 - قبل الماتش"
        },
        "description": {
            "fr": "Template spécial CAN 2025 pour présenter les matchs à venir",
            "ar": "قالب خاص بكأس أفريقيا 2025 لتقديم المباريات القادمة",
            "en": "Special CAN 2025 template for upcoming match presentations",
            "darija": "تومبلات سبيسيال ديال الكان 2025"
        },
        "category": "sport",
        "thumbnail_url": "/templates/can2025.jpg",
        "duration": 20,
        "credits": 20,
        "is_premium": False,
        "popularity": 100,
        "parameters": {
            "team1_logo": {"type": "image", "required": True},
            "team2_logo": {"type": "image", "required": True},
            "team1_name": {"type": "text", "required": True},
            "team2_name": {"type": "text", "required": True},
            "match_date": {"type": "text", "required": True},
            "stadium": {"type": "text", "required": False}
        },
        "ai_hints": {
            "style": "sports broadcast, epic, stadium atmosphere",
            "effects": "fire, energy, team colors",
            "audio": "crowd cheer, epic music"
        }
    },
    {
        "id": "5",
        "name": {
            "fr": "Immobilier - Visite Virtuelle",
            "ar": "عقارات - جولة افتراضية",
            "en": "Real Estate - Virtual Tour",
            "darija": "لموبيلي - زيارة فيرتوال"
        },
        "description": {
            "fr": "Présentez des biens immobiliers avec survol cinématique",
            "ar": "اعرض العقارات مع تصوير سينمائي",
            "en": "Present real estate with cinematic flyover",
            "darija": "عرض الديار بطريقة سينماتيك"
        },
        "category": "immobilier",
        "thumbnail_url": "/templates/realestate.jpg",
        "duration": 30,
        "credits": 25,
        "is_premium": True,
        "popularity": 78,
        "parameters": {
            "property_images": {"type": "images", "required": True, "max": 5},
            "property_title": {"type": "text", "required": True},
            "price": {"type": "text", "required": True},
            "location": {"type": "text", "required": True},
            "features": {"type": "text", "required": False}
        },
        "ai_hints": {
            "style": "luxury, elegant, cinematic",
            "camera": "slow pan, drone shot, reveal",
            "music": "ambient, sophisticated"
        }
    },
    {
        "id": "6",
        "name": {
            "fr": "Restaurant - Menu du Jour",
            "ar": "مطعم - قائمة اليوم",
            "en": "Restaurant - Daily Menu",
            "darija": "ريسطو - مونو ديال نهار"
        },
        "description": {
            "fr": "Mettez en valeur vos plats avec des plans appétissants",
            "ar": "أبرز أطباقك بلقطات شهية",
            "en": "Highlight your dishes with appetizing shots",
            "darija": "عرض الماكلة ديالك بطريقة شهيوة"
        },
        "category": "food",
        "thumbnail_url": "/templates/food.jpg",
        "duration": 15,
        "credits": 12,
        "is_premium": False,
        "popularity": 85,
        "parameters": {
            "dish_images": {"type": "images", "required": True, "max": 3},
            "restaurant_name": {"type": "text", "required": True},
            "menu_items": {"type": "text", "required": True},
            "price": {"type": "text", "required": False}
        },
        "ai_hints": {
            "style": "food photography, warm colors, close-up",
            "effects": "steam, bokeh, appetizing"
        }
    },
    {
        "id": "7",
        "name": {
            "fr": "Ramadan Kareem",
            "ar": "رمضان كريم",
            "en": "Ramadan Kareem",
            "darija": "رمضان مبارك"
        },
        "description": {
            "fr": "Voeux de Ramadan avec motifs islamiques élégants",
            "ar": "تهاني رمضان مع زخارف إسلامية أنيقة",
            "en": "Ramadan greetings with elegant Islamic patterns",
            "darija": "تهنئة ديال رمضان بالزخارف الإسلامية"
        },
        "category": "festive",
        "thumbnail_url": "/templates/ramadan.jpg",
        "duration": 15,
        "credits": 10,
        "is_premium": False,
        "popularity": 90,
        "parameters": {
            "logo": {"type": "image", "required": False},
            "brand_name": {"type": "text", "required": True},
            "message": {"type": "text", "default": "رمضان مبارك سعيد"}
        },
        "ai_hints": {
            "style": "islamic art, golden, elegant, lanterns",
            "colors": "gold, purple, deep blue",
            "effects": "glow, particles, crescent moon"
        }
    },
    {
        "id": "8",
        "name": {
            "fr": "Fête de l'Aïd",
            "ar": "عيد مبارك",
            "en": "Eid Mubarak",
            "darija": "العيد الكبير"
        },
        "description": {
            "fr": "Célébrez l'Aïd avec une vidéo festive",
            "ar": "احتفل بالعيد مع فيديو احتفالي",
            "en": "Celebrate Eid with a festive video",
            "darija": "احتافل بالعيد مع فيديو زوين"
        },
        "category": "festive",
        "thumbnail_url": "/templates/eid.jpg",
        "duration": 15,
        "credits": 10,
        "is_premium": False,
        "popularity": 88,
        "parameters": {
            "brand_name": {"type": "text", "required": True},
            "message": {"type": "text", "default": "عيد مبارك سعيد"}
        },
        "ai_hints": {
            "style": "festive, joyful, islamic art",
            "effects": "confetti, sparkle, celebration"
        }
    },
    {
        "id": "9",
        "name": {
            "fr": "Formation en ligne",
            "ar": "تعليم إلكتروني",
            "en": "Online Course Promo",
            "darija": "كور أونلاين"
        },
        "description": {
            "fr": "Promouvez vos formations et cours en ligne",
            "ar": "روّج لدوراتك وتدريباتك عبر الإنترنت",
            "en": "Promote your online courses and training",
            "darija": "إشهار للكورسات ديالك أونلاين"
        },
        "category": "education",
        "thumbnail_url": "/templates/education.jpg",
        "duration": 20,
        "credits": 15,
        "is_premium": False,
        "popularity": 72,
        "parameters": {
            "course_title": {"type": "text", "required": True},
            "instructor_name": {"type": "text", "required": True},
            "course_image": {"type": "image", "required": True},
            "price": {"type": "text", "required": False}
        },
        "ai_hints": {
            "style": "professional, educational, modern",
            "effects": "text animations, knowledge icons"
        }
    },
    {
        "id": "10",
        "name": {
            "fr": "Annonce de Mariage",
            "ar": "دعوة زفاف",
            "en": "Wedding Announcement",
            "darija": "عراسة - الدعوة"
        },
        "description": {
            "fr": "Annonce élégante pour votre mariage",
            "ar": "إعلان أنيق لحفل زفافك",
            "en": "Elegant announcement for your wedding",
            "darija": "دعوة زوينة للعرس ديالك"
        },
        "category": "event",
        "thumbnail_url": "/templates/wedding.jpg",
        "duration": 20,
        "credits": 18,
        "is_premium": True,
        "popularity": 75,
        "parameters": {
            "bride_name": {"type": "text", "required": True},
            "groom_name": {"type": "text", "required": True},
            "date": {"type": "text", "required": True},
            "venue": {"type": "text", "required": True},
            "photo": {"type": "image", "required": False}
        },
        "ai_hints": {
            "style": "romantic, elegant, flowers",
            "colors": "gold, white, blush pink",
            "effects": "particles, soft glow"
        }
    },
    {
        "id": "11",
        "name": {
            "fr": "Breaking News",
            "ar": "خبر عاجل",
            "en": "Breaking News",
            "darija": "خبر عاجل"
        },
        "description": {
            "fr": "Style actualités pour annonces importantes",
            "ar": "أسلوب إخباري للإعلانات المهمة",
            "en": "News style for important announcements",
            "darija": "ستايل ديال الأخبار للإعلانات المهمة"
        },
        "category": "news",
        "thumbnail_url": "/templates/news.jpg",
        "duration": 15,
        "credits": 12,
        "is_premium": False,
        "popularity": 70,
        "parameters": {
            "headline": {"type": "text", "required": True},
            "subheadline": {"type": "text", "required": False},
            "logo": {"type": "image", "required": False}
        },
        "ai_hints": {
            "style": "news broadcast, urgent, professional",
            "effects": "breaking news banner, ticker"
        }
    },
    {
        "id": "12",
        "name": {
            "fr": "Voyage & Tourisme",
            "ar": "سياحة وسفر",
            "en": "Travel & Tourism",
            "darija": "السياحة و السفر"
        },
        "description": {
            "fr": "Promouvez des destinations touristiques",
            "ar": "روّج للوجهات السياحية",
            "en": "Promote tourist destinations",
            "darija": "إشهار للبلايص ديال السياحة"
        },
        "category": "travel",
        "thumbnail_url": "/templates/travel.jpg",
        "duration": 25,
        "credits": 20,
        "is_premium": True,
        "popularity": 82,
        "parameters": {
            "destination_images": {"type": "images", "required": True, "max": 5},
            "destination_name": {"type": "text", "required": True},
            "price": {"type": "text", "required": False},
            "highlights": {"type": "text", "required": False}
        },
        "ai_hints": {
            "style": "wanderlust, cinematic, adventure",
            "camera": "drone shots, panning, timelapse",
            "music": "uplifting, inspiring"
        }
    },
    {
        "id": "13",
        "name": {
            "fr": "Pub TikTok Virale",
            "ar": "إعلان تيك توك فيروسي",
            "en": "Viral TikTok Ad",
            "darija": "إشهار تيك توك فيرال"
        },
        "description": {
            "fr": "Format court et accrocheur pour TikTok",
            "ar": "تنسيق قصير وجذاب لتيك توك",
            "en": "Short catchy format for TikTok",
            "darija": "فورما قصيرة وشادة للتيك توك"
        },
        "category": "social-media",
        "thumbnail_url": "/templates/tiktok.jpg",
        "duration": 15,
        "credits": 12,
        "is_premium": False,
        "popularity": 95,
        "parameters": {
            "product_video": {"type": "video", "required": False},
            "product_image": {"type": "image", "required": True},
            "hook_text": {"type": "text", "required": True, "label": {"fr": "Accroche", "darija": "الجملة لي تشد"}},
            "cta": {"type": "text", "default": "Lien في البيو"}
        },
        "ai_hints": {
            "style": "trendy, fast-paced, gen-z",
            "aspect_ratio": "9:16",
            "transitions": "quick cuts, zoom, shake",
            "audio": "trending sound, voiceover"
        }
    },
    {
        "id": "14",
        "name": {
            "fr": "Témoignage Client",
            "ar": "شهادة عميل",
            "en": "Customer Testimonial",
            "darija": "شهادة ديال كليان"
        },
        "description": {
            "fr": "Mettez en avant les avis de vos clients",
            "ar": "أبرز آراء عملائك",
            "en": "Highlight your customer reviews",
            "darija": "عرض الآراء ديال الكليانات ديالك"
        },
        "category": "corporate",
        "thumbnail_url": "/templates/testimonial.jpg",
        "duration": 20,
        "credits": 15,
        "is_premium": False,
        "popularity": 68,
        "parameters": {
            "customer_photo": {"type": "image", "required": False},
            "customer_name": {"type": "text", "required": True},
            "testimonial": {"type": "text", "required": True},
            "rating": {"type": "number", "required": False, "max": 5}
        },
        "ai_hints": {
            "style": "trustworthy, clean, professional",
            "effects": "quote marks, stars, subtle animation"
        }
    },
    {
        "id": "15",
        "name": {
            "fr": "Soldes & Promotions",
            "ar": "تخفيضات وعروض",
            "en": "Sales & Promotions",
            "darija": "السولد و البروموسيون"
        },
        "description": {
            "fr": "Annoncez vos soldes avec impact",
            "ar": "أعلن عن تخفيضاتك بتأثير قوي",
            "en": "Announce your sales with impact",
            "darija": "علان على السولد بطريقة قوية"
        },
        "category": "e-commerce",
        "thumbnail_url": "/templates/sale.jpg",
        "duration": 10,
        "credits": 10,
        "is_premium": False,
        "popularity": 90,
        "parameters": {
            "discount_percentage": {"type": "text", "required": True, "label": {"fr": "Pourcentage", "darija": "النسبة ديال التخفيض"}},
            "product_images": {"type": "images", "required": True, "max": 4},
            "end_date": {"type": "text", "required": False}
        },
        "ai_hints": {
            "style": "urgent, exciting, bold colors",
            "effects": "flash, countdown, price slash",
            "colors": "red, yellow, high contrast"
        }
    }
]


def get_template_for_locale(template: dict, locale: str = "fr") -> TemplateResponse:
    """Convert template dict to TemplateResponse with locale."""
    name = template["name"].get(locale, template["name"].get("fr", ""))
    description = template["description"].get(locale, template["description"].get("fr", ""))
    
    return TemplateResponse(
        id=template["id"],
        name=name,
        description=description,
        category=template["category"],
        thumbnail_url=template.get("thumbnail_url", ""),
        duration=template["duration"],
        credits=template["credits"],
        parameters=template["parameters"]
    )


@router.get("", response_model=List[TemplateResponse], tags=["Templates - List"])
async def list_templates(
    category: Optional[str] = None,
    locale: str = Query("fr", description="Locale (fr, ar, en, darija)"),
    premium_only: bool = False,
    sort_by: str = Query("popularity", description="Sort by: popularity, credits, duration")
):
    """List all available templates with optional filtering."""
    filtered = TEMPLATES.copy()
    
    # Filter by category
    if category:
        filtered = [t for t in filtered if t["category"].lower() == category.lower()]
    
    # Filter premium only
    if premium_only:
        filtered = [t for t in filtered if t.get("is_premium", False)]
    
    # Sort
    if sort_by == "popularity":
        filtered = sorted(filtered, key=lambda x: x.get("popularity", 0), reverse=True)
    elif sort_by == "credits":
        filtered = sorted(filtered, key=lambda x: x["credits"])
    elif sort_by == "duration":
        filtered = sorted(filtered, key=lambda x: x["duration"])
    
    return [get_template_for_locale(t, locale) for t in filtered]


@router.get("/categories", tags=["Templates - Categories"])
async def list_categories(locale: str = "fr"):
    """List all template categories."""
    categories_info = {
        "e-commerce": {"fr": "E-commerce", "ar": "تجارة إلكترونية", "darija": "التجارة أونلاين", "icon": "🛒"},
        "social-media": {"fr": "Réseaux Sociaux", "ar": "شبكات اجتماعية", "darija": "الريزو", "icon": "📱"},
        "youtube": {"fr": "YouTube", "ar": "يوتيوب", "darija": "يوتوب", "icon": "▶️"},
        "sport": {"fr": "Sport", "ar": "رياضة", "darija": "السبور", "icon": "⚽"},
        "immobilier": {"fr": "Immobilier", "ar": "عقارات", "darija": "لموبيلي", "icon": "🏠"},
        "food": {"fr": "Restauration", "ar": "مطاعم", "darija": "الماكلة", "icon": "🍽️"},
        "education": {"fr": "Éducation", "ar": "تعليم", "darija": "التعليم", "icon": "📚"},
        "corporate": {"fr": "Entreprise", "ar": "شركات", "darija": "الشركات", "icon": "💼"},
        "event": {"fr": "Événements", "ar": "فعاليات", "darija": "المناسبات", "icon": "🎉"},
        "festive": {"fr": "Fêtes", "ar": "أعياد", "darija": "الأعياد", "icon": "🌙"},
        "news": {"fr": "Actualités", "ar": "أخبار", "darija": "الأخبار", "icon": "📰"},
        "travel": {"fr": "Voyage", "ar": "سفر", "darija": "السياحة", "icon": "✈️"}
    }
    
    result = []
    for cat_id, info in categories_info.items():
        count = len([t for t in TEMPLATES if t["category"] == cat_id])
        result.append({
            "id": cat_id,
            "name": info.get(locale, info["fr"]),
            "icon": info["icon"],
            "count": count
        })
    
    return sorted(result, key=lambda x: x["count"], reverse=True)


@router.get("/popular", tags=["Templates - List"])
async def get_popular_templates(
    limit: int = Query(6, ge=1, le=20),
    locale: str = "fr"
):
    """Get most popular templates."""
    sorted_templates = sorted(TEMPLATES, key=lambda x: x.get("popularity", 0), reverse=True)
    return [get_template_for_locale(t, locale) for t in sorted_templates[:limit]]


@router.get("/featured", tags=["Templates - List"])
async def get_featured_templates(locale: str = "fr"):
    """Get featured templates (curated selection)."""
    featured_ids = ["4", "7", "13", "1", "5"]  # CAN 2025, Ramadan, TikTok, E-commerce, Immobilier
    featured = [t for t in TEMPLATES if t["id"] in featured_ids]
    return [get_template_for_locale(t, locale) for t in featured]


@router.get("/seasonal", tags=["Templates - List"])
async def get_seasonal_templates(locale: str = "fr"):
    """Get seasonal templates based on current date."""
    now = datetime.now()
    month = now.month
    
    seasonal_categories = []
    
    # Ramadan (approximately March-April)
    if month in [3, 4]:
        seasonal_categories.append("festive")
    
    # Summer vacation (June-August)
    if month in [6, 7, 8]:
        seasonal_categories.append("travel")
    
    # End of year sales (November-December)
    if month in [11, 12]:
        seasonal_categories.extend(["e-commerce", "festive"])
    
    # Back to school (September)
    if month == 9:
        seasonal_categories.append("education")
    
    # CAN 2025 (January-February 2025)
    if month in [1, 2] and now.year == 2025:
        seasonal_categories.append("sport")
    
    if not seasonal_categories:
        seasonal_categories = ["social-media", "e-commerce"]  # Default
    
    filtered = [t for t in TEMPLATES if t["category"] in seasonal_categories]
    return [get_template_for_locale(t, locale) for t in filtered[:6]]


@router.get("/{template_id}", response_model=TemplateResponse, tags=["Templates - Detail"])
async def get_template(template_id: str, locale: str = "fr"):
    """Get a specific template by ID."""
    for template in TEMPLATES:
        if template["id"] == template_id:
            return get_template_for_locale(template, locale)
    
    raise HTTPException(status_code=404, detail="Template not found")


@router.get("/{template_id}/full", tags=["Templates - Detail"])
async def get_template_full(template_id: str):
    """Get full template data including all locales and AI hints."""
    for template in TEMPLATES:
        if template["id"] == template_id:
            return template
    
    raise HTTPException(status_code=404, detail="Template not found")


@router.get("/{template_id}/preview", tags=["Templates - Preview"])
async def get_template_preview(template_id: str):
    """Get template preview data for rendering."""
    for template in TEMPLATES:
        if template["id"] == template_id:
            return {
                "id": template["id"],
                "thumbnail_url": template.get("thumbnail_url"),
                "duration": template["duration"],
                "ai_hints": template.get("ai_hints", {}),
                "sample_prompt": _generate_sample_prompt(template)
            }
    
    raise HTTPException(status_code=404, detail="Template not found")


def _generate_sample_prompt(template: dict) -> str:
    """Generate a sample AI prompt for the template."""
    hints = template.get("ai_hints", {})
    category = template["category"]
    
    base_prompt = f"Create a {template['duration']}-second video in {hints.get('style', 'modern professional')} style"
    
    if hints.get("aspect_ratio"):
        base_prompt += f", aspect ratio {hints['aspect_ratio']}"
    
    if hints.get("camera"):
        base_prompt += f", with {hints['camera']} camera movements"
    
    if hints.get("effects"):
        base_prompt += f", including {hints['effects']} effects"
    
    return base_prompt
