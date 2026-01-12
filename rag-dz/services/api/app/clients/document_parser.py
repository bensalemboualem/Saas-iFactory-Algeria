import PyPDF2
import docx
import io
from typing import List, Dict, Tuple
import re
import logging

logger = logging.getLogger(__name__)

class DocumentParser:
    @staticmethod
    def detect_language(text: str) -> str:
        """Détection basique de langue pour contexte algérien"""
        # Comptage caractères arabes
        arabic_chars = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))
        
        # Comptage mots français/anglais communs
        french_words = len(re.findall(r'\b(le|la|les|de|du|des|et|est|dans|pour|avec|sur|par|une|un)\b', text.lower()))
        english_words = len(re.findall(r'\b(the|and|is|in|for|with|on|by|a|an|of|to)\b', text.lower()))
        
        total_chars = len(text)
        if total_chars == 0:
            return "fr"
            
        arabic_ratio = arabic_chars / total_chars
        
        if arabic_ratio > 0.3:
            return "ar"
        elif english_words > french_words * 1.5:
            return "en"
        else:
            return "fr"  # Default pour l'Algérie
    
    @staticmethod
    def chunk_text(text: str, language: str, chunk_size: int = None) -> List[str]:
        """Chunking adaptatif selon la langue"""
        if chunk_size is None:
            chunk_sizes = {"ar": 800, "fr": 1200, "en": 1000}
            chunk_size = chunk_sizes.get(language, 1000)
        
        chunks = []
        current_chunk = ""
        
        paragraphs = text.split("\n\n")
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            if len(current_chunk) + len(paragraph) < chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk) > 50]
    
    @classmethod
    def parse_pdf(cls, file_content: bytes) -> Tuple[str, str]:
        """Parse PDF et retourne (texte, langue)"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            language = cls.detect_language(text)
            return text.strip(), language
            
        except Exception as e:
            logger.error(f"PDF parsing error: {e}")
            raise ValueError(f"Erreur lors du parsing PDF: {str(e)}")
    
    @classmethod
    def parse_docx(cls, file_content: bytes) -> Tuple[str, str]:
        """Parse DOCX et retourne (texte, langue)"""
        try:
            doc_file = io.BytesIO(file_content)
            doc = docx.Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            language = cls.detect_language(text)
            return text.strip(), language
            
        except Exception as e:
            logger.error(f"DOCX parsing error: {e}")
            raise ValueError(f"Erreur lors du parsing DOCX: {str(e)}")
    
    @classmethod
    def parse_txt(cls, file_content: bytes) -> Tuple[str, str]:
        """Parse TXT et retourne (texte, langue)"""
        try:
            try:
                text = file_content.decode('utf-8')
            except UnicodeDecodeError:
                text = file_content.decode('iso-8859-1')
            
            language = cls.detect_language(text)
            return text.strip(), language
            
        except Exception as e:
            logger.error(f"TXT parsing error: {e}")
            raise ValueError(f"Erreur lors du parsing TXT: {str(e)}")
    
    @classmethod
    def parse_file(cls, filename: str, file_content: bytes) -> Dict:
        """Parse fichier selon extension"""
        extension = filename.lower().split('.')[-1]
        
        parsers = {
            'pdf': cls.parse_pdf,
            'docx': cls.parse_docx,
            'txt': cls.parse_txt,
            'text': cls.parse_txt
        }
        
        if extension not in parsers:
            raise ValueError(f"Type de fichier non supporté: {extension}")
        
        text, language = parsers[extension](file_content)
        chunks = cls.chunk_text(text, language)
        
        return {
            'text': text,
            'language': language,
            'chunks': chunks,
            'filename': filename,
            'extension': extension
        }
