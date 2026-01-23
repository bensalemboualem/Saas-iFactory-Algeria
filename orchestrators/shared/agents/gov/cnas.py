"""
CNAS Agent - Caisse Nationale des Assurances Sociales.
Automatise les interactions avec le portail CNAS.
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


class CNASAttestation(BaseModel):
    """Attestation d'affiliation CNAS"""
    numero: str
    nom: str
    prenom: str
    nss: str  # Numéro de Sécurité Sociale
    date_naissance: str | None = None
    employeur: str | None = None
    numero_employeur: str | None = None
    date_affiliation: str | None = None
    statut: str = "affilié"
    date_emission: datetime = Field(default_factory=datetime.utcnow)
    valid_until: datetime | None = None


class CNASCotisation(BaseModel):
    """Cotisation CNAS"""
    periode: str  # Format: "MM/YYYY"
    montant_salarie: float
    montant_employeur: float
    montant_total: float
    statut: str  # payé, en attente, etc.
    date_paiement: str | None = None


class CNASCarteChifa(BaseModel):
    """Informations Carte Chifa"""
    numero_carte: str
    nss: str
    nom: str
    prenom: str
    date_naissance: str | None = None
    ayants_droit: list[dict] = Field(default_factory=list)
    date_expiration: str | None = None
    statut: str = "active"


class CNASParser(ParserBase):
    """
    Parser pour les pages CNAS.
    Extrait les données des attestations, cotisations, et carte Chifa.
    """

    async def parse(self, html: str) -> dict:
        """Parse generic CNAS page"""
        soup = BeautifulSoup(html, "html.parser")
        return {
            "title": self._get_title(soup),
            "content": self._get_main_content(soup)
        }

    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title = soup.find("h1") or soup.find("title")
        return self.clean_text(title.text) if title else ""

    def _get_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content"""
        main = soup.find("main") or soup.find("div", class_="content")
        return self.clean_text(main.text) if main else ""

    async def parse_attestation(self, html: str) -> CNASAttestation | None:
        """
        Parse une attestation d'affiliation CNAS.

        Args:
            html: HTML de la page d'attestation

        Returns:
            CNASAttestation ou None
        """
        soup = BeautifulSoup(html, "html.parser")

        # Chercher les champs de l'attestation
        data = {}

        # Pattern: Label: Valeur
        patterns = {
            "numero": r"N[°o]\s*(?:attestation|affiliation)?\s*[:\s]+([A-Z0-9/-]+)",
            "nss": r"N[°o]?\s*(?:SS|Sécurité\s*Sociale)\s*[:\s]+(\d{12,15})",
            "nom": r"Nom\s*[:\s]+([A-ZÀ-Ü\s]+)",
            "prenom": r"Prénom\s*[:\s]+([A-Za-zÀ-ü\s]+)",
            "date_naissance": r"(?:Date\s*de\s*naissance|Né\(e\)\s*le)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
            "employeur": r"Employeur\s*[:\s]+(.+?)(?:\n|$)",
            "numero_employeur": r"N[°o]\s*Employeur\s*[:\s]+([A-Z0-9/-]+)",
            "date_affiliation": r"(?:Date\s*d'affiliation|Affilié\s*depuis)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
        }

        text = soup.get_text()

        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data[field] = self.clean_text(match.group(1))

        # Vérifier les champs obligatoires
        if not data.get("nss") and not data.get("numero"):
            return None

        return CNASAttestation(
            numero=data.get("numero", ""),
            nom=data.get("nom", ""),
            prenom=data.get("prenom", ""),
            nss=data.get("nss", ""),
            date_naissance=data.get("date_naissance"),
            employeur=data.get("employeur"),
            numero_employeur=data.get("numero_employeur"),
            date_affiliation=data.get("date_affiliation"),
        )

    async def parse_historique(self, html: str) -> list[CNASCotisation]:
        """
        Parse l'historique des cotisations.

        Args:
            html: HTML de la page d'historique

        Returns:
            Liste de CNASCotisation
        """
        soup = BeautifulSoup(html, "html.parser")
        cotisations = []

        # Chercher le tableau des cotisations
        table = soup.find("table", class_=re.compile(r"cotisation|historique", re.I))
        if not table:
            table = soup.find("table")

        if not table:
            return cotisations

        rows = table.find_all("tr")[1:]  # Skip header

        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) >= 4:
                try:
                    cotisation = CNASCotisation(
                        periode=self.clean_text(cols[0].text),
                        montant_salarie=self.parse_amount(cols[1].text),
                        montant_employeur=self.parse_amount(cols[2].text),
                        montant_total=self.parse_amount(cols[3].text),
                        statut=self.clean_text(cols[4].text) if len(cols) > 4 else "inconnu",
                        date_paiement=self.clean_text(cols[5].text) if len(cols) > 5 else None
                    )
                    cotisations.append(cotisation)
                except Exception:
                    continue

        return cotisations

    async def parse_carte_chifa(self, html: str) -> CNASCarteChifa | None:
        """
        Parse les informations de la carte Chifa.

        Args:
            html: HTML de la page carte Chifa

        Returns:
            CNASCarteChifa ou None
        """
        soup = BeautifulSoup(html, "html.parser")

        data = {}
        text = soup.get_text()

        patterns = {
            "numero_carte": r"N[°o]\s*(?:carte|Chifa)\s*[:\s]+([A-Z0-9]+)",
            "nss": r"N[°o]?\s*SS\s*[:\s]+(\d{12,15})",
            "nom": r"Nom\s*[:\s]+([A-ZÀ-Ü\s]+)",
            "prenom": r"Prénom\s*[:\s]+([A-Za-zÀ-ü\s]+)",
            "date_expiration": r"(?:Date\s*d'expiration|Expire\s*le)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data[field] = self.clean_text(match.group(1))

        # Parse ayants droit
        ayants_droit = []
        ad_section = soup.find(string=re.compile(r"ayants?\s*droit", re.I))
        if ad_section:
            ad_table = ad_section.find_next("table")
            if ad_table:
                for row in ad_table.find_all("tr")[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        ayants_droit.append({
                            "nom": self.clean_text(cols[0].text),
                            "lien": self.clean_text(cols[1].text) if len(cols) > 1 else "",
                            "nss": self.clean_text(cols[2].text) if len(cols) > 2 else ""
                        })

        if not data.get("numero_carte"):
            return None

        return CNASCarteChifa(
            numero_carte=data.get("numero_carte", ""),
            nss=data.get("nss", ""),
            nom=data.get("nom", ""),
            prenom=data.get("prenom", ""),
            date_expiration=data.get("date_expiration"),
            ayants_droit=ayants_droit
        )


class CNASAgent(GOVAgentBase):
    """
    Agent pour le portail CNAS (Sécurité Sociale Algérie).

    Fonctionnalités:
    - Connexion au compte
    - Récupération attestation d'affiliation
    - Historique des cotisations
    - Informations carte Chifa
    """

    SERVICE = GOVService.CNAS
    BASE_URL = "https://www.cnas.dz"
    PORTAL_URL = "https://teledeclaration.cnas.dz"

    def __init__(self, credentials: GOVCredentials | None = None, headless: bool = True):
        super().__init__(credentials, headless)
        self.parser = CNASParser()

    async def login(self) -> GOVSession:
        """
        Se connecter au portail CNAS.

        Returns:
            Session active
        """
        if not self.credentials:
            raise ValueError("Credentials required for login")

        await self.init_browser()
        await self.navigate(f"{self.PORTAL_URL}/login")

        # Attendre le formulaire
        await self.wait_for_selector("input[name='username'], input[name='login']")

        # Remplir les credentials
        await self.fill("input[name='username'], input[name='login']", self.credentials.username)
        await self.fill("input[name='password']", self.credentials.password)

        # Si NSS requis
        if self.credentials.nss:
            nss_field = await self._page.query_selector("input[name='nss']")
            if nss_field:
                await self.fill("input[name='nss']", self.credentials.nss)

        # Soumettre
        await self.click("button[type='submit'], input[type='submit']")

        # Attendre redirection
        await self._page.wait_for_load_state("networkidle")

        # Vérifier connexion réussie
        cookies = await self._context.cookies()
        session_cookie = next((c for c in cookies if "session" in c["name"].lower()), None)

        if session_cookie:
            self.session = GOVSession(
                service=self.SERVICE,
                session_id=session_cookie["value"],
                cookies={c["name"]: c["value"] for c in cookies}
            )
            return self.session

        raise RuntimeError("Login failed - no session cookie found")

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
        Récupérer l'attestation d'affiliation.

        Returns:
            GOVDocument avec l'attestation
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/attestation")
        await self.wait_for_selector(".attestation, .document, main")

        html = await self.get_page_content()
        attestation = await self.parser.parse_attestation(html)

        return GOVDocument(
            service=self.SERVICE,
            doc_type="attestation_affiliation",
            title="Attestation d'affiliation CNAS",
            html=html,
            data=attestation.model_dump() if attestation else {}
        )

    async def get_historique_cotisations(self) -> list[CNASCotisation]:
        """
        Récupérer l'historique des cotisations.

        Returns:
            Liste des cotisations
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/cotisations/historique")
        await self.wait_for_selector("table, .historique")

        html = await self.get_page_content()
        return await self.parser.parse_historique(html)

    async def get_carte_chifa(self) -> CNASCarteChifa | None:
        """
        Récupérer les informations de la carte Chifa.

        Returns:
            CNASCarteChifa
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/carte-chifa")
        await self.wait_for_selector(".carte-chifa, .card-info, main")

        html = await self.get_page_content()
        return await self.parser.parse_carte_chifa(html)

    async def telecharger_attestation_pdf(self, output_path: str) -> bool:
        """
        Télécharger l'attestation en PDF.

        Args:
            output_path: Chemin du fichier de sortie

        Returns:
            True si succès
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/attestation")

        # Chercher le bouton de téléchargement PDF
        pdf_button = await self._page.query_selector(
            "a[href*='pdf'], button[data-format='pdf'], .download-pdf"
        )

        if pdf_button:
            async with self._page.expect_download() as download_info:
                await pdf_button.click()
            download = await download_info.value
            await download.save_as(output_path)
            return True

        # Fallback: imprimer en PDF
        await self._page.pdf(path=output_path)
        return True
