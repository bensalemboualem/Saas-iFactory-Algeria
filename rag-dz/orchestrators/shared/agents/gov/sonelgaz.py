"""
Sonelgaz Agent - Société Nationale de l'Électricité et du Gaz.
Automatise les interactions avec le portail Sonelgaz.
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


class SonelgazFacture(BaseModel):
    """Facture Sonelgaz"""
    numero: str
    reference_client: str
    periode: str  # Format: "MM/YYYY - MM/YYYY"
    type_energie: str  # electricite, gaz, ou les deux
    montant_ht: float
    tva: float
    montant_ttc: float
    date_emission: str | None = None
    date_echeance: str | None = None
    statut: str = "en_attente"  # payee, en_attente, en_retard
    consommation_kwh: float | None = None
    consommation_m3: float | None = None


class SonelgazConsommation(BaseModel):
    """Consommation mensuelle Sonelgaz"""
    mois: str
    annee: int
    electricite_kwh: float | None = None
    gaz_m3: float | None = None
    montant_electricite: float | None = None
    montant_gaz: float | None = None
    index_electricite: int | None = None
    index_gaz: int | None = None


class SonelgazContrat(BaseModel):
    """Contrat Sonelgaz"""
    numero_contrat: str
    reference_client: str
    nom_titulaire: str
    adresse: str
    wilaya: str
    type_contrat: str  # domestique, professionnel, industriel
    puissance_souscrite: float | None = None
    date_debut: str | None = None
    statut: str = "actif"


class SonelgazParser(ParserBase):
    """
    Parser pour les pages Sonelgaz.
    Extrait les données des factures et consommations.
    """

    async def parse(self, html: str) -> dict:
        """Parse generic Sonelgaz page"""
        soup = BeautifulSoup(html, "html.parser")
        return {
            "title": self._get_title(soup),
            "content": self._get_main_content(soup)
        }

    def _get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find("h1") or soup.find("title")
        return self.clean_text(title.text) if title else ""

    def _get_main_content(self, soup: BeautifulSoup) -> str:
        main = soup.find("main") or soup.find("div", class_="content")
        return self.clean_text(main.text) if main else ""

    async def parse_facture(self, html: str) -> SonelgazFacture | None:
        """
        Parse une facture Sonelgaz.

        Args:
            html: HTML de la page facture

        Returns:
            SonelgazFacture ou None
        """
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        data = {}

        patterns = {
            "numero": r"N[°o]\s*(?:facture)?\s*[:\s]+([A-Z0-9/-]+)",
            "reference_client": r"(?:Réf[\.é]rence|Client)\s*[:\s]+([A-Z0-9/-]+)",
            "periode": r"Période\s*[:\s]+(.+?)(?:\n|$)",
            "montant_ht": r"(?:Montant\s*HT|HT)\s*[:\s]+([\d\s,\.]+)\s*(?:DA|DZD)?",
            "tva": r"TVA\s*[:\s]+([\d\s,\.]+)\s*(?:DA|DZD)?",
            "montant_ttc": r"(?:Montant\s*TTC|TTC|Total)\s*[:\s]+([\d\s,\.]+)\s*(?:DA|DZD)?",
            "date_emission": r"(?:Date\s*d'émission|Émis\s*le)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
            "date_echeance": r"(?:Date\s*d'échéance|À\s*payer\s*avant)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
            "consommation_kwh": r"(?:Consommation|Électricité)\s*[:\s]+([\d\s,\.]+)\s*kWh",
            "consommation_m3": r"(?:Gaz|Consommation\s*gaz)\s*[:\s]+([\d\s,\.]+)\s*m[³3]",
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = self.clean_text(match.group(1))
                if field in ["montant_ht", "tva", "montant_ttc", "consommation_kwh", "consommation_m3"]:
                    data[field] = self.parse_amount(value)
                else:
                    data[field] = value

        # Déterminer le type d'énergie
        type_energie = "electricite_gaz"
        if data.get("consommation_kwh") and not data.get("consommation_m3"):
            type_energie = "electricite"
        elif data.get("consommation_m3") and not data.get("consommation_kwh"):
            type_energie = "gaz"

        # Déterminer le statut
        statut = "en_attente"
        if re.search(r"payée?|réglée?", text, re.IGNORECASE):
            statut = "payee"
        elif re.search(r"retard|impayée?", text, re.IGNORECASE):
            statut = "en_retard"

        if not data.get("numero") and not data.get("reference_client"):
            return None

        return SonelgazFacture(
            numero=data.get("numero", ""),
            reference_client=data.get("reference_client", ""),
            periode=data.get("periode", ""),
            type_energie=type_energie,
            montant_ht=data.get("montant_ht", 0),
            tva=data.get("tva", 0),
            montant_ttc=data.get("montant_ttc", 0),
            date_emission=data.get("date_emission"),
            date_echeance=data.get("date_echeance"),
            statut=statut,
            consommation_kwh=data.get("consommation_kwh"),
            consommation_m3=data.get("consommation_m3"),
        )

    async def parse_consommation(self, html: str) -> list[SonelgazConsommation]:
        """
        Parse l'historique de consommation.

        Args:
            html: HTML de la page d'historique

        Returns:
            Liste de SonelgazConsommation
        """
        soup = BeautifulSoup(html, "html.parser")
        consommations = []

        # Chercher le tableau de consommation
        table = soup.find("table", class_=re.compile(r"consommation|historique", re.I))
        if not table:
            table = soup.find("table")

        if not table:
            return consommations

        rows = table.find_all("tr")[1:]  # Skip header

        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) >= 3:
                try:
                    # Parser la période (format: "Janvier 2024" ou "01/2024")
                    periode_text = self.clean_text(cols[0].text)
                    mois_match = re.search(r"(\w+)\s*(\d{4})", periode_text)
                    if mois_match:
                        mois = mois_match.group(1)
                        annee = int(mois_match.group(2))
                    else:
                        date_match = re.search(r"(\d{2})/(\d{4})", periode_text)
                        if date_match:
                            mois = date_match.group(1)
                            annee = int(date_match.group(2))
                        else:
                            continue

                    consommation = SonelgazConsommation(
                        mois=mois,
                        annee=annee,
                        electricite_kwh=self.parse_amount(cols[1].text) if len(cols) > 1 else None,
                        gaz_m3=self.parse_amount(cols[2].text) if len(cols) > 2 else None,
                        montant_electricite=self.parse_amount(cols[3].text) if len(cols) > 3 else None,
                        montant_gaz=self.parse_amount(cols[4].text) if len(cols) > 4 else None,
                    )
                    consommations.append(consommation)
                except Exception:
                    continue

        return consommations

    async def parse_contrat(self, html: str) -> SonelgazContrat | None:
        """
        Parse les informations du contrat.

        Args:
            html: HTML de la page contrat

        Returns:
            SonelgazContrat ou None
        """
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        data = {}

        patterns = {
            "numero_contrat": r"N[°o]\s*(?:contrat)?\s*[:\s]+([A-Z0-9/-]+)",
            "reference_client": r"(?:Réf[\.é]rence|Client)\s*[:\s]+([A-Z0-9/-]+)",
            "nom_titulaire": r"(?:Titulaire|Nom)\s*[:\s]+([A-ZÀ-Ü\s]+)",
            "adresse": r"Adresse\s*[:\s]+(.+?)(?:\n|Wilaya)",
            "wilaya": r"Wilaya\s*[:\s]+(\d{2}\s*-\s*[A-ZÀ-Ü\s]+|\d{2})",
            "type_contrat": r"Type\s*(?:de\s*)?(?:contrat)?\s*[:\s]+(domestique|professionnel|industriel)",
            "puissance_souscrite": r"Puissance\s*(?:souscrite)?\s*[:\s]+([\d,\.]+)\s*kVA",
            "date_debut": r"(?:Date\s*de\s*début|Depuis\s*le)\s*[:\s]+(\d{2}/\d{2}/\d{4})",
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = self.clean_text(match.group(1))
                if field == "puissance_souscrite":
                    data[field] = self.parse_amount(value)
                else:
                    data[field] = value

        if not data.get("numero_contrat") and not data.get("reference_client"):
            return None

        return SonelgazContrat(
            numero_contrat=data.get("numero_contrat", ""),
            reference_client=data.get("reference_client", ""),
            nom_titulaire=data.get("nom_titulaire", ""),
            adresse=data.get("adresse", ""),
            wilaya=data.get("wilaya", ""),
            type_contrat=data.get("type_contrat", "domestique"),
            puissance_souscrite=data.get("puissance_souscrite"),
            date_debut=data.get("date_debut"),
        )


class SonelgazAgent(GOVAgentBase):
    """
    Agent pour le portail Sonelgaz (Électricité et Gaz Algérie).

    Fonctionnalités:
    - Connexion au compte client
    - Consultation des factures
    - Historique de consommation
    - Informations contrat
    - Téléchargement factures PDF
    """

    SERVICE = GOVService.SONELGAZ
    BASE_URL = "https://www.sonelgaz.dz"
    PORTAL_URL = "https://client.sonelgaz.dz"

    def __init__(self, credentials: GOVCredentials | None = None, headless: bool = True):
        super().__init__(credentials, headless)
        self.parser = SonelgazParser()

    async def login(self) -> GOVSession:
        """
        Se connecter au portail Sonelgaz.

        Returns:
            Session active
        """
        if not self.credentials:
            raise ValueError("Credentials required for login")

        await self.init_browser()
        await self.navigate(f"{self.PORTAL_URL}/login")

        # Attendre le formulaire
        await self.wait_for_selector("input[name='email'], input[name='username']")

        # Remplir les credentials
        email_field = await self._page.query_selector("input[name='email']")
        if email_field:
            await self.fill("input[name='email']", self.credentials.username)
        else:
            await self.fill("input[name='username']", self.credentials.username)

        await self.fill("input[name='password']", self.credentials.password)

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
        Récupérer le contrat (attestation principale).

        Returns:
            GOVDocument avec le contrat
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/contrat")
        await self.wait_for_selector(".contrat, .contract, main")

        html = await self.get_page_content()
        contrat = await self.parser.parse_contrat(html)

        return GOVDocument(
            service=self.SERVICE,
            doc_type="contrat",
            title="Contrat Sonelgaz",
            html=html,
            data=contrat.model_dump() if contrat else {}
        )

    async def get_derniere_facture(self) -> SonelgazFacture | None:
        """
        Récupérer la dernière facture.

        Returns:
            SonelgazFacture
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/factures")
        await self.wait_for_selector(".facture, .invoice, table")

        # Cliquer sur la première facture
        first_facture = await self._page.query_selector(
            ".facture:first-child, tr.facture:first-child, tbody tr:first-child"
        )
        if first_facture:
            await first_facture.click()
            await self._page.wait_for_load_state("networkidle")

        html = await self.get_page_content()
        return await self.parser.parse_facture(html)

    async def get_historique_factures(self, limit: int = 12) -> list[SonelgazFacture]:
        """
        Récupérer l'historique des factures.

        Args:
            limit: Nombre maximum de factures

        Returns:
            Liste de SonelgazFacture
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/factures/historique")
        await self.wait_for_selector("table, .factures")

        factures = []
        html = await self.get_page_content()

        # Parser le tableau des factures
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("tbody tr, .facture-row")[:limit]

        for row in rows:
            # Cliquer pour voir les détails
            row_id = row.get("data-id") or row.get("id")
            if row_id:
                try:
                    await self.click(f"[data-id='{row_id}'], #{row_id}")
                    await self._page.wait_for_load_state("networkidle")
                    detail_html = await self.get_page_content()
                    facture = await self.parser.parse_facture(detail_html)
                    if facture:
                        factures.append(facture)
                    await self._page.go_back()
                except Exception:
                    continue

        return factures

    async def get_historique_consommation(self, mois: int = 12) -> list[SonelgazConsommation]:
        """
        Récupérer l'historique de consommation.

        Args:
            mois: Nombre de mois d'historique

        Returns:
            Liste de SonelgazConsommation
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/consommation/historique")
        await self.wait_for_selector("table, .chart, .consommation")

        html = await self.get_page_content()
        consommations = await self.parser.parse_consommation(html)

        return consommations[:mois]

    async def telecharger_facture_pdf(self, facture_numero: str, output_path: str) -> bool:
        """
        Télécharger une facture en PDF.

        Args:
            facture_numero: Numéro de la facture
            output_path: Chemin du fichier de sortie

        Returns:
            True si succès
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/factures/{facture_numero}")

        # Chercher le bouton de téléchargement
        pdf_button = await self._page.query_selector(
            "a[href*='pdf'], button[data-format='pdf'], .download-pdf, .telecharger"
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

    async def payer_facture(self, facture_numero: str) -> str:
        """
        Initier le paiement d'une facture (redirige vers la page de paiement).

        Args:
            facture_numero: Numéro de la facture

        Returns:
            URL de paiement
        """
        if not self.session:
            await self.login()

        await self.navigate(f"{self.PORTAL_URL}/factures/{facture_numero}/payer")

        # Récupérer l'URL de paiement
        return self._page.url
