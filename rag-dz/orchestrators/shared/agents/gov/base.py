"""
Base classes for Algerian Government Service Agents.
These agents automate interactions with government websites.
"""

import os
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class GOVService(str, Enum):
    """Services gouvernementaux algériens"""
    CNAS = "cnas"           # Sécurité Sociale
    CASNOS = "casnos"       # Non-salariés
    CNRC = "cnrc"           # Registre de Commerce
    DGI = "dgi"             # Impôts
    SONELGAZ = "sonelgaz"   # Électricité et Gaz
    ADE = "ade"             # Eau
    ANDI = "andi"           # Investissement


class GOVCredentials(BaseModel):
    """Credentials for a government service"""
    service: GOVService
    username: str
    password: str
    nif: str | None = None  # Numéro d'Identification Fiscale
    nss: str | None = None  # Numéro de Sécurité Sociale
    rc: str | None = None   # Registre de Commerce


class GOVSession(BaseModel):
    """Active session with a government service"""
    service: GOVService
    session_id: str
    cookies: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
    user_info: dict = Field(default_factory=dict)


class GOVDocument(BaseModel):
    """Document retrieved from a government service"""
    service: GOVService
    doc_type: str
    doc_id: str | None = None
    title: str
    content: str | None = None
    html: str | None = None
    data: dict = Field(default_factory=dict)
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    valid_until: datetime | None = None


class GOVAgentBase(ABC):
    """
    Base class for government service agents.
    Provides common functionality for browser automation.
    """

    SERVICE: GOVService
    BASE_URL: str

    def __init__(
        self,
        credentials: GOVCredentials | None = None,
        headless: bool = True
    ):
        """
        Initialize the agent.

        Args:
            credentials: Login credentials
            headless: Run browser in headless mode
        """
        self.credentials = credentials
        self.headless = headless
        self.session: GOVSession | None = None
        self._browser = None
        self._page = None

    async def init_browser(self):
        """Initialize the browser (Playwright)"""
        try:
            from playwright.async_api import async_playwright

            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless
            )
            self._context = await self._browser.new_context(
                locale="fr-DZ",
                timezone_id="Africa/Algiers"
            )
            self._page = await self._context.new_page()

        except ImportError:
            raise RuntimeError("Playwright is required. Install with: pip install playwright")

    async def close(self):
        """Close the browser"""
        if self._browser:
            await self._browser.close()
        if hasattr(self, "_playwright") and self._playwright:
            await self._playwright.stop()

    @abstractmethod
    async def login(self) -> GOVSession:
        """
        Login to the service.

        Returns:
            Active session
        """
        pass

    @abstractmethod
    async def logout(self):
        """Logout from the service"""
        pass

    @abstractmethod
    async def get_attestation(self) -> GOVDocument:
        """
        Get the main attestation/certificate.

        Returns:
            GOVDocument
        """
        pass

    async def is_logged_in(self) -> bool:
        """Check if currently logged in"""
        return self.session is not None

    async def navigate(self, url: str):
        """Navigate to a URL"""
        if not self._page:
            await self.init_browser()
        await self._page.goto(url)

    async def get_page_content(self) -> str:
        """Get current page HTML content"""
        if not self._page:
            return ""
        return await self._page.content()

    async def screenshot(self, path: str):
        """Take a screenshot"""
        if self._page:
            await self._page.screenshot(path=path)

    async def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wait for an element"""
        if self._page:
            await self._page.wait_for_selector(selector, timeout=timeout)

    async def fill(self, selector: str, value: str):
        """Fill an input field"""
        if self._page:
            await self._page.fill(selector, value)

    async def click(self, selector: str):
        """Click an element"""
        if self._page:
            await self._page.click(selector)

    async def get_text(self, selector: str) -> str | None:
        """Get text content of an element"""
        if not self._page:
            return None
        element = await self._page.query_selector(selector)
        if element:
            return await element.text_content()
        return None

    async def get_attribute(self, selector: str, attr: str) -> str | None:
        """Get attribute of an element"""
        if not self._page:
            return None
        element = await self._page.query_selector(selector)
        if element:
            return await element.get_attribute(attr)
        return None


class ParserBase(ABC):
    """Base class for HTML parsers"""

    @staticmethod
    def clean_text(text: str | None) -> str:
        """Clean whitespace from text"""
        if not text:
            return ""
        return " ".join(text.split())

    @staticmethod
    def parse_date(date_str: str, format: str = "%d/%m/%Y") -> datetime | None:
        """Parse a date string"""
        try:
            return datetime.strptime(date_str.strip(), format)
        except ValueError:
            return None

    @staticmethod
    def parse_amount(amount_str: str) -> float:
        """Parse an amount string (handle DZD formatting)"""
        if not amount_str:
            return 0.0
        # Remove spaces, DA, DZD, etc.
        cleaned = amount_str.replace(" ", "").replace("DA", "").replace("DZD", "")
        cleaned = cleaned.replace(",", ".")
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    @abstractmethod
    async def parse(self, html: str) -> dict:
        """Parse HTML content"""
        pass
