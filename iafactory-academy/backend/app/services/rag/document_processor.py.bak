"""
Document Processor for RAG
Handles parsing, chunking and metadata extraction
"""

import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import markdown


class DocumentType(str, Enum):
    """Types of documents"""
    COURSE = "cours"
    QUIZ = "quiz"
    EXAM = "examen"
    GUIDE = "guide"
    STRUCTURE = "structure"
    PORTAL = "portail"


class EducationLevel(str, Enum):
    """Education levels"""
    PRIMARY = "primaire"
    MIDDLE = "college"
    HIGH = "lycee"
    TEACHERS = "enseignants"


@dataclass
class DocumentMetadata:
    """Metadata for a processed document"""
    title: str
    doc_type: str
    level: Optional[str] = None
    module: Optional[str] = None
    language: str = "fr"
    duration_hours: Optional[float] = None
    credits: Optional[int] = None
    difficulty: Optional[str] = None
    source_file: Optional[str] = None
    chunk_index: int = 0
    total_chunks: int = 1
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "doc_type": self.doc_type,
            "level": self.level,
            "module": self.module,
            "language": self.language,
            "duration_hours": self.duration_hours,
            "credits": self.credits,
            "difficulty": self.difficulty,
            "source_file": self.source_file,
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
            "tags": ",".join(self.tags) if self.tags else ""
        }


class DocumentProcessor:
    """Process documents for RAG ingestion"""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        separators: Optional[List[str]] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators or ["\n\n", "\n", ". ", " ", ""],
            length_function=len
        )

    def detect_language(self, text: str) -> str:
        """Detect language from text content"""
        # Simple heuristic based on character patterns
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        if arabic_pattern.search(text[:500]):
            return "ar"

        # Check for French-specific words
        french_indicators = ["cours", "module", "leçon", "objectifs", "évaluation", "lycée"]
        text_lower = text.lower()
        french_count = sum(1 for word in french_indicators if word in text_lower)

        if french_count >= 2:
            return "fr"
        return "en"

    def parse_html(self, html_content: str) -> Dict[str, Any]:
        """Parse HTML content and extract structured data"""
        soup = BeautifulSoup(html_content, 'lxml')

        # Extract title
        title = ""
        if soup.title:
            title = soup.title.string or ""
        elif soup.find('h1'):
            title = soup.find('h1').get_text(strip=True)

        # Extract main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        text_content = main_content.get_text(separator='\n', strip=True) if main_content else ""

        # Extract code blocks
        code_blocks = []
        for code in soup.find_all(['code', 'pre']):
            code_blocks.append(code.get_text())

        # Extract sections
        sections = []
        for section in soup.find_all(['section', 'div'], class_=re.compile(r'module|lesson|chapter')):
            section_title = section.find(['h2', 'h3', 'h4'])
            sections.append({
                "title": section_title.get_text(strip=True) if section_title else "",
                "content": section.get_text(separator='\n', strip=True)
            })

        return {
            "title": title,
            "content": text_content,
            "code_blocks": code_blocks,
            "sections": sections,
            "language": self.detect_language(text_content)
        }

    def parse_markdown(self, md_content: str) -> Dict[str, Any]:
        """Parse Markdown content"""
        # Convert to HTML for consistent parsing
        html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        result = self.parse_html(html)

        # Also keep raw markdown for better chunking
        result["raw_content"] = md_content
        return result

    def parse_json(self, json_content: str) -> Dict[str, Any]:
        """Parse JSON content (structure files)"""
        try:
            data = json.loads(json_content)
            return {
                "title": data.get("title", data.get("name", "Structure")),
                "content": json.dumps(data, ensure_ascii=False, indent=2),
                "data": data,
                "language": "fr"
            }
        except json.JSONDecodeError:
            return {
                "title": "JSON Document",
                "content": json_content,
                "data": {},
                "language": "fr"
            }

    def extract_metadata(
        self,
        parsed_content: Dict[str, Any],
        source_file: str,
        doc_type: DocumentType = DocumentType.COURSE
    ) -> DocumentMetadata:
        """Extract metadata from parsed content"""
        content = parsed_content.get("content", "")
        title = parsed_content.get("title", "Document")

        # Detect level from content
        level = None
        level_patterns = {
            EducationLevel.PRIMARY.value: r"primaire|primary|ابتدائي",
            EducationLevel.MIDDLE.value: r"collège|college|middle|متوسط",
            EducationLevel.HIGH.value: r"lycée|lycee|high.?school|ثانوي",
            EducationLevel.TEACHERS.value: r"enseignant|teacher|formateur|معلم"
        }
        for level_name, pattern in level_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                level = level_name
                break

        # Detect module
        module = None
        module_match = re.search(r"Module\s+([A-Z]\d+|[LP]\d+)", content, re.IGNORECASE)
        if module_match:
            module = module_match.group(1).upper()

        # Extract duration
        duration = None
        duration_match = re.search(r"(\d+)\s*(?:heures?|h|hours?)", content, re.IGNORECASE)
        if duration_match:
            duration = float(duration_match.group(1))

        # Extract tags
        tags = []
        tag_patterns = ["IA", "LLM", "Machine Learning", "Python", "Transformers", "NLP", "Vision"]
        for tag in tag_patterns:
            if tag.lower() in content.lower():
                tags.append(tag)

        return DocumentMetadata(
            title=title,
            doc_type=doc_type.value,
            level=level,
            module=module,
            language=parsed_content.get("language", "fr"),
            duration_hours=duration,
            source_file=source_file,
            tags=tags
        )

    def chunk_document(
        self,
        content: str,
        metadata: DocumentMetadata
    ) -> List[Document]:
        """
        Split document into chunks with metadata

        Args:
            content: Full text content
            metadata: Base metadata for the document

        Returns:
            List of LangChain Document objects
        """
        chunks = self.text_splitter.split_text(content)

        documents = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.to_dict()
            chunk_metadata["chunk_index"] = i
            chunk_metadata["total_chunks"] = len(chunks)

            documents.append(Document(
                page_content=chunk,
                metadata=chunk_metadata
            ))

        return documents

    def process_file(
        self,
        file_content: str,
        file_name: str,
        file_type: str = "auto"
    ) -> List[Document]:
        """
        Process a file and return chunked documents

        Args:
            file_content: Raw file content
            file_name: Name of the source file
            file_type: Type of file (html, md, json, auto)

        Returns:
            List of processed Document objects
        """
        # Auto-detect file type
        if file_type == "auto":
            if file_name.endswith('.html'):
                file_type = "html"
            elif file_name.endswith('.md'):
                file_type = "md"
            elif file_name.endswith('.json'):
                file_type = "json"
            else:
                file_type = "text"

        # Parse content
        if file_type == "html":
            parsed = self.parse_html(file_content)
        elif file_type == "md":
            parsed = self.parse_markdown(file_content)
        elif file_type == "json":
            parsed = self.parse_json(file_content)
        else:
            parsed = {
                "title": file_name,
                "content": file_content,
                "language": self.detect_language(file_content)
            }

        # Detect document type from filename
        doc_type = DocumentType.COURSE
        if "quiz" in file_name.lower() or "exam" in file_name.lower():
            doc_type = DocumentType.QUIZ
        elif "guide" in file_name.lower() or "formation" in file_name.lower():
            doc_type = DocumentType.GUIDE
        elif "structure" in file_name.lower():
            doc_type = DocumentType.STRUCTURE
        elif "portail" in file_name.lower() or "portal" in file_name.lower():
            doc_type = DocumentType.PORTAL

        # Extract metadata
        metadata = self.extract_metadata(parsed, file_name, doc_type)

        # Chunk and return
        content = parsed.get("raw_content", parsed.get("content", ""))
        return self.chunk_document(content, metadata)

    def process_bbc_structure(self, json_content: str) -> List[Document]:
        """
        Special processing for BBC School structure JSON

        Extracts modules, lessons, and metadata from the master structure file
        """
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError:
            return []

        documents = []

        # Process each level
        levels = data.get("levels", data.get("niveaux", []))
        for level in levels:
            level_name = level.get("name", level.get("nom", ""))
            level_id = level.get("id", "")

            # Process modules
            modules = level.get("modules", [])
            for module in modules:
                module_name = module.get("name", module.get("nom", ""))
                module_id = module.get("id", "")

                # Create module document
                module_content = f"""
Module: {module_name}
Niveau: {level_name}
ID: {module_id}
Durée: {module.get('duration', module.get('duree', 'N/A'))} heures
Crédits: {module.get('credits', 'N/A')}

Objectifs:
{chr(10).join('- ' + obj for obj in module.get('objectives', module.get('objectifs', [])))}

Contenu:
{chr(10).join('- ' + lesson for lesson in module.get('lessons', module.get('lecons', [])))}
"""
                metadata = DocumentMetadata(
                    title=f"{level_name} - {module_name}",
                    doc_type=DocumentType.STRUCTURE.value,
                    level=level_name.lower(),
                    module=module_id,
                    language="fr",
                    duration_hours=module.get('duration', module.get('duree')),
                    credits=module.get('credits'),
                    source_file="programme_complet_structure.json",
                    tags=["structure", "programme", level_name.lower()]
                )

                documents.append(Document(
                    page_content=module_content.strip(),
                    metadata=metadata.to_dict()
                ))

        return documents
