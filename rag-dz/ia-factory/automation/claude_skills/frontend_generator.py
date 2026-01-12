"""
IA Factory - Claude Skill: Frontend Generator
Génération de composants UI et pages web
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import os

router = APIRouter(prefix="/skills/frontend", tags=["Claude Skills - Frontend"])


class FrameworkType(str, Enum):
    REACT = "react"
    VUE = "vue"
    SVELTE = "svelte"
    HTML = "html"              # Vanilla HTML/CSS/JS
    TAILWIND = "tailwind"      # HTML + Tailwind
    ASTRO = "astro"


class ComponentType(str, Enum):
    LANDING_PAGE = "landing_page"
    DASHBOARD = "dashboard"
    FORM = "form"
    CARD = "card"
    NAVBAR = "navbar"
    FOOTER = "footer"
    HERO = "hero"
    PRICING = "pricing"
    TESTIMONIAL = "testimonial"
    FAQ = "faq"
    CTA = "cta"
    FEATURE_GRID = "feature_grid"
    STATS = "stats"
    TEAM = "team"
    CONTACT = "contact"


class StyleTheme(str, Enum):
    MODERN = "modern"
    MINIMAL = "minimal"
    CORPORATE = "corporate"
    STARTUP = "startup"
    DARK = "dark"
    LIGHT = "light"
    ALGERIAN = "algerian"      # Vert/Blanc/Rouge
    SWISS = "swiss"            # Rouge/Blanc épuré


class ComponentRequest(BaseModel):
    """Requête de génération de composant"""
    component_type: ComponentType
    framework: FrameworkType = FrameworkType.TAILWIND
    theme: StyleTheme = StyleTheme.MODERN
    title: Optional[str] = None
    content: Dict[str, Any] = Field(default_factory=dict)
    responsive: bool = True
    dark_mode: bool = False
    language: str = "fr"


class PageRequest(BaseModel):
    """Requête de génération de page complète"""
    page_type: str  # landing, dashboard, auth, etc.
    framework: FrameworkType = FrameworkType.TAILWIND
    theme: StyleTheme = StyleTheme.MODERN
    components: List[ComponentType] = Field(default_factory=list)
    company_name: str = "IA Factory"
    meta: Dict[str, str] = Field(default_factory=dict)
    responsive: bool = True
    dark_mode: bool = False


class GeneratedComponent(BaseModel):
    """Composant généré"""
    id: str
    component_type: ComponentType
    framework: FrameworkType
    code: str
    preview_url: Optional[str] = None
    created_at: datetime


class GeneratedPage(BaseModel):
    """Page générée"""
    id: str
    page_type: str
    framework: FrameworkType
    html: str
    css: str
    js: Optional[str] = None
    filepath: str
    preview_url: str
    created_at: datetime


class FrontendGenerator:
    """
    Générateur de composants frontend
    Produit du code HTML/CSS/JS ou React/Vue prêt à l'emploi
    """
    
    # Palettes de couleurs
    THEMES = {
        StyleTheme.MODERN: {
            "primary": "#1F4E79",
            "secondary": "#2E75B6",
            "accent": "#00B0F0",
            "background": "#FFFFFF",
            "surface": "#F8FAFC",
            "text": "#1E293B",
            "text_muted": "#64748B"
        },
        StyleTheme.DARK: {
            "primary": "#3B82F6",
            "secondary": "#60A5FA",
            "accent": "#F59E0B",
            "background": "#0F172A",
            "surface": "#1E293B",
            "text": "#F1F5F9",
            "text_muted": "#94A3B8"
        },
        StyleTheme.STARTUP: {
            "primary": "#8B5CF6",
            "secondary": "#A78BFA",
            "accent": "#F472B6",
            "background": "#FFFFFF",
            "surface": "#FAF5FF",
            "text": "#1E1B4B",
            "text_muted": "#6B7280"
        },
        StyleTheme.ALGERIAN: {
            "primary": "#006233",
            "secondary": "#D52B1E",
            "accent": "#FFFFFF",
            "background": "#FFFFFF",
            "surface": "#F0FDF4",
            "text": "#166534",
            "text_muted": "#4B5563"
        },
        StyleTheme.SWISS: {
            "primary": "#DC2626",
            "secondary": "#EF4444",
            "accent": "#FFFFFF",
            "background": "#FFFFFF",
            "surface": "#FEF2F2",
            "text": "#1F2937",
            "text_muted": "#6B7280"
        }
    }
    
    # Templates de composants Tailwind
    TAILWIND_COMPONENTS = {
        ComponentType.HERO: '''
<section class="bg-gradient-to-r from-{primary} to-{secondary} text-white py-20">
    <div class="container mx-auto px-6">
        <div class="flex flex-col lg:flex-row items-center">
            <div class="lg:w-1/2 mb-10 lg:mb-0">
                <h1 class="text-4xl lg:text-6xl font-bold mb-6 leading-tight">
                    {title}
                </h1>
                <p class="text-xl mb-8 text-white/90">
                    {subtitle}
                </p>
                <div class="flex flex-col sm:flex-row gap-4">
                    <a href="{cta_link}" class="bg-white text-{primary} px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition text-center">
                        {cta_text}
                    </a>
                    <a href="#demo" class="border-2 border-white px-8 py-4 rounded-lg font-semibold hover:bg-white/10 transition text-center">
                        Voir la démo
                    </a>
                </div>
            </div>
            <div class="lg:w-1/2">
                <img src="{image}" alt="Hero" class="rounded-lg shadow-2xl">
            </div>
        </div>
    </div>
</section>
''',
        
        ComponentType.FEATURE_GRID: '''
<section class="py-20 bg-{surface}">
    <div class="container mx-auto px-6">
        <div class="text-center mb-16">
            <h2 class="text-3xl lg:text-4xl font-bold text-{text} mb-4">{title}</h2>
            <p class="text-xl text-{text_muted} max-w-2xl mx-auto">{subtitle}</p>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features}
        </div>
    </div>
</section>
''',
        
        ComponentType.PRICING: '''
<section class="py-20 bg-{background}">
    <div class="container mx-auto px-6">
        <div class="text-center mb-16">
            <h2 class="text-3xl lg:text-4xl font-bold text-{text} mb-4">{title}</h2>
            <p class="text-xl text-{text_muted}">{subtitle}</p>
        </div>
        <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {pricing_cards}
        </div>
    </div>
</section>
''',
        
        ComponentType.TESTIMONIAL: '''
<section class="py-20 bg-{surface}">
    <div class="container mx-auto px-6">
        <h2 class="text-3xl lg:text-4xl font-bold text-center text-{text} mb-16">{title}</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {testimonials}
        </div>
    </div>
</section>
''',
        
        ComponentType.CTA: '''
<section class="py-20 bg-{primary}">
    <div class="container mx-auto px-6 text-center">
        <h2 class="text-3xl lg:text-4xl font-bold text-white mb-6">{title}</h2>
        <p class="text-xl text-white/90 mb-8 max-w-2xl mx-auto">{subtitle}</p>
        <a href="{cta_link}" class="inline-block bg-white text-{primary} px-10 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition">
            {cta_text}
        </a>
    </div>
</section>
''',
        
        ComponentType.NAVBAR: '''
<nav class="bg-{background} shadow-sm sticky top-0 z-50">
    <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
            <a href="/" class="text-2xl font-bold text-{primary}">{company}</a>
            <div class="hidden md:flex items-center space-x-8">
                {nav_links}
            </div>
            <div class="hidden md:flex items-center space-x-4">
                <a href="/login" class="text-{text} hover:text-{primary} transition">Connexion</a>
                <a href="/signup" class="bg-{primary} text-white px-6 py-2 rounded-lg hover:bg-{secondary} transition">
                    Commencer
                </a>
            </div>
            <button class="md:hidden text-{text}">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                </svg>
            </button>
        </div>
    </div>
</nav>
''',
        
        ComponentType.FOOTER: '''
<footer class="bg-{text} text-white py-16">
    <div class="container mx-auto px-6">
        <div class="grid md:grid-cols-4 gap-8 mb-12">
            <div>
                <h3 class="text-xl font-bold mb-4">{company}</h3>
                <p class="text-gray-400">{description}</p>
            </div>
            <div>
                <h4 class="font-semibold mb-4">Produits</h4>
                <ul class="space-y-2 text-gray-400">
                    {product_links}
                </ul>
            </div>
            <div>
                <h4 class="font-semibold mb-4">Entreprise</h4>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="/about" class="hover:text-white transition">À propos</a></li>
                    <li><a href="/contact" class="hover:text-white transition">Contact</a></li>
                    <li><a href="/careers" class="hover:text-white transition">Carrières</a></li>
                </ul>
            </div>
            <div>
                <h4 class="font-semibold mb-4">Contact</h4>
                <p class="text-gray-400">
                    {email}<br>
                    {phone}<br>
                    {address}
                </p>
            </div>
        </div>
        <div class="border-t border-gray-700 pt-8 text-center text-gray-400">
            <p>© {year} {company}. Tous droits réservés.</p>
        </div>
    </div>
</footer>
''',
        
        ComponentType.FAQ: '''
<section class="py-20 bg-{background}">
    <div class="container mx-auto px-6 max-w-4xl">
        <h2 class="text-3xl lg:text-4xl font-bold text-center text-{text} mb-16">{title}</h2>
        <div class="space-y-4">
            {faq_items}
        </div>
    </div>
</section>
''',
        
        ComponentType.STATS: '''
<section class="py-16 bg-{primary}">
    <div class="container mx-auto px-6">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center text-white">
            {stat_items}
        </div>
    </div>
</section>
'''
    }
    
    # Template de page landing complète
    LANDING_PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} | {company}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '{primary}',
                        secondary: '{secondary}',
                        accent: '{accent}'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        .gradient-text {{
            background: linear-gradient(135deg, {primary}, {accent});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
    </style>
</head>
<body class="bg-{background} text-{text}">
    {components}
    
    <script>
        // Mobile menu toggle
        document.querySelector('nav button')?.addEventListener('click', function() {{
            const menu = document.querySelector('nav .hidden.md\\:flex');
            menu?.classList.toggle('hidden');
        }});
        
        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function(e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href'))?.scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>
'''
    
    def __init__(self):
        self.output_dir = "outputs/frontend"
        os.makedirs(self.output_dir, exist_ok=True)
        self.generated_components: Dict[str, GeneratedComponent] = {}
        self.generated_pages: Dict[str, GeneratedPage] = {}
    
    async def generate_component(self, request: ComponentRequest) -> GeneratedComponent:
        """Génère un composant UI"""
        
        theme = self.THEMES.get(request.theme, self.THEMES[StyleTheme.MODERN])
        template = self.TAILWIND_COMPONENTS.get(request.component_type, "")
        
        # Remplacer les variables de couleur
        code = template.format(
            primary=theme["primary"].replace("#", ""),
            secondary=theme["secondary"].replace("#", ""),
            accent=theme["accent"].replace("#", ""),
            background=theme["background"].replace("#", ""),
            surface=theme["surface"].replace("#", ""),
            text=theme["text"].replace("#", ""),
            text_muted=theme["text_muted"].replace("#", ""),
            title=request.content.get("title", "Titre"),
            subtitle=request.content.get("subtitle", "Sous-titre"),
            cta_text=request.content.get("cta_text", "Commencer"),
            cta_link=request.content.get("cta_link", "#"),
            image=request.content.get("image", "https://placehold.co/600x400"),
            company=request.content.get("company", "IA Factory"),
            description=request.content.get("description", ""),
            email=request.content.get("email", "contact@iafactory.ch"),
            phone=request.content.get("phone", ""),
            address=request.content.get("address", ""),
            year=datetime.now().year,
            features=self._generate_features(request.content.get("features", [])),
            pricing_cards=self._generate_pricing_cards(request.content.get("pricing", [])),
            testimonials=self._generate_testimonials(request.content.get("testimonials", [])),
            nav_links=self._generate_nav_links(request.content.get("nav_links", [])),
            product_links=self._generate_product_links(request.content.get("products", [])),
            faq_items=self._generate_faq_items(request.content.get("faqs", [])),
            stat_items=self._generate_stat_items(request.content.get("stats", []))
        )
        
        component_id = f"comp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{request.component_type.value}"
        
        generated = GeneratedComponent(
            id=component_id,
            component_type=request.component_type,
            framework=request.framework,
            code=code,
            created_at=datetime.now()
        )
        
        self.generated_components[component_id] = generated
        
        return generated
    
    async def generate_page(self, request: PageRequest) -> GeneratedPage:
        """Génère une page complète"""
        
        theme = self.THEMES.get(request.theme, self.THEMES[StyleTheme.MODERN])
        
        # Générer chaque composant
        components_html = []
        
        for comp_type in request.components:
            comp_request = ComponentRequest(
                component_type=comp_type,
                framework=request.framework,
                theme=request.theme,
                content=request.meta
            )
            comp = await self.generate_component(comp_request)
            components_html.append(comp.code)
        
        # Assembler la page
        html = self.LANDING_PAGE_TEMPLATE.format(
            language="fr",
            title=request.meta.get("title", "Accueil"),
            description=request.meta.get("description", ""),
            company=request.company_name,
            primary=theme["primary"],
            secondary=theme["secondary"],
            accent=theme["accent"],
            background="white" if theme["background"] == "#FFFFFF" else theme["background"].replace("#", ""),
            text=theme["text"].replace("#", ""),
            components="\n".join(components_html)
        )
        
        # Sauvegarder
        page_id = f"page_{datetime.now().strftime('%Y%m%d%H%M%S')}_{request.page_type}"
        filename = f"{page_id}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        generated = GeneratedPage(
            id=page_id,
            page_type=request.page_type,
            framework=request.framework,
            html=html,
            css="",  # Inline avec Tailwind
            filepath=filepath,
            preview_url=f"/skills/frontend/preview/{page_id}",
            created_at=datetime.now()
        )
        
        self.generated_pages[page_id] = generated
        
        return generated
    
    def _generate_features(self, features: List[Dict]) -> str:
        """Génère le HTML des features"""
        if not features:
            features = [
                {"icon": "🚀", "title": "Rapide", "description": "Performance optimisée"},
                {"icon": "🔒", "title": "Sécurisé", "description": "Données protégées"},
                {"icon": "🎯", "title": "Précis", "description": "Résultats fiables"}
            ]
        
        html = ""
        for feature in features:
            html += f'''
            <div class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition">
                <div class="text-4xl mb-4">{feature.get("icon", "✨")}</div>
                <h3 class="text-xl font-bold mb-2">{feature.get("title", "Feature")}</h3>
                <p class="text-gray-600">{feature.get("description", "")}</p>
            </div>
            '''
        return html
    
    def _generate_pricing_cards(self, pricing: List[Dict]) -> str:
        """Génère les cartes de pricing"""
        if not pricing:
            pricing = [
                {"name": "Starter", "price": "500", "features": ["5 utilisateurs", "10GB stockage", "Support email"]},
                {"name": "Pro", "price": "1200", "features": ["25 utilisateurs", "100GB stockage", "Support prioritaire", "API access"], "popular": True},
                {"name": "Enterprise", "price": "3000", "features": ["Illimité", "1TB stockage", "Support dédié", "On-premise option"]}
            ]
        
        html = ""
        for plan in pricing:
            popular = plan.get("popular", False)
            border = "border-2 border-primary" if popular else "border border-gray-200"
            badge = '<span class="bg-primary text-white text-sm px-3 py-1 rounded-full">Populaire</span>' if popular else ""
            
            features_html = "".join(f'<li class="flex items-center gap-2"><span class="text-green-500">✓</span>{f}</li>' for f in plan.get("features", []))
            
            html += f'''
            <div class="bg-white p-8 rounded-xl {border} relative">
                <div class="absolute -top-3 left-1/2 transform -translate-x-1/2">{badge}</div>
                <h3 class="text-xl font-bold mb-2">{plan.get("name", "Plan")}</h3>
                <div class="text-4xl font-bold mb-6">{plan.get("price", "0")} <span class="text-lg text-gray-500">CHF/mois</span></div>
                <ul class="space-y-3 mb-8">{features_html}</ul>
                <button class="w-full {'bg-primary text-white' if popular else 'border border-primary text-primary'} py-3 rounded-lg font-semibold hover:opacity-90 transition">
                    Choisir
                </button>
            </div>
            '''
        return html
    
    def _generate_testimonials(self, testimonials: List[Dict]) -> str:
        """Génère les témoignages"""
        if not testimonials:
            testimonials = [
                {"quote": "IA Factory a transformé notre façon de travailler.", "author": "Ahmed B.", "role": "CEO, TechDZ"}
            ]
        
        html = ""
        for t in testimonials:
            html += f'''
            <div class="bg-white p-8 rounded-xl shadow-lg">
                <p class="text-gray-600 italic mb-6">"{t.get("quote", "")}"</p>
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold">
                        {t.get("author", "A")[0]}
                    </div>
                    <div>
                        <div class="font-bold">{t.get("author", "Client")}</div>
                        <div class="text-gray-500 text-sm">{t.get("role", "")}</div>
                    </div>
                </div>
            </div>
            '''
        return html
    
    def _generate_nav_links(self, links: List[Dict]) -> str:
        """Génère les liens de navigation"""
        if not links:
            links = [
                {"label": "Produits", "href": "#produits"},
                {"label": "Tarifs", "href": "#tarifs"},
                {"label": "À propos", "href": "#about"},
                {"label": "Contact", "href": "#contact"}
            ]
        
        return "".join(f'<a href="{l.get("href", "#")}" class="text-gray-600 hover:text-primary transition">{l.get("label", "")}</a>' for l in links)
    
    def _generate_product_links(self, products: List[str]) -> str:
        """Génère les liens produits"""
        if not products:
            products = ["RAG Solutions", "Chatbots IA", "Voice Assistants"]
        
        return "".join(f'<li><a href="#" class="hover:text-white transition">{p}</a></li>' for p in products)
    
    def _generate_faq_items(self, faqs: List[Dict]) -> str:
        """Génère les items FAQ"""
        if not faqs:
            faqs = [
                {"question": "Comment ça marche?", "answer": "Notre solution s'intègre facilement à vos systèmes existants."},
                {"question": "Quel est le délai de mise en place?", "answer": "En moyenne 2 à 4 semaines selon la complexité."}
            ]
        
        html = ""
        for i, faq in enumerate(faqs):
            html += f'''
            <details class="bg-white rounded-lg shadow p-6 cursor-pointer group">
                <summary class="font-bold text-lg flex justify-between items-center">
                    {faq.get("question", "")}
                    <span class="transform group-open:rotate-180 transition">▼</span>
                </summary>
                <p class="mt-4 text-gray-600">{faq.get("answer", "")}</p>
            </details>
            '''
        return html
    
    def _generate_stat_items(self, stats: List[Dict]) -> str:
        """Génère les statistiques"""
        if not stats:
            stats = [
                {"value": "100+", "label": "Clients"},
                {"value": "50M+", "label": "Requêtes/mois"},
                {"value": "99.9%", "label": "Uptime"},
                {"value": "24/7", "label": "Support"}
            ]
        
        return "".join(f'''
            <div>
                <div class="text-4xl font-bold">{s.get("value", "0")}</div>
                <div class="text-white/80">{s.get("label", "")}</div>
            </div>
        ''' for s in stats)


# Instance globale
frontend_generator = FrontendGenerator()


# Routes API

@router.post("/component", response_model=Dict[str, Any])
async def generate_component(request: ComponentRequest):
    """
    Génère un composant UI
    
    Types: hero, feature_grid, pricing, testimonial, cta, navbar, footer, faq, stats
    """
    comp = await frontend_generator.generate_component(request)
    return {
        "status": "success",
        "component_id": comp.id,
        "component_type": comp.component_type.value,
        "code": comp.code
    }


@router.post("/page", response_model=Dict[str, Any])
async def generate_page(request: PageRequest):
    """
    Génère une page complète avec plusieurs composants
    """
    page = await frontend_generator.generate_page(request)
    return {
        "status": "success",
        "page_id": page.id,
        "preview_url": page.preview_url,
        "html": page.html[:500] + "..." if len(page.html) > 500 else page.html
    }


@router.post("/landing-page")
async def generate_landing_page(
    company_name: str = "IA Factory",
    title: str = "L'IA qui comprend votre contexte",
    subtitle: str = "Solutions d'intelligence artificielle sur mesure pour votre entreprise",
    theme: StyleTheme = StyleTheme.MODERN
):
    """
    Génère rapidement une landing page complète
    """
    request = PageRequest(
        page_type="landing",
        theme=theme,
        company_name=company_name,
        components=[
            ComponentType.NAVBAR,
            ComponentType.HERO,
            ComponentType.FEATURE_GRID,
            ComponentType.STATS,
            ComponentType.PRICING,
            ComponentType.TESTIMONIAL,
            ComponentType.FAQ,
            ComponentType.CTA,
            ComponentType.FOOTER
        ],
        meta={
            "title": title,
            "subtitle": subtitle,
            "company": company_name
        }
    )
    
    return await generate_page(request)


@router.get("/preview/{page_id}")
async def preview_page(page_id: str):
    """Affiche la prévisualisation d'une page"""
    from fastapi.responses import HTMLResponse
    
    page = frontend_generator.generated_pages.get(page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    return HTMLResponse(content=page.html)


@router.get("/components")
async def list_components():
    """Liste tous les composants générés"""
    return list(frontend_generator.generated_components.values())


@router.get("/pages")
async def list_pages():
    """Liste toutes les pages générées"""
    return [
        {
            "id": p.id,
            "page_type": p.page_type,
            "preview_url": p.preview_url,
            "created_at": p.created_at.isoformat()
        }
        for p in frontend_generator.generated_pages.values()
    ]


@router.get("/themes")
async def list_themes():
    """Liste tous les thèmes disponibles"""
    return frontend_generator.THEMES


@router.get("/component-types")
async def list_component_types():
    """Liste tous les types de composants disponibles"""
    return [ct.value for ct in ComponentType]
