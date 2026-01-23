"""
Templates IA Factory - Templates personnalisés pour l'Algérie
"""

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class TemplateCategory(str, Enum):
    """Catégories de templates"""
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    AGENT = "agent"


class TemplateInfo(BaseModel):
    """Information sur un template"""
    id: str
    name: str
    description: str
    category: TemplateCategory
    stack: list[str]
    features: list[str]
    files: dict[str, str] = Field(default_factory=dict)


# ============ TEMPLATE: IAFACTORY-FASTAPI ============

IAFACTORY_FASTAPI_FILES = {
    "main.py": '''"""
IA Factory FastAPI Backend
Avec intégration Chargily et support multi-tenant
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configuration
CHARGILY_API_KEY = os.getenv("CHARGILY_API_KEY")
CHARGILY_SECRET = os.getenv("CHARGILY_SECRET_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="IA Factory API",
    description="API Backend avec Chargily",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ MODELS ============

class PaymentRequest(BaseModel):
    amount: int  # En DZD
    description: str
    customer_email: str | None = None


class PaymentResponse(BaseModel):
    checkout_url: str
    payment_id: str


# ============ MULTI-TENANT ============

async def get_tenant_id(
    authorization: str = Header(..., alias="Authorization")
) -> str:
    """Extrait le tenant_id du JWT. JAMAIS via header X-Tenant-ID."""
    # TODO: Implémenter extraction JWT
    # Le tenant_id doit TOUJOURS venir du JWT, jamais d'un header
    return "default-tenant"


# ============ ENDPOINTS ============

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "iafactory-api"}


@app.post("/payments", response_model=PaymentResponse)
async def create_payment(
    request: PaymentRequest,
    tenant_id: str = Depends(get_tenant_id)
):
    """Crée un paiement via Chargily"""
    if not CHARGILY_API_KEY:
        raise HTTPException(500, "Chargily not configured")

    # TODO: Implémenter appel Chargily
    # Toujours en DZD, minimum 75 DZD
    if request.amount < 75:
        raise HTTPException(400, "Minimum amount is 75 DZD")

    return PaymentResponse(
        checkout_url="https://pay.chargily.com/checkout/xxx",
        payment_id="pay_xxx"
    )


@app.post("/webhooks/chargily")
async def chargily_webhook(payload: dict):
    """Webhook Chargily pour les notifications de paiement"""
    # TODO: Vérifier signature webhook
    # TODO: Traiter le paiement
    return {"received": True}
''',

    "chargily.py": '''"""
Service Chargily - Intégration paiement Algérie
"""

import os
import hmac
import hashlib
from typing import Any

import httpx
from pydantic import BaseModel


class ChargilyConfig(BaseModel):
    api_key: str
    secret_key: str
    base_url: str = "https://pay.chargily.com/api/v2"


class ChargilyCheckout(BaseModel):
    id: str
    checkout_url: str
    amount: int
    currency: str = "DZD"
    status: str


class ChargilyService:
    """Service d'intégration Chargily"""

    def __init__(self, config: ChargilyConfig | None = None):
        self.config = config or ChargilyConfig(
            api_key=os.getenv("CHARGILY_API_KEY", ""),
            secret_key=os.getenv("CHARGILY_SECRET_KEY", "")
        )
        self.client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            }
        )

    async def create_checkout(
        self,
        amount: int,
        description: str,
        success_url: str,
        failure_url: str,
        customer_email: str | None = None,
        metadata: dict | None = None
    ) -> ChargilyCheckout:
        """
        Crée un checkout Chargily.

        Args:
            amount: Montant en DZD (minimum 75)
            description: Description du paiement
            success_url: URL de redirection succès
            failure_url: URL de redirection échec
            customer_email: Email du client
            metadata: Métadonnées additionnelles

        Returns:
            Checkout créé avec URL de paiement
        """
        if amount < 75:
            raise ValueError("Minimum amount is 75 DZD")

        response = await self.client.post("/checkouts", json={
            "amount": amount,
            "currency": "DZD",
            "description": description,
            "success_url": success_url,
            "failure_url": failure_url,
            "customer_email": customer_email,
            "metadata": metadata or {}
        })
        response.raise_for_status()

        data = response.json()
        return ChargilyCheckout(
            id=data["id"],
            checkout_url=data["checkout_url"],
            amount=amount,
            status=data["status"]
        )

    async def get_checkout(self, checkout_id: str) -> ChargilyCheckout:
        """Récupère le statut d'un checkout"""
        response = await self.client.get(f"/checkouts/{checkout_id}")
        response.raise_for_status()
        data = response.json()
        return ChargilyCheckout(**data)

    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str
    ) -> bool:
        """Vérifie la signature d'un webhook Chargily"""
        expected = hmac.new(
            self.config.secret_key.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    async def close(self):
        await self.client.aclose()
''',

    "requirements.txt": '''fastapi>=0.109.0
uvicorn>=0.27.0
httpx>=0.26.0
pydantic>=2.5.0
python-dotenv>=1.0.0
python-jose[cryptography]>=3.3.0
''',

    ".env.example": '''# Chargily Payment
CHARGILY_API_KEY=your-api-key
CHARGILY_SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Security
JWT_SECRET=your-jwt-secret
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Multi-tenant
ENABLE_MULTI_TENANT=true
'''
}

# ============ TEMPLATE: IAFACTORY-NEXTJS ============

IAFACTORY_NEXTJS_FILES = {
    "app/layout.tsx": '''import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { I18nProvider } from "@/components/i18n-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "IA Factory",
  description: "Plateforme IA pour l'Algérie",
};

export default function RootLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  return (
    <html lang={locale} dir={locale === "ar" ? "rtl" : "ltr"}>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system">
          <I18nProvider locale={locale}>
            {children}
          </I18nProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
''',

    "components/i18n-provider.tsx": '''"use client";

import { createContext, useContext, ReactNode } from "react";

type Locale = "fr" | "ar" | "en";

interface I18nContextType {
  locale: Locale;
  t: (key: string) => string;
  dir: "ltr" | "rtl";
}

const I18nContext = createContext<I18nContextType | null>(null);

// Traductions
const translations: Record<Locale, Record<string, string>> = {
  fr: {
    welcome: "Bienvenue sur IA Factory",
    login: "Se connecter",
    register: "S'inscrire",
    dashboard: "Tableau de bord",
  },
  ar: {
    welcome: "مرحبا بك في IA Factory",
    login: "تسجيل الدخول",
    register: "إنشاء حساب",
    dashboard: "لوحة التحكم",
  },
  en: {
    welcome: "Welcome to IA Factory",
    login: "Sign in",
    register: "Sign up",
    dashboard: "Dashboard",
  },
};

export function I18nProvider({
  children,
  locale,
}: {
  children: ReactNode;
  locale: string;
}) {
  const safeLocale = (["fr", "ar", "en"].includes(locale) ? locale : "fr") as Locale;
  const dir = safeLocale === "ar" ? "rtl" : "ltr";

  const t = (key: string): string => {
    return translations[safeLocale][key] || key;
  };

  return (
    <I18nContext.Provider value={{ locale: safeLocale, t, dir }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error("useI18n must be used within I18nProvider");
  }
  return context;
}
''',

    "middleware.ts": '''import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const locales = ["fr", "ar", "en"];
const defaultLocale = "fr";

function getLocale(request: NextRequest): string {
  // Check cookie
  const cookieLocale = request.cookies.get("NEXT_LOCALE")?.value;
  if (cookieLocale && locales.includes(cookieLocale)) {
    return cookieLocale;
  }

  // Check Accept-Language header
  const acceptLang = request.headers.get("Accept-Language");
  if (acceptLang) {
    const preferred = acceptLang.split(",")[0].split("-")[0];
    if (locales.includes(preferred)) {
      return preferred;
    }
  }

  return defaultLocale;
}

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  // Check if pathname has locale
  const pathnameHasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );

  if (pathnameHasLocale) return;

  // Redirect to locale
  const locale = getLocale(request);
  request.nextUrl.pathname = `/${locale}${pathname}`;
  return NextResponse.redirect(request.nextUrl);
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
''',

    "tailwind.config.ts": '''import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#10B981",
          dark: "#059669",
        },
      },
    },
  },
  plugins: [],
};
export default config;
'''
}

# ============ TEMPLATE: IAFACTORY-GOV-AGENT ============

IAFACTORY_GOV_AGENT_FILES = {
    "agent.py": '''"""
IA Factory GOV Agent
Agent d'automatisation pour les services gouvernementaux algériens
"""

import asyncio
from typing import Any
from enum import Enum

from playwright.async_api import async_playwright, Page, Browser


class GovService(str, Enum):
    """Services GOV supportés"""
    CNAS = "cnas"
    CASNOS = "casnos"
    CNRC = "cnrc"
    SONELGAZ = "sonelgaz"
    SEAAL = "seaal"


class GovAgentConfig:
    """Configuration de l'agent"""
    CNAS_URL = "https://www.cnas.dz"
    CASNOS_URL = "https://www.casnos.com.dz"
    CNRC_URL = "https://www.cnrc.dz"
    SONELGAZ_URL = "https://www.sonelgaz.dz"
    SEAAL_URL = "https://www.seaal.dz"


class GovAgent:
    """
    Agent d'automatisation pour les services GOV algériens.
    Utilise Playwright pour l'automatisation browser.
    """

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def start(self):
        """Démarre le browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()

    async def stop(self):
        """Ferme le browser"""
        if self.browser:
            await self.browser.close()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *args):
        await self.stop()

    # ============ CNAS ============

    async def cnas_check_affiliation(self, numero_assure: str) -> dict:
        """
        Vérifie l'affiliation CNAS d'un assuré.

        Args:
            numero_assure: Numéro d'assuré social

        Returns:
            Informations d'affiliation
        """
        if not self.page:
            raise RuntimeError("Agent not started")

        await self.page.goto(f"{GovAgentConfig.CNAS_URL}/services")

        # TODO: Implémenter navigation et extraction
        # Cette partie dépend de la structure du site

        return {
            "service": "cnas",
            "numero": numero_assure,
            "status": "pending",
            "message": "Implementation required"
        }

    # ============ CNRC ============

    async def cnrc_verify_commerce(self, numero_rc: str) -> dict:
        """
        Vérifie un numéro de registre du commerce.

        Args:
            numero_rc: Numéro de registre du commerce

        Returns:
            Informations du commerce
        """
        if not self.page:
            raise RuntimeError("Agent not started")

        await self.page.goto(f"{GovAgentConfig.CNRC_URL}/verification")

        # TODO: Implémenter

        return {
            "service": "cnrc",
            "numero": numero_rc,
            "status": "pending"
        }

    # ============ SONELGAZ ============

    async def sonelgaz_get_facture(
        self,
        numero_contrat: str,
        identifiant: str
    ) -> dict:
        """
        Récupère la dernière facture Sonelgaz.

        Args:
            numero_contrat: Numéro de contrat
            identifiant: Identifiant client

        Returns:
            Informations de facturation
        """
        if not self.page:
            raise RuntimeError("Agent not started")

        await self.page.goto(f"{GovAgentConfig.SONELGAZ_URL}/espace-client")

        # TODO: Implémenter

        return {
            "service": "sonelgaz",
            "contrat": numero_contrat,
            "status": "pending"
        }


async def main():
    """Exemple d'utilisation"""
    async with GovAgent(headless=True) as agent:
        result = await agent.cnas_check_affiliation("12345678")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
''',

    "requirements.txt": '''playwright>=1.40.0
httpx>=0.26.0
pydantic>=2.5.0
''',

    "README.md": '''# IA Factory GOV Agent

Agent d'automatisation pour les services gouvernementaux algériens.

## Services supportés

- **CNAS** - Caisse Nationale d'Assurances Sociales
- **CASNOS** - Caisse Nationale de Sécurité Sociale des Non-Salariés
- **CNRC** - Centre National du Registre du Commerce
- **Sonelgaz** - Électricité et Gaz
- **SEAAL** - Eau et Assainissement

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

```python
from agent import GovAgent

async with GovAgent() as agent:
    result = await agent.cnas_check_affiliation("12345678")
    print(result)
```
'''
}

# ============ TEMPLATE REGISTRY ============

IAFACTORY_TEMPLATES: dict[str, TemplateInfo] = {
    "iafactory-fastapi": TemplateInfo(
        id="iafactory-fastapi",
        name="IA Factory FastAPI",
        description="Backend FastAPI avec intégration Chargily et multi-tenant",
        category=TemplateCategory.BACKEND,
        stack=["Python", "FastAPI", "Chargily", "PostgreSQL"],
        features=[
            "Intégration Chargily (paiement DZD)",
            "Multi-tenant via JWT",
            "Webhooks sécurisés",
            "RLS ready"
        ],
        files=IAFACTORY_FASTAPI_FILES
    ),
    "iafactory-nextjs": TemplateInfo(
        id="iafactory-nextjs",
        name="IA Factory Next.js",
        description="Frontend Next.js avec i18n (FR/AR/EN) et support RTL",
        category=TemplateCategory.FRONTEND,
        stack=["TypeScript", "Next.js", "Tailwind CSS"],
        features=[
            "Internationalisation (FR, AR, EN)",
            "Support RTL pour l'arabe",
            "Dark mode",
            "Responsive design"
        ],
        files=IAFACTORY_NEXTJS_FILES
    ),
    "iafactory-gov-agent": TemplateInfo(
        id="iafactory-gov-agent",
        name="IA Factory GOV Agent",
        description="Agent d'automatisation pour les services gouvernementaux algériens",
        category=TemplateCategory.AGENT,
        stack=["Python", "Playwright"],
        features=[
            "CNAS integration",
            "CNRC verification",
            "Sonelgaz facturation",
            "Browser automation"
        ],
        files=IAFACTORY_GOV_AGENT_FILES
    ),
}


def get_template(template_id: str) -> TemplateInfo | None:
    """Récupère un template par ID"""
    return IAFACTORY_TEMPLATES.get(template_id)


def list_templates() -> list[TemplateInfo]:
    """Liste tous les templates disponibles"""
    return list(IAFACTORY_TEMPLATES.values())


def get_template_files(template_id: str) -> dict[str, str]:
    """Récupère les fichiers d'un template"""
    template = get_template(template_id)
    return template.files if template else {}
