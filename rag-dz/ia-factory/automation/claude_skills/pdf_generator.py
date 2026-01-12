"""
IA Factory - Claude Skill: PDF Generator
Génération de documents PDF professionnels
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import os

router = APIRouter(prefix="/skills/pdf", tags=["Claude Skills - PDF"])


class PDFType(str, Enum):
    REPORT = "report"               # Rapport
    INVOICE = "invoice"             # Facture
    CERTIFICATE = "certificate"     # Certificat
    BROCHURE = "brochure"           # Brochure
    EBOOK = "ebook"                 # E-book
    WHITEPAPER = "whitepaper"       # Livre blanc
    FLYER = "flyer"                 # Flyer
    CV = "cv"                       # CV
    LETTER = "letter"               # Lettre


class PageSize(str, Enum):
    A4 = "A4"
    LETTER = "letter"
    A3 = "A3"
    A5 = "A5"


class PageOrientation(str, Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class ContentBlock(BaseModel):
    """Bloc de contenu"""
    type: str  # text, heading, image, table, list, quote, code
    content: Any
    style: Dict[str, Any] = Field(default_factory=dict)


class PDFRequest(BaseModel):
    """Requête de génération de PDF"""
    pdf_type: PDFType
    title: str
    subtitle: Optional[str] = None
    author: str = "IA Factory"
    content_blocks: List[ContentBlock] = Field(default_factory=list)
    page_size: PageSize = PageSize.A4
    orientation: PageOrientation = PageOrientation.PORTRAIT
    include_header: bool = True
    include_footer: bool = True
    include_page_numbers: bool = True
    language: str = "fr"


class GeneratedPDF(BaseModel):
    """PDF généré"""
    id: str
    filename: str
    filepath: str
    pdf_type: PDFType
    page_count: int
    created_at: datetime
    size_bytes: int
    download_url: str


class PdfGenerator:
    """
    Générateur de documents PDF
    Utilise ReportLab ou WeasyPrint pour créer des PDFs professionnels
    """
    
    # Styles par défaut
    STYLES = {
        "title": {
            "font_size": 28,
            "font_name": "Helvetica-Bold",
            "color": "#1F4E79",
            "alignment": "center",
            "space_after": 20
        },
        "subtitle": {
            "font_size": 16,
            "font_name": "Helvetica",
            "color": "#666666",
            "alignment": "center",
            "space_after": 30
        },
        "heading1": {
            "font_size": 20,
            "font_name": "Helvetica-Bold",
            "color": "#1F4E79",
            "space_before": 20,
            "space_after": 12
        },
        "heading2": {
            "font_size": 16,
            "font_name": "Helvetica-Bold",
            "color": "#2E75B6",
            "space_before": 15,
            "space_after": 10
        },
        "body": {
            "font_size": 11,
            "font_name": "Helvetica",
            "color": "#333333",
            "line_height": 1.5
        },
        "quote": {
            "font_size": 12,
            "font_name": "Helvetica-Oblique",
            "color": "#555555",
            "left_indent": 40,
            "border_left": "#2E75B6"
        }
    }
    
    # Templates HTML pour WeasyPrint
    HTML_TEMPLATES = {
        PDFType.REPORT: """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: {page_size};
            margin: 2cm;
            @top-right {{
                content: "{company}";
                font-size: 10pt;
                color: #666;
            }}
            @bottom-center {{
                content: "Page " counter(page) " / " counter(pages);
                font-size: 10pt;
            }}
        }}
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #1F4E79;
            font-size: 28pt;
            text-align: center;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #2E75B6;
            font-size: 18pt;
            margin-top: 30px;
            border-bottom: 2px solid #2E75B6;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #1F4E79;
            font-size: 14pt;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            font-size: 14pt;
            margin-bottom: 40px;
        }}
        .meta {{
            text-align: center;
            color: #888;
            margin-bottom: 50px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #1F4E79;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 10px;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        blockquote {{
            border-left: 4px solid #2E75B6;
            padding-left: 20px;
            margin-left: 0;
            font-style: italic;
            color: #555;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }}
        pre {{
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {subtitle_html}
    <div class="meta">
        <p>Préparé par: {author}</p>
        <p>Date: {date}</p>
    </div>
    {content}
</body>
</html>
""",
        
        PDFType.INVOICE: """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 1.5cm;
        }}
        body {{
            font-family: 'Helvetica', sans-serif;
            font-size: 10pt;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 40px;
        }}
        .company {{
            font-size: 24pt;
            font-weight: bold;
            color: #1F4E79;
        }}
        .invoice-title {{
            font-size: 28pt;
            color: #1F4E79;
            text-align: right;
        }}
        .invoice-number {{
            text-align: right;
            color: #666;
        }}
        .addresses {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 40px;
        }}
        .address-block {{
            width: 45%;
        }}
        .address-label {{
            font-weight: bold;
            color: #1F4E79;
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
        }}
        th {{
            background-color: #1F4E79;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            border-bottom: 1px solid #ddd;
            padding: 12px;
        }}
        .totals {{
            text-align: right;
            margin-top: 30px;
        }}
        .total-row {{
            font-size: 12pt;
            margin: 5px 0;
        }}
        .grand-total {{
            font-size: 16pt;
            font-weight: bold;
            color: #1F4E79;
            border-top: 2px solid #1F4E79;
            padding-top: 10px;
        }}
        .footer {{
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 9pt;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="company">{company}</div>
        <div>
            <div class="invoice-title">FACTURE</div>
            <div class="invoice-number">N° {invoice_number}</div>
            <div class="invoice-number">Date: {date}</div>
        </div>
    </div>
    {content}
    <div class="footer">
        {company} | contact@iafactory.ch | www.iafactory.ch
    </div>
</body>
</html>
""",
        
        PDFType.CERTIFICATE: """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4 landscape;
            margin: 0;
        }}
        body {{
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .certificate {{
            background: white;
            width: 90%;
            height: 85%;
            border: 3px solid #1F4E79;
            padding: 40px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .border-inner {{
            border: 1px solid #2E75B6;
            height: 100%;
            padding: 30px;
        }}
        .title {{
            font-size: 48pt;
            color: #1F4E79;
            margin-bottom: 20px;
        }}
        .subtitle {{
            font-size: 16pt;
            color: #666;
            margin-bottom: 40px;
        }}
        .recipient {{
            font-size: 32pt;
            color: #333;
            margin: 30px 0;
            border-bottom: 2px solid #1F4E79;
            display: inline-block;
            padding: 0 30px 10px;
        }}
        .description {{
            font-size: 14pt;
            color: #555;
            margin: 30px 50px;
            line-height: 1.8;
        }}
        .date {{
            font-size: 12pt;
            color: #888;
            margin-top: 40px;
        }}
        .signature {{
            margin-top: 50px;
            display: flex;
            justify-content: space-around;
        }}
        .sig-block {{
            text-align: center;
        }}
        .sig-line {{
            width: 200px;
            border-top: 1px solid #333;
            margin-top: 60px;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="certificate">
        <div class="border-inner">
            <div class="title">CERTIFICAT</div>
            <div class="subtitle">{subtitle}</div>
            <p>Ce certificat est décerné à</p>
            <div class="recipient">{recipient}</div>
            <div class="description">{description}</div>
            <div class="date">Délivré le {date}</div>
            <div class="signature">
                <div class="sig-block">
                    <div class="sig-line">{author}</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    }
    
    def __init__(self):
        self.output_dir = "outputs/pdfs"
        os.makedirs(self.output_dir, exist_ok=True)
        self.generated_files: Dict[str, GeneratedPDF] = {}
    
    async def generate(self, request: PDFRequest) -> GeneratedPDF:
        """Génère un document PDF"""
        
        # Essayer WeasyPrint d'abord (meilleur rendu)
        try:
            return await self._generate_weasyprint(request)
        except ImportError:
            pass
        
        # Fallback sur ReportLab
        try:
            return await self._generate_reportlab(request)
        except ImportError:
            raise HTTPException(
                status_code=500,
                detail="Aucun générateur PDF disponible. Installez weasyprint ou reportlab."
            )
    
    async def _generate_weasyprint(self, request: PDFRequest) -> GeneratedPDF:
        """Génère un PDF avec WeasyPrint"""
        from weasyprint import HTML, CSS
        
        # Construire le HTML
        template = self.HTML_TEMPLATES.get(request.pdf_type, self.HTML_TEMPLATES[PDFType.REPORT])
        
        content_html = self._build_content_html(request.content_blocks)
        
        html_content = template.format(
            title=request.title,
            subtitle_html=f'<div class="subtitle">{request.subtitle}</div>' if request.subtitle else "",
            author=request.author,
            company="IA Factory",
            date=datetime.now().strftime("%d %B %Y"),
            content=content_html,
            page_size=request.page_size.value,
            invoice_number=datetime.now().strftime("%Y%m%d%H%M"),
            recipient=request.title,
            description="",
            subtitle=request.subtitle or ""
        )
        
        # Générer le PDF
        html = HTML(string=html_content)
        
        file_id = f"pdf_{datetime.now().strftime('%Y%m%d%H%M%S')}_{request.pdf_type.value}"
        filename = f"{file_id}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        html.write_pdf(filepath)
        
        # Infos fichier
        file_size = os.path.getsize(filepath)
        
        # Compter les pages (approximatif)
        page_count = max(1, len(request.content_blocks) // 3)
        
        generated = GeneratedPDF(
            id=file_id,
            filename=filename,
            filepath=filepath,
            pdf_type=request.pdf_type,
            page_count=page_count,
            created_at=datetime.now(),
            size_bytes=file_size,
            download_url=f"/skills/pdf/download/{file_id}"
        )
        
        self.generated_files[file_id] = generated
        
        return generated
    
    async def _generate_reportlab(self, request: PDFRequest) -> GeneratedPDF:
        """Génère un PDF avec ReportLab"""
        from reportlab.lib.pagesizes import A4, letter, A3, A5
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch, cm
        from reportlab.lib import colors
        
        # Taille de page
        page_sizes = {
            PageSize.A4: A4,
            PageSize.LETTER: letter,
            PageSize.A3: A3,
            PageSize.A5: A5
        }
        page_size = page_sizes.get(request.page_size, A4)
        
        if request.orientation == PageOrientation.LANDSCAPE:
            page_size = (page_size[1], page_size[0])
        
        file_id = f"pdf_{datetime.now().strftime('%Y%m%d%H%M%S')}_{request.pdf_type.value}"
        filename = f"{file_id}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=page_size,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        styles = getSampleStyleSheet()
        
        # Styles personnalisés
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=28,
            textColor=colors.HexColor('#1F4E79'),
            spaceAfter=20,
            alignment=1  # Center
        )
        
        story = []
        
        # Titre
        story.append(Paragraph(request.title, title_style))
        story.append(Spacer(1, 12))
        
        # Sous-titre
        if request.subtitle:
            story.append(Paragraph(request.subtitle, styles['Heading2']))
            story.append(Spacer(1, 20))
        
        # Contenu
        for block in request.content_blocks:
            if block.type == "heading":
                story.append(Paragraph(str(block.content), styles['Heading1']))
            elif block.type == "text":
                story.append(Paragraph(str(block.content), styles['Normal']))
            elif block.type == "list":
                for item in block.content:
                    story.append(Paragraph(f"• {item}", styles['Normal']))
            
            story.append(Spacer(1, 12))
        
        doc.build(story)
        
        file_size = os.path.getsize(filepath)
        
        generated = GeneratedPDF(
            id=file_id,
            filename=filename,
            filepath=filepath,
            pdf_type=request.pdf_type,
            page_count=1,
            created_at=datetime.now(),
            size_bytes=file_size,
            download_url=f"/skills/pdf/download/{file_id}"
        )
        
        self.generated_files[file_id] = generated
        
        return generated
    
    def _build_content_html(self, blocks: List[ContentBlock]) -> str:
        """Construit le HTML à partir des blocs de contenu"""
        html_parts = []
        
        for block in blocks:
            if block.type == "heading":
                level = block.style.get("level", 2)
                html_parts.append(f"<h{level}>{block.content}</h{level}>")
            
            elif block.type == "text":
                html_parts.append(f"<p>{block.content}</p>")
            
            elif block.type == "list":
                items = "".join(f"<li>{item}</li>" for item in block.content)
                html_parts.append(f"<ul>{items}</ul>")
            
            elif block.type == "quote":
                html_parts.append(f"<blockquote>{block.content}</blockquote>")
            
            elif block.type == "code":
                html_parts.append(f"<pre><code>{block.content}</code></pre>")
            
            elif block.type == "table":
                table_html = self._build_table_html(block.content)
                html_parts.append(table_html)
        
        return "\n".join(html_parts)
    
    def _build_table_html(self, data: List[List[Any]]) -> str:
        """Construit le HTML d'un tableau"""
        if not data:
            return ""
        
        html = "<table>"
        
        # En-tête
        if data:
            html += "<thead><tr>"
            for cell in data[0]:
                html += f"<th>{cell}</th>"
            html += "</tr></thead>"
        
        # Corps
        html += "<tbody>"
        for row in data[1:]:
            html += "<tr>"
            for cell in row:
                html += f"<td>{cell}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        
        return html
    
    def list_files(self) -> List[GeneratedPDF]:
        """Liste tous les PDFs générés"""
        return list(self.generated_files.values())


# Instance globale
pdf_generator = PdfGenerator()


# Routes API

@router.post("/generate", response_model=Dict[str, Any])
async def generate_pdf(request: PDFRequest):
    """
    Génère un document PDF professionnel
    
    Types supportés:
    - report: Rapport
    - invoice: Facture
    - certificate: Certificat
    - brochure: Brochure
    - ebook: E-book
    """
    pdf = await pdf_generator.generate(request)
    return {
        "status": "success",
        "file_id": pdf.id,
        "filename": pdf.filename,
        "page_count": pdf.page_count,
        "size_kb": round(pdf.size_bytes / 1024, 2),
        "download_url": pdf.download_url
    }


@router.get("/files")
async def list_files():
    """Liste tous les PDFs générés"""
    return pdf_generator.list_files()


@router.get("/download/{file_id}")
async def download_file(file_id: str):
    """Télécharge un PDF généré"""
    from fastapi.responses import FileResponse
    
    pdf = pdf_generator.generated_files.get(file_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(
        path=pdf.filepath,
        filename=pdf.filename,
        media_type="application/pdf"
    )


@router.post("/certificate")
async def generate_certificate(
    recipient: str,
    title: str = "Certificat de Formation",
    description: str = "A complété avec succès la formation",
    author: str = "Boualem Chebaki"
):
    """
    Génère rapidement un certificat
    """
    request = PDFRequest(
        pdf_type=PDFType.CERTIFICATE,
        title=title,
        subtitle="IA Factory Academy",
        author=author,
        content_blocks=[
            ContentBlock(type="text", content=recipient),
            ContentBlock(type="text", content=description)
        ],
        orientation=PageOrientation.LANDSCAPE
    )
    
    return await generate_pdf(request)
