"""
DGI Agent - Direction Générale des Impôts.
Automatise les interactions avec le portail Jibaya't.
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


class DGIAttestation(BaseModel):
    """Attestation fiscale DGI"""
    numero: str
    nif: str  # Numéro d'Identification Fiscale
    raison_sociale: str
    adresse: str
    wilaya: str
    activite_principale: str | None = None
    regime_fiscal: str  # réel, forfaitaire, IFU
    date_emission: str | None = None
    date_validite: str | None = None
    situation: str = "en_règle"  # en_règle, en_défaut


class DGIDeclaration(BaseModel):
    """Déclaration fiscale"""
    type_declaration: str  # G50, G50A, TAP, IRG, IBS, etc.
    periode: str
    date_depot: str | None = None
    montant_declare: float
    montant_paye: float
    statut: str  # deposee, en_attente, validee


class DGIEcheance(BaseModel):
    """Échéance fiscale"""
    type_impot: str
    libelle: str
    date_echeance: str
    montant: float
    statut: str  # a_payer, payee, en_retard


class DGIParser(ParserBase):
    """Parser pour les pages DGI/Jibaya't"""

    async def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        return {
            "title": self._get_title(soup),
            "content": soup.get_text()[:500]
        }

    def _get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find("h1") or soup.find("title")
        return self.clean_text(title.text) if title else ""

    async def parse_attestation(self, html: str) -> DGIAttestation | None:
        """
        Parse une attestation fiscale.

        Args:
            html: HTML de la page

        Returns:
            DGIAttestation ou None
        """
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        data = {}

        patterns = {
            "numero": r"(?:N[°o]\s*)?(?:Attestation)\s*[:\s]+([A-Z0-9/-]+)",
            "nif": r"NIF\s*[:\s]+(\d{15,20})",
            "raison_sociale": r"(?:Raison\s*sociale|Contribuable)\s*[:\s]+(.+?)(?:\n|$)",
            "adresse": r"Adresse\s*[:\s]+(.+?)(?:\n|Wilaya)",
            "wilaya": r"Wilaya\s*[:\s]+(\d{2}\s*-?\s*[A-ZÀ-Ü\s]+)",
            "activite_principale": r"Activité\s*(?:principale)?\s*[:\s]+(.+?)(?:\n|$)",
            "regime_fiscal": r"Régime\s*(?:fiscal)?\s*[:\s]+(réel|forfaitaire|IFU|simplifié)",
            "date_emission": r"(?:Date\s*d'émission|Émis\s*le)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
            "date_validite": r"(?:Valide\s*jusqu'au|Date\s*de\s*validité)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data[field] = self.clean_text(match.group(1))

        # Déterminer la situation
        situation = "en_règle"
        if re.search(r"défaut|impayé|retard", text, re.IGNORECASE):
            situation = "en_défaut"

        if not data.get("nif"):
            return None

        return DGIAttestation(
            numero=data.get("numero", ""),
            nif=data.get("nif", ""),
            raison_sociale=data.get("raison_sociale", ""),
            adresse=data.get("adresse", ""),
            wilaya=data.get("wilaya", ""),
            activite_principale=data.get("activite_principale"),
            regime_fiscal=data.get("regime_fiscal", "réel"),
            date_emission=data.get("date_emission"),
            date_validite=data.get("date_validite"),
            situation=situation,
        )

    async def parse_declarations(self, html: str) -> list[DGIDeclaration]:
        """
        Parse la liste des déclarations.

        Args:
            html: HTML de la page

        Returns:
            Liste de DGIDeclaration
        """
        soup = BeautifulSoup(html, "html.parser")
        declarations = []

        table = soup.find("table", class_=re.compile(r"declaration|historique", re.I))
        if not table:
            table = soup.find("table")

        if not table:
            return declarations

        rows = table.find_all("tr")[1:]

        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) >= 4:
                try:
                    declaration = DGIDeclaration(
                        type_declaration=self.clean_text(cols[0].text),
                        periode=self.clean_text(cols[1].text),
                        date_depot=self.clean_text(cols[2].text) if len(cols) > 2 else None,
                        montant_declare=self.parse_amount(cols[3].text) if len(cols) > 3 else 0,
                        montant_paye=self.parse_amount(cols[4].text) if len(cols) > 4 else 0,
                        statut=self.clean_text(cols[5].text) if len(cols) > 5 else "deposee",
                    )
                    declarations.append(declaration)
                except Exception:
                    continue

        return declarations

    async def parse_echeances(self, html: str) -> list[DGIEcheance]:
        """
        Parse le calendrier des échéances.

        Args:
            html: HTML de la page

        Returns:
            Liste de DGIEcheance
        """
        soup = BeautifulSoup(html, "html.parser")
        echeances = []

        table = soup.find("table", class_=re.compile(r"echeance|calendrier", re.I))
        if not table:
            table = soup.find("table")

        if not table:
            return echeances

        rows = table.find_all("tr")[1:]

        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) >= 3:
                try:
                    echeance = DGIEcheance(
                        type_impot=self.clean_text(cols[0].text),
                        libelle=self.clean_text(cols[1].text),
                        date_echeance=self.clean_text(cols[2].text),
                        montant=self.parse_amount(cols[3].text) if len(cols) > 3 else 0,
                        statut=self.clean_text(cols[4].text) if len(cols) > 4 else "a_payer",
                    )
                    echeances.append(echeance)
                except Exception:
                    continue

        return echeances


class DGIAgent(GOVAgentBase):
    """
    Agent pour le portail Jibaya't (Impôts Algérie).

    Fonctionnalités:
    - Connexion au compte contribuable
    - Attestation de situation fiscale
    - Historique des déclarations
    - Calendrier des échéances
    - Télédéclaration G50, TAP, etc.
    """

    SERVICE = GOVService.DGI
    BASE_URL = "https://www.mfdgi.gov.dz"
    PORTAL_URL = "https://jibayatic.mfdgi.gov.dz"

    def __init__(self, credentials: GOVCredentials | None = None, headless: bool = True):
        super().__init__(credentials, headless)
        self.parser = DGIParser()

    async def login(self) -> GOVSession:
        """Se connecter au portail Jibaya't"""
        if not self.credentials:
            raise ValueError("Credentials required for login")

        await self.init_browser()
        await self.navigate(f"{self.PORTAL_URL}/login")

        await self.wait_for_selector("input[name='nif'], input[name='username']")

        # Le portail Jibaya't utilise le NIF
        nif_field = await self._page.query_selector("input[name='nif']")
        if nif_field and self.credentials.nif:
            await self.fill("input[name='nif']", self.credentials.nif)
        else:
            await self.fill("input[name='username']", self.credentials.username)

        await self.fill("input[name='password']", self.credentials.password)

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
        Récupérer l'attestation de situation fiscale.

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
            doc_type="attestation_fiscale",
            title="Attestation de Situation Fiscale",
            html=html,
            data=attestation.model_dump() if attestation else {}
        )

    async def get_declarations(self, annee: int | None = None) -> list[DGIDeclaration]:
        """
        Récupérer l'historique des déclarations.

        Args:
            annee: Filtrer par année (optionnel)

        Returns:
            Liste de DGIDeclaration
        """
        if not self.session:
            await self.login()

        url = f"{self.PORTAL_URL}/declarations"
        if annee:
            url += f"?annee={annee}"

        await self.navigate(url)
        await self.wait_for_selector("table, .declarations")

        html = await self.get_page_content()
        return await self.parser.parse_declarations(html)

    async def get_echeances(self) -> list[DGIEcheance]:
        """
        Récupérer le calendrier des échéances fiscales.

        Returns:
            Liste de DGIEcheance
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/echeances")
        await self.wait_for_selector("table, .calendrier")

        html = await self.get_page_content()
        return await self.parser.parse_echeances(html)

    async def get_solde_compte(self) -> dict:
        """
        Récupérer le solde du compte fiscal.

        Returns:
            Dict avec le solde
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/compte")
        await self.wait_for_selector(".solde, .compte, main")

        html = await self.get_page_content()
        soup = BeautifulSoup(html, "html.parser")

        # Chercher le solde
        solde_match = re.search(
            r"Solde\s*[:\s]+([\d\s,\.]+)\s*(?:DA|DZD)?",
            soup.get_text(),
            re.IGNORECASE
        )

        return {
            "solde": self.parser.parse_amount(solde_match.group(1)) if solde_match else 0,
            "devise": "DZD"
        }

    async def telecharger_attestation_pdf(self, output_path: str) -> bool:
        """Télécharger l'attestation en PDF"""
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/attestation")

        pdf_button = await self._page.query_selector("a[href*='pdf'], .download-pdf")
        if pdf_button:
            async with self._page.expect_download() as download_info:
                await pdf_button.click()
            download = await download_info.value
            await download.save_as(output_path)
            return True

        await self._page.pdf(path=output_path)
        return True
