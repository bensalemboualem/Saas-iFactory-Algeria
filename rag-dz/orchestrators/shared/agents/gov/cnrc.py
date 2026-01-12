"""
CNRC Agent - Centre National du Registre de Commerce.
Automatise les interactions avec le portail CNRC.
"""

import re
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from .base import (
    GOVAgentBase,
    GOVCredentials,
    GOVSession,
    GOVDocument,
    GOVService,
    ParserBase,
)


class CNRCExtrait(BaseModel):
    """Extrait du Registre de Commerce"""
    numero_rc: str
    raison_sociale: str
    forme_juridique: str  # SARL, SPA, EURL, etc.
    capital_social: float | None = None
    siege_social: str
    wilaya: str
    activites: list[str] = Field(default_factory=list)
    date_creation: str | None = None
    date_expiration: str | None = None
    gerants: list[str] = Field(default_factory=list)
    nif: str | None = None  # Numéro d'Identification Fiscale
    nis: str | None = None  # Numéro d'Identification Statistique
    statut: str = "actif"


class CNRCModification(BaseModel):
    """Modification au registre de commerce"""
    type_modification: str
    date_modification: str
    description: str
    reference: str | None = None


class CNRCParser(ParserBase):
    """Parser pour les pages CNRC"""

    async def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        return {
            "title": self._get_title(soup),
            "content": soup.get_text()[:500]
        }

    def _get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find("h1") or soup.find("title")
        return self.clean_text(title.text) if title else ""

    async def parse_extrait(self, html: str) -> CNRCExtrait | None:
        """
        Parse un extrait du registre de commerce.

        Args:
            html: HTML de la page

        Returns:
            CNRCExtrait ou None
        """
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        data = {}

        patterns = {
            "numero_rc": r"(?:N[°o]\s*)?(?:RC|Registre\s*de\s*Commerce)\s*[:\s]+([A-Z0-9/-]+)",
            "raison_sociale": r"(?:Raison\s*sociale|Dénomination)\s*[:\s]+(.+?)(?:\n|$)",
            "forme_juridique": r"(?:Forme\s*juridique|Nature)\s*[:\s]+(SARL|SPA|EURL|SNC|EI|SA)",
            "capital_social": r"Capital\s*(?:social)?\s*[:\s]+([\d\s,\.]+)\s*(?:DA|DZD)?",
            "siege_social": r"(?:Siège\s*social|Adresse)\s*[:\s]+(.+?)(?:\n|Wilaya)",
            "wilaya": r"Wilaya\s*[:\s]+(\d{2}\s*-?\s*[A-ZÀ-Ü\s]+)",
            "date_creation": r"(?:Date\s*de\s*création|Créé\s*le)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
            "date_expiration": r"(?:Date\s*d'expiration|Expire\s*le)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
            "nif": r"NIF\s*[:\s]+(\d{15,20})",
            "nis": r"NIS\s*[:\s]+(\d{10,15})",
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = self.clean_text(match.group(1))
                if field == "capital_social":
                    data[field] = self.parse_amount(value)
                else:
                    data[field] = value

        # Parser les activités
        activites = []
        activites_section = soup.find(string=re.compile(r"activit[ée]s?", re.I))
        if activites_section:
            ul = activites_section.find_next("ul")
            if ul:
                for li in ul.find_all("li"):
                    activites.append(self.clean_text(li.text))

        # Parser les gérants
        gerants = []
        gerants_section = soup.find(string=re.compile(r"g[ée]rants?|dirigeants?", re.I))
        if gerants_section:
            ul = gerants_section.find_next("ul")
            if ul:
                for li in ul.find_all("li"):
                    gerants.append(self.clean_text(li.text))

        if not data.get("numero_rc"):
            return None

        return CNRCExtrait(
            numero_rc=data.get("numero_rc", ""),
            raison_sociale=data.get("raison_sociale", ""),
            forme_juridique=data.get("forme_juridique", ""),
            capital_social=data.get("capital_social"),
            siege_social=data.get("siege_social", ""),
            wilaya=data.get("wilaya", ""),
            activites=activites,
            date_creation=data.get("date_creation"),
            date_expiration=data.get("date_expiration"),
            gerants=gerants,
            nif=data.get("nif"),
            nis=data.get("nis"),
        )


class CNRCAgent(GOVAgentBase):
    """
    Agent pour le portail CNRC (Registre de Commerce Algérie).

    Fonctionnalités:
    - Connexion au compte
    - Récupération extrait RC
    - Historique des modifications
    - Téléchargement documents
    """

    SERVICE = GOVService.CNRC
    BASE_URL = "https://www.cnrc.dz"
    PORTAL_URL = "https://sidjilcom.cnrc.dz"

    def __init__(self, credentials: GOVCredentials | None = None, headless: bool = True):
        super().__init__(credentials, headless)
        self.parser = CNRCParser()

    async def login(self) -> GOVSession:
        """Se connecter au portail CNRC"""
        if not self.credentials:
            raise ValueError("Credentials required for login")

        await self.init_browser()
        await self.navigate(f"{self.PORTAL_URL}/login")

        await self.wait_for_selector("input[name='username'], input[name='email']")

        await self.fill("input[name='username'], input[name='email']", self.credentials.username)
        await self.fill("input[name='password']", self.credentials.password)

        if self.credentials.rc:
            rc_field = await self._page.query_selector("input[name='rc']")
            if rc_field:
                await self.fill("input[name='rc']", self.credentials.rc)

        await self.click("button[type='submit'], input[type='submit']")
        await self._page.wait_for_load_state("networkidle")

        cookies = await self._context.cookies()
        session_cookie = next((c for c in cookies if "session" in c["name"].lower()), None)

        if session_cookie:
            self.session = GOVSession(
                service=self.SERVICE,
                session_id=session_cookie["value"],
                cookies={c["name"]: c["value"] for c in cookies}
            )
            return self.session

        raise RuntimeError("Login failed")

    async def logout(self):
        """Se déconnecter"""
        if self._page:
            try:
                await self.navigate(f"{self.PORTAL_URL}/logout")
            except Exception:
                pass
        self.session = None
        await self.close()

    async def get_attestation(self) -> GOVDocument:
        """
        Récupérer l'extrait du registre de commerce.

        Returns:
            GOVDocument avec l'extrait RC
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/extrait")
        await self.wait_for_selector(".extrait, .document, main")

        html = await self.get_page_content()
        extrait = await self.parser.parse_extrait(html)

        return GOVDocument(
            service=self.SERVICE,
            doc_type="extrait_rc",
            title="Extrait du Registre de Commerce",
            html=html,
            data=extrait.model_dump() if extrait else {}
        )

    async def rechercher_entreprise(self, rc_number: str) -> CNRCExtrait | None:
        """
        Rechercher une entreprise par numéro RC.

        Args:
            rc_number: Numéro du registre de commerce

        Returns:
            CNRCExtrait ou None
        """
        await self.init_browser()
        await self.navigate(f"{self.BASE_URL}/recherche")

        await self.wait_for_selector("input[name='rc'], input[name='search']")
        await self.fill("input[name='rc'], input[name='search']", rc_number)
        await self.click("button[type='submit']")
        await self._page.wait_for_load_state("networkidle")

        html = await self.get_page_content()
        return await self.parser.parse_extrait(html)

    async def telecharger_extrait_pdf(self, output_path: str) -> bool:
        """Télécharger l'extrait en PDF"""
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/extrait/pdf")

        pdf_button = await self._page.query_selector("a[href*='pdf'], .download-pdf")
        if pdf_button:
            async with self._page.expect_download() as download_info:
                await pdf_button.click()
            download = await download_info.value
            await download.save_as(output_path)
            return True

        await self._page.pdf(path=output_path)
        return True
