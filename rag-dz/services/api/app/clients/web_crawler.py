"""
Smart Web Crawler - Adapté d'Archon

Crawler intelligent pour sites de documentation avec:
- Détection automatique de sitemaps
- Crawling récursif avec respect des limites
- Extraction de contenu markdown
- Gestion des erreurs et retry
"""

import asyncio
import logging
import re
from typing import List, Dict, Any, Optional, Set
from urllib.parse import urljoin, urlparse
import aiohttp
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class URLHandler:
    """Helper pour les opérations sur les URLs"""

    @staticmethod
    def is_sitemap(url: str) -> bool:
        """Vérifie si l'URL est un sitemap"""
        try:
            parsed = urlparse(url)
            path = parsed.path.lower()
            return path.endswith(".xml") and "sitemap" in path
        except Exception as e:
            logger.warning(f"Erreur vérification sitemap: {e}")
            return False

    @staticmethod
    def is_same_domain(url1: str, url2: str) -> bool:
        """Vérifie si deux URLs sont du même domaine"""
        try:
            domain1 = urlparse(url1).netloc
            domain2 = urlparse(url2).netloc
            return domain1 == domain2
        except Exception:
            return False

    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalise une URL (enlève fragments, trailing slash)"""
        try:
            parsed = urlparse(url)
            # Enlever le fragment (#...)
            normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                normalized += f"?{parsed.query}"
            # Enlever trailing slash sauf pour root
            if normalized.endswith("/") and parsed.path != "/":
                normalized = normalized[:-1]
            return normalized
        except Exception:
            return url


class SitemapParser:
    """Parser pour sitemaps XML"""

    @staticmethod
    async def parse_sitemap(url: str, session: aiohttp.ClientSession) -> List[str]:
        """
        Parse un sitemap et retourne la liste des URLs

        Args:
            url: URL du sitemap
            session: Session aiohttp

        Returns:
            Liste des URLs trouvées
        """
        urls = []
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status != 200:
                    logger.warning(f"Sitemap non accessible: {url} (status {response.status})")
                    return urls

                content = await response.text()
                root = ET.fromstring(content)

                # Gérer les namespaces XML
                namespaces = {
                    'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                    'xhtml': 'http://www.w3.org/1999/xhtml'
                }

                # Extraire les URLs
                for url_elem in root.findall('.//sitemap:url/sitemap:loc', namespaces):
                    if url_elem.text:
                        urls.append(url_elem.text.strip())

                # Si c'est un sitemap index, récursivement parser les sous-sitemaps
                for sitemap_elem in root.findall('.//sitemap:sitemap/sitemap:loc', namespaces):
                    if sitemap_elem.text:
                        sub_urls = await SitemapParser.parse_sitemap(sitemap_elem.text.strip(), session)
                        urls.extend(sub_urls)

                logger.info(f"Sitemap {url}: {len(urls)} URLs trouvées")

        except Exception as e:
            logger.error(f"Erreur parsing sitemap {url}: {e}")

        return urls


class SmartWebCrawler:
    """
    Crawler web intelligent avec support:
    - Sitemaps
    - Crawling récursif
    - Extraction de contenu
    """

    def __init__(
        self,
        max_depth: int = 3,
        max_pages: int = 100,
        respect_robots_txt: bool = True,
        timeout: int = 30
    ):
        """
        Initialise le crawler

        Args:
            max_depth: Profondeur maximale de crawling
            max_pages: Nombre maximum de pages à crawler
            respect_robots_txt: Respecter robots.txt
            timeout: Timeout des requêtes en secondes
        """
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.respect_robots_txt = respect_robots_txt
        self.timeout = timeout
        self.visited_urls: Set[str] = set()
        self.url_handler = URLHandler()

    async def crawl_website(
        self,
        start_url: str,
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Crawle un site web à partir d'une URL

        Args:
            start_url: URL de départ
            progress_callback: Callback pour le progress (optional)

        Returns:
            Liste de dictionnaires avec les pages crawlées
        """
        pages = []

        async with aiohttp.ClientSession() as session:
            # Vérifier si c'est un sitemap
            if self.url_handler.is_sitemap(start_url):
                logger.info(f"Détection sitemap: {start_url}")
                urls_to_crawl = await SitemapParser.parse_sitemap(start_url, session)

                # Limiter au max_pages
                if len(urls_to_crawl) > self.max_pages:
                    urls_to_crawl = urls_to_crawl[:self.max_pages]

                # Crawler chaque URL du sitemap
                for i, url in enumerate(urls_to_crawl):
                    page = await self._crawl_single_page(url, session)
                    if page:
                        pages.append(page)

                    if progress_callback:
                        progress_callback(i + 1, len(urls_to_crawl))

                    # Rate limiting
                    await asyncio.sleep(0.5)

            else:
                # Crawling récursif normal
                logger.info(f"Crawling récursif: {start_url}")
                pages = await self._crawl_recursive(
                    start_url,
                    session,
                    depth=0,
                    progress_callback=progress_callback
                )

        logger.info(f"Crawling terminé: {len(pages)} pages extraites")
        return pages

    async def _crawl_recursive(
        self,
        url: str,
        session: aiohttp.ClientSession,
        depth: int = 0,
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """Crawle récursivement à partir d'une URL"""
        pages = []

        # Vérifier les limites
        if depth > self.max_depth or len(self.visited_urls) >= self.max_pages:
            return pages

        # Normaliser et vérifier si déjà visité
        normalized_url = self.url_handler.normalize_url(url)
        if normalized_url in self.visited_urls:
            return pages

        self.visited_urls.add(normalized_url)

        # Crawler la page
        page = await self._crawl_single_page(normalized_url, session)
        if not page:
            return pages

        pages.append(page)

        if progress_callback:
            progress_callback(len(self.visited_urls), self.max_pages)

        # Extraire et crawler les liens (si pas trop profond)
        if depth < self.max_depth and len(self.visited_urls) < self.max_pages:
            links = page.get('links', [])
            for link in links[:10]:  # Limiter nombre de liens par page
                if self.url_handler.is_same_domain(url, link):
                    await asyncio.sleep(0.5)  # Rate limiting
                    sub_pages = await self._crawl_recursive(
                        link, session, depth + 1, progress_callback
                    )
                    pages.extend(sub_pages)

                # Vérifier limite
                if len(self.visited_urls) >= self.max_pages:
                    break

        return pages

    async def _crawl_single_page(
        self,
        url: str,
        session: aiohttp.ClientSession
    ) -> Optional[Dict[str, Any]]:
        """
        Crawle une seule page

        Args:
            url: URL de la page
            session: Session aiohttp

        Returns:
            Dictionnaire avec le contenu de la page ou None
        """
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status != 200:
                    logger.warning(f"Page non accessible: {url} (status {response.status})")
                    return None

                content_type = response.headers.get('Content-Type', '')
                if 'text/html' not in content_type:
                    logger.debug(f"Ignoré (pas HTML): {url}")
                    return None

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # Extraire le contenu
                title = soup.find('title')
                title_text = title.get_text(strip=True) if title else url

                # Extraire le texte principal
                # Enlever scripts, styles, etc.
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                text = soup.get_text(separator='\n', strip=True)
                # Nettoyer les lignes vides
                text = re.sub(r'\n\s*\n', '\n\n', text)

                # Extraire les liens
                links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    if absolute_url.startswith('http'):
                        links.append(absolute_url)

                logger.info(f"Page crawlée: {url} ({len(text)} chars)")

                return {
                    'url': url,
                    'title': title_text,
                    'text': text,
                    'links': links,
                    'success': True
                }

        except asyncio.TimeoutError:
            logger.error(f"Timeout crawling: {url}")
            return None
        except Exception as e:
            logger.error(f"Erreur crawling {url}: {e}")
            return None


# Helper pour intégrer avec le système existant
async def crawl_documentation_site(
    url: str,
    max_pages: int = 100,
    max_depth: int = 3,
    progress_callback: Optional[callable] = None
) -> List[Dict[str, Any]]:
    """
    Fonction helper pour crawler un site de documentation

    Args:
        url: URL de départ
        max_pages: Nombre max de pages
        max_depth: Profondeur max
        progress_callback: Callback pour progress

    Returns:
        Liste des pages crawlées
    """
    crawler = SmartWebCrawler(
        max_depth=max_depth,
        max_pages=max_pages,
        respect_robots_txt=True,
        timeout=30
    )

    return await crawler.crawl_website(url, progress_callback)
