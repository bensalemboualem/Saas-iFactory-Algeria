"""
Scrapers DZ - Collection de données algériennes
===============================================
Chaque scraper récupère les données d'une source officielle algérienne
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
import re
from io import BytesIO

# Pour PDF
try:
    import pypdf
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

logger = logging.getLogger("dz-scrapers")

# User-Agent pour éviter les blocages
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,ar;q=0.8",
}


class BaseScraper(ABC):
    """Classe de base pour tous les scrapers DZ"""
    
    source_name: str = ""
    source_url: str = ""
    doc_type: str = ""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=HEADERS)
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    @abstractmethod
    async def scrape(self) -> List[Dict]:
        """Récupère les documents de la source"""
        pass
    
    async def fetch_html(self, url: str) -> str:
        """Récupère le HTML d'une page"""
        async with self.session.get(url, timeout=30) as response:
            if response.status == 200:
                return await response.text()
            logger.error(f"Erreur HTTP {response.status} pour {url}")
            return ""
    
    async def fetch_pdf(self, url: str) -> str:
        """Récupère et extrait le texte d'un PDF"""
        if not PDF_AVAILABLE:
            logger.warning("pypdf non disponible, skip PDF")
            return ""
        
        try:
            async with self.session.get(url, timeout=60) as response:
                if response.status == 200:
                    pdf_bytes = await response.read()
                    return self.extract_pdf_text(pdf_bytes)
        except Exception as e:
            logger.error(f"Erreur PDF {url}: {e}")
        return ""
    
    def extract_pdf_text(self, pdf_bytes: bytes) -> str:
        """Extrait le texte d'un PDF"""
        try:
            reader = pypdf.PdfReader(BytesIO(pdf_bytes))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Erreur extraction PDF: {e}")
            return ""
    
    def clean_html(self, html: str) -> str:
        """Extrait le texte propre du HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Supprimer scripts et styles
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        text = soup.get_text(separator='\n')
        
        # Nettoyer
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    async def delay(self, seconds: float = 1.0):
        """Délai pour éviter le rate limiting"""
        await asyncio.sleep(seconds)


# ==================== JORADP ====================

class JORADPScraper(BaseScraper):
    """
    Scraper pour le Journal Officiel de la République Algérienne
    https://www.joradp.dz
    
    Récupère:
    - Lois
    - Décrets
    - Arrêtés
    - Décisions
    """
    
    source_name = "DZ_JO"
    source_url = "https://www.joradp.dz"
    doc_type = "law"
    
    async def scrape(self) -> List[Dict]:
        documents = []
        
        async with aiohttp.ClientSession(headers=HEADERS) as self.session:
            # Page d'accueil pour récupérer les derniers JO
            base_url = "https://www.joradp.dz/HAR/Index.htm"
            
            try:
                html = await self.fetch_html(base_url)
                if not html:
                    # Fallback: essayer les PDFs directement
                    return await self.scrape_recent_pdfs()
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Trouver les liens vers les JO
                links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
                
                for link in links[:10]:  # Limiter à 10 derniers
                    pdf_url = link.get('href')
                    if not pdf_url.startswith('http'):
                        pdf_url = f"{self.source_url}/{pdf_url}"
                    
                    await self.delay(2)  # Respecter le serveur
                    
                    text = await self.fetch_pdf(pdf_url)
                    if text and len(text) > 100:
                        # Extraire le titre du PDF
                        title = self.extract_jo_title(text, link.text)
                        date_str = self.extract_jo_date(pdf_url, text)
                        
                        documents.append({
                            "title": title,
                            "text": text,
                            "source_url": pdf_url,
                            "source_name": self.source_name,
                            "type": self.detect_doc_type(text),
                            "date": date_str
                        })
                        
                        logger.info(f"📜 JO récupéré: {title}")
                
            except Exception as e:
                logger.error(f"Erreur scraping JORADP: {e}")
        
        return documents
    
    async def scrape_recent_pdfs(self) -> List[Dict]:
        """Scrape les PDFs récents directement"""
        documents = []
        year = datetime.now().year
        
        # Format: F{year}{numero}.pdf
        for num in range(1, 10):
            pdf_url = f"https://www.joradp.dz/FTP/JO-FRANCAIS/{year}/F{year}0{num:02d}.pdf"
            
            try:
                text = await self.fetch_pdf(pdf_url)
                if text:
                    documents.append({
                        "title": f"Journal Officiel N°{num} - {year}",
                        "text": text,
                        "source_url": pdf_url,
                        "source_name": self.source_name,
                        "type": "law",
                        "date": f"{year}-01-{num:02d}"
                    })
            except:
                continue
            
            await self.delay(2)
        
        return documents
    
    def extract_jo_title(self, text: str, link_text: str) -> str:
        """Extrait le titre du JO"""
        # Chercher "JOURNAL OFFICIEL N°X"
        match = re.search(r'JOURNAL OFFICIEL.*?N[°o]\s*(\d+)', text, re.I)
        if match:
            return f"Journal Officiel N°{match.group(1)}"
        return link_text or "Journal Officiel"
    
    def extract_jo_date(self, url: str, text: str) -> str:
        """Extrait la date du JO"""
        # Essayer depuis l'URL
        match = re.search(r'/(\d{4})/', url)
        if match:
            year = match.group(1)
            return f"{year}-01-01"
        return datetime.now().strftime("%Y-%m-%d")
    
    def detect_doc_type(self, text: str) -> str:
        """Détecte le type de document"""
        text_lower = text.lower()[:2000]
        
        if "décret" in text_lower:
            return "decree"
        elif "loi n°" in text_lower or "loi de finances" in text_lower:
            return "law"
        elif "arrêté" in text_lower:
            return "decree"
        elif "circulaire" in text_lower:
            return "circular"
        return "law"


# ==================== DGI ====================

class DGIScraper(BaseScraper):
    """
    Scraper pour la Direction Générale des Impôts
    https://www.mfdgi.gov.dz
    
    Récupère:
    - Barèmes IRG, TVA, TAP
    - Notes et circulaires fiscales
    - Guides pratiques
    """
    
    source_name = "DZ_DGI"
    source_url = "https://www.mfdgi.gov.dz"
    doc_type = "tax"
    
    async def scrape(self) -> List[Dict]:
        documents = []
        
        async with aiohttp.ClientSession(headers=HEADERS) as self.session:
            # Pages principales à scraper
            pages = [
                "/index.php/fr/documentation/textes-reglementaires",
                "/index.php/fr/documentation/notes-et-circulaires",
                "/index.php/fr/documentation/guides-pratiques",
            ]
            
            for page in pages:
                try:
                    url = f"{self.source_url}{page}"
                    html = await self.fetch_html(url)
                    
                    if html:
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Chercher les articles/documents
                        articles = soup.find_all(['article', 'div'], class_=re.compile(r'item|article|document'))
                        
                        for article in articles[:10]:
                            title_tag = article.find(['h2', 'h3', 'a'])
                            title = title_tag.text.strip() if title_tag else "Document DGI"
                            
                            # Chercher lien PDF
                            pdf_link = article.find('a', href=re.compile(r'\.pdf$', re.I))
                            
                            if pdf_link:
                                pdf_url = pdf_link['href']
                                if not pdf_url.startswith('http'):
                                    pdf_url = f"{self.source_url}{pdf_url}"
                                
                                await self.delay(2)
                                text = await self.fetch_pdf(pdf_url)
                            else:
                                # Contenu HTML
                                text = article.get_text(separator='\n')
                            
                            if text and len(text) > 100:
                                documents.append({
                                    "title": title,
                                    "text": text,
                                    "source_url": url,
                                    "source_name": self.source_name,
                                    "type": "tax",
                                    "date": datetime.now().strftime("%Y-%m-%d")
                                })
                                
                                logger.info(f"💰 DGI document: {title}")
                    
                    await self.delay(2)
                    
                except Exception as e:
                    logger.error(f"Erreur scraping DGI {page}: {e}")
        
        return documents


# ==================== ONS ====================

class ONSScraper(BaseScraper):
    """
    Scraper pour l'Office National des Statistiques
    https://www.ons.dz
    
    Récupère:
    - Rapports statistiques
    - Indicateurs économiques
    - Publications
    """
    
    source_name = "DZ_ONS"
    source_url = "https://www.ons.dz"
    doc_type = "statistic"
    
    async def scrape(self) -> List[Dict]:
        documents = []
        
        async with aiohttp.ClientSession(headers=HEADERS) as self.session:
            # Publications récentes
            pages = [
                "/index.php?option=com_content&view=article&id=1",
                "/index.php?option=com_content&view=section&id=1",
            ]
            
            try:
                # Page principale
                html = await self.fetch_html(self.source_url)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Chercher les PDFs
                    pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
                    
                    for link in pdf_links[:10]:
                        pdf_url = link['href']
                        if not pdf_url.startswith('http'):
                            pdf_url = f"{self.source_url}/{pdf_url}"
                        
                        await self.delay(3)
                        text = await self.fetch_pdf(pdf_url)
                        
                        if text and len(text) > 200:
                            title = link.text.strip() or self.extract_title_from_pdf(text)
                            
                            documents.append({
                                "title": title,
                                "text": text,
                                "source_url": pdf_url,
                                "source_name": self.source_name,
                                "type": "statistic",
                                "date": datetime.now().strftime("%Y-%m-%d")
                            })
                            
                            logger.info(f"📊 ONS rapport: {title}")
                            
            except Exception as e:
                logger.error(f"Erreur scraping ONS: {e}")
        
        return documents
    
    def extract_title_from_pdf(self, text: str) -> str:
        """Extrait le titre du contenu PDF"""
        lines = text.split('\n')[:10]
        for line in lines:
            if len(line.strip()) > 10 and len(line.strip()) < 200:
                return line.strip()
        return "Rapport ONS"


# ==================== BANQUE D'ALGÉRIE ====================

class BankAlgeriaScraper(BaseScraper):
    """
    Scraper pour la Banque d'Algérie
    https://www.bank-of-algeria.dz
    
    Récupère:
    - Taux de change
    - Circulaires
    - Rapports annuels
    - Notes
    """
    
    source_name = "DZ_BANK"
    source_url = "https://www.bank-of-algeria.dz"
    doc_type = "circular"
    
    async def scrape(self) -> List[Dict]:
        documents = []
        
        async with aiohttp.ClientSession(headers=HEADERS) as self.session:
            sections = [
                "/html/circulaires.htm",
                "/html/rapports.htm",
                "/html/notes.htm",
            ]
            
            for section in sections:
                try:
                    url = f"{self.source_url}{section}"
                    html = await self.fetch_html(url)
                    
                    if html:
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Chercher les liens PDF
                        links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
                        
                        for link in links[:5]:
                            pdf_url = link['href']
                            if not pdf_url.startswith('http'):
                                pdf_url = f"{self.source_url}/html/{pdf_url}"
                            
                            await self.delay(2)
                            text = await self.fetch_pdf(pdf_url)
                            
                            if text:
                                title = link.text.strip() or "Document Banque d'Algérie"
                                
                                documents.append({
                                    "title": title,
                                    "text": text,
                                    "source_url": pdf_url,
                                    "source_name": self.source_name,
                                    "type": "circular",
                                    "date": datetime.now().strftime("%Y-%m-%d")
                                })
                                
                                logger.info(f"🏦 Banque d'Algérie: {title}")
                    
                    await self.delay(2)
                    
                except Exception as e:
                    logger.error(f"Erreur scraping Banque d'Algérie {section}: {e}")
        
        return documents


# ==================== DOUANES ====================

class DouanesScraper(BaseScraper):
    """
    Scraper pour les Douanes Algériennes
    https://www.douane.gov.dz
    
    Récupère:
    - Nomenclatures douanières
    - Notes d'importation/exportation
    - Tarifs douaniers
    """
    
    source_name = "DZ_DOUANE"
    source_url = "https://www.douane.gov.dz"
    doc_type = "procedure"
    
    async def scrape(self) -> List[Dict]:
        documents = []
        
        async with aiohttp.ClientSession(headers=HEADERS) as self.session:
            try:
                html = await self.fetch_html(self.source_url)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Récupérer les sections importantes
                    sections = soup.find_all(['div', 'section'], class_=re.compile(r'content|article|news'))
                    
                    for section in sections[:10]:
                        text = section.get_text(separator='\n').strip()
                        
                        if len(text) > 200:
                            title_tag = section.find(['h1', 'h2', 'h3'])
                            title = title_tag.text.strip() if title_tag else "Information Douanes"
                            
                            documents.append({
                                "title": title,
                                "text": text,
                                "source_url": self.source_url,
                                "source_name": self.source_name,
                                "type": "procedure",
                                "date": datetime.now().strftime("%Y-%m-%d")
                            })
                            
                            logger.info(f"🛃 Douanes: {title}")
                            
            except Exception as e:
                logger.error(f"Erreur scraping Douanes: {e}")
        
        return documents


# ==================== ANEM ====================

class ANEMScraper(BaseScraper):
    """
    Scraper pour l'ANEM (Agence Nationale de l'Emploi)
    https://www.anem.dz
    
    Récupère:
    - Procédures d'emploi
    - Réglementations
    - Offres et dispositifs
    """
    
    source_name = "DZ_ANEM"
    source_url = "https://www.anem.dz"
    doc_type = "procedure"
    
    async def scrape(self) -> List[Dict]:
        documents = []
        
        async with aiohttp.ClientSession(headers=HEADERS) as self.session:
            try:
                html = await self.fetch_html(self.source_url)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Sections importantes
                    articles = soup.find_all(['article', 'div'], class_=re.compile(r'content|post|article'))
                    
                    for article in articles[:10]:
                        text = article.get_text(separator='\n').strip()
                        
                        if len(text) > 150:
                            title_tag = article.find(['h1', 'h2', 'h3'])
                            title = title_tag.text.strip() if title_tag else "Information ANEM"
                            
                            documents.append({
                                "title": title,
                                "text": text,
                                "source_url": self.source_url,
                                "source_name": self.source_name,
                                "type": "procedure",
                                "date": datetime.now().strftime("%Y-%m-%d")
                            })
                            
                            logger.info(f"💼 ANEM: {title}")
                            
            except Exception as e:
                logger.error(f"Erreur scraping ANEM: {e}")
        
        return documents


# ==================== ANDI ====================

class ANDIScraper(BaseScraper):
    """
    Scraper pour l'ANDI (Agence Nationale de Développement de l'Investissement)
    https://andi.dz
    
    Récupère:
    - Procédures création entreprise
    - Avantages fiscaux
    - Guides investisseurs
    """
    
    source_name = "DZ_ANDI"
    source_url = "https://andi.dz"
    doc_type = "procedure"
    
    async def scrape(self) -> List[Dict]:
        documents = []
        
        async with aiohttp.ClientSession(headers=HEADERS) as self.session:
            pages = [
                "/index.php/fr/",
                "/index.php/fr/creer-son-entreprise",
                "/index.php/fr/avantages",
            ]
            
            for page in pages:
                try:
                    url = f"{self.source_url}{page}"
                    html = await self.fetch_html(url)
                    
                    if html:
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Contenu principal
                        main = soup.find(['main', 'article', 'div'], class_=re.compile(r'content|main'))
                        
                        if main:
                            text = main.get_text(separator='\n').strip()
                            
                            if len(text) > 200:
                                title_tag = main.find(['h1', 'h2'])
                                title = title_tag.text.strip() if title_tag else "Guide ANDI"
                                
                                documents.append({
                                    "title": title,
                                    "text": text,
                                    "source_url": url,
                                    "source_name": self.source_name,
                                    "type": "procedure",
                                    "date": datetime.now().strftime("%Y-%m-%d")
                                })
                                
                                logger.info(f"🏢 ANDI: {title}")
                    
                    await self.delay(2)
                    
                except Exception as e:
                    logger.error(f"Erreur scraping ANDI {page}: {e}")
        
        return documents


# ==================== NEWS ====================

class NewsScraper(BaseScraper):
    """
    Scraper pour les actualités économiques algériennes
    
    Sources:
    - APS (Algérie Presse Service)
    - TSA (Tout Sur l'Algérie)
    - El Moudjahid
    """
    
    source_name = "DZ_NEWS"
    source_url = "multiple"
    doc_type = "news"
    
    NEWS_SOURCES = [
        {"name": "APS", "url": "https://www.aps.dz/economie", "selector": "article"},
        {"name": "TSA", "url": "https://www.tsa-algerie.com/economie/", "selector": ".post"},
        {"name": "ElMoudjahid", "url": "https://www.elmoudjahid.dz/fr/economie", "selector": "article"},
    ]
    
    async def scrape(self) -> List[Dict]:
        documents = []
        
        async with aiohttp.ClientSession(headers=HEADERS) as self.session:
            for source in self.NEWS_SOURCES:
                try:
                    html = await self.fetch_html(source["url"])
                    
                    if html:
                        soup = BeautifulSoup(html, 'html.parser')
                        articles = soup.select(source["selector"])[:5]
                        
                        for article in articles:
                            # Titre
                            title_tag = article.find(['h1', 'h2', 'h3', 'a'])
                            title = title_tag.text.strip() if title_tag else "Actualité"
                            
                            # Lien article complet
                            link = article.find('a', href=True)
                            article_url = link['href'] if link else source["url"]
                            
                            if not article_url.startswith('http'):
                                article_url = f"{source['url'].rsplit('/', 1)[0]}/{article_url}"
                            
                            # Contenu
                            text = article.get_text(separator='\n').strip()
                            
                            # Si le contenu est court, récupérer l'article complet
                            if len(text) < 300 and link:
                                await self.delay(1)
                                full_html = await self.fetch_html(article_url)
                                if full_html:
                                    full_soup = BeautifulSoup(full_html, 'html.parser')
                                    content = full_soup.find(['article', 'div'], class_=re.compile(r'content|post|article'))
                                    if content:
                                        text = content.get_text(separator='\n').strip()
                            
                            if len(text) > 100:
                                documents.append({
                                    "title": f"[{source['name']}] {title}",
                                    "text": text,
                                    "source_url": article_url,
                                    "source_name": self.source_name,
                                    "type": "news",
                                    "date": datetime.now().strftime("%Y-%m-%d")
                                })
                                
                                logger.info(f"📰 News {source['name']}: {title[:50]}...")
                    
                    await self.delay(2)
                    
                except Exception as e:
                    logger.error(f"Erreur scraping news {source['name']}: {e}")
        
        return documents


# ==================== EXPORT ====================

__all__ = [
    'JORADPScraper',
    'DGIScraper', 
    'ONSScraper',
    'BankAlgeriaScraper',
    'DouanesScraper',
    'ANEMScraper',
    'ANDIScraper',
    'NewsScraper',
]
