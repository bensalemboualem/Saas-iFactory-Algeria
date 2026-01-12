"""
PDF Export Service for BBC School Reports
Generates professional PDF reports for Minister presentations
"""

import io
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from .advanced_features import (
    BBC_PROGRAM_DATA,
    BudgetCalculator,
    TimelineGenerator
)


@dataclass
class ReportConfig:
    """Configuration for PDF report"""
    title: str = "Programme National IA - BBC School Algérie"
    subtitle: str = "Rapport de Présentation Ministérielle"
    author: str = "IAFactory Academy"
    logo_url: Optional[str] = None
    include_budget: bool = True
    include_timeline: bool = True
    include_kpis: bool = True
    include_modules: bool = True
    language: str = "fr"


class PDFExportService:
    """Generate PDF reports for BBC School program"""

    @classmethod
    def generate_report_content(cls, config: ReportConfig = None) -> Dict[str, Any]:
        """
        Generate report content (structured data for PDF generation)

        This returns a structured document that can be rendered as PDF
        by a frontend PDF library (jsPDF, react-pdf, etc.)
        """
        config = config or ReportConfig()

        report = {
            "metadata": {
                "title": config.title,
                "subtitle": config.subtitle,
                "author": config.author,
                "generated_at": datetime.now().isoformat(),
                "language": config.language
            },
            "sections": []
        }

        # Section 1: Executive Summary
        report["sections"].append({
            "title": "Résumé Exécutif",
            "type": "summary",
            "content": {
                "program_name": BBC_PROGRAM_DATA["program_name"],
                "launch_date": BBC_PROGRAM_DATA["launch_date"],
                "pilot_duration": f"{BBC_PROGRAM_DATA['pilot_duration_months']} mois",
                "key_figures": [
                    {"label": "Établissements pilotes", "value": BBC_PROGRAM_DATA["total_schools"]},
                    {"label": "Enseignants à former", "value": BBC_PROGRAM_DATA["total_teachers"]},
                    {"label": "Élèves ciblés", "value": BBC_PROGRAM_DATA["total_students_target"]},
                    {"label": "Budget total", "value": f"{BBC_PROGRAM_DATA['budget']['total_da']:,} DA"}
                ]
            }
        })

        # Section 2: Budget
        if config.include_budget:
            budget = BudgetCalculator.calculate()
            report["sections"].append({
                "title": "Budget et Financement",
                "type": "budget",
                "content": {
                    "total_da": budget["total"]["formatted_da"],
                    "total_usd": budget["total"]["formatted_usd"],
                    "breakdown": [
                        {
                            "category": cat.replace("_", " ").title(),
                            "amount_da": f"{data['da']:,} DA",
                            "percent": f"{data['percent']}%"
                        }
                        for cat, data in budget["breakdown"].items()
                    ],
                    "costs_per_unit": {
                        "per_school": f"{budget['costs_per_unit']['per_school_da']:,} DA",
                        "per_teacher": f"{budget['costs_per_unit']['per_teacher_da']:,} DA",
                        "per_student": f"{budget['costs_per_unit']['per_student_da']:,} DA"
                    }
                }
            })

        # Section 3: Timeline
        if config.include_timeline:
            timeline = TimelineGenerator.to_json()
            report["sections"].append({
                "title": "Calendrier de Déploiement",
                "type": "timeline",
                "content": {
                    "start_date": timeline["start_date"],
                    "end_date": timeline["end_date"],
                    "duration_months": timeline["duration_months"],
                    "events": timeline["events"],
                    "mermaid": TimelineGenerator.to_mermaid()
                }
            })

        # Section 4: KPIs
        if config.include_kpis:
            report["sections"].append({
                "title": "Indicateurs de Performance",
                "type": "kpis",
                "content": {
                    "kpis": [
                        {
                            "name": kpi.replace("_", " ").title(),
                            "target": data["target"],
                            "unit": data["unit"]
                        }
                        for kpi, data in BBC_PROGRAM_DATA["kpis"].items()
                    ]
                }
            })

        # Section 5: Education Levels & Modules
        if config.include_modules:
            levels_content = []
            for level_key, level_data in BBC_PROGRAM_DATA["levels"].items():
                level_info = {
                    "id": level_key,
                    "name": level_data["name_fr"],
                    "name_ar": level_data.get("name_ar", ""),
                    "modules_count": level_data["modules"],
                    "total_hours": level_data["total_hours"]
                }
                if "age_range" in level_data:
                    level_info["age_range"] = level_data["age_range"]

                levels_content.append(level_info)

            # Add module details for Lycée
            modules_detail = []
            for module_id in BBC_PROGRAM_DATA["levels"]["lycee"]["modules_list"]:
                module = BBC_PROGRAM_DATA["modules"].get(module_id, {})
                modules_detail.append({
                    "id": module_id,
                    "name": module.get("name", ""),
                    "hours": module.get("duration_hours", 0),
                    "credits": module.get("credits", 0),
                    "difficulty": module.get("difficulty", "")
                })

            report["sections"].append({
                "title": "Niveaux et Modules",
                "type": "modules",
                "content": {
                    "levels": levels_content,
                    "lycee_modules": modules_detail
                }
            })

        # Section 6: Contact & Next Steps
        report["sections"].append({
            "title": "Prochaines Étapes",
            "type": "next_steps",
            "content": {
                "steps": [
                    "Validation ministérielle du programme",
                    "Sélection des 50 établissements pilotes",
                    "Recrutement et formation des formateurs",
                    "Déploiement de l'infrastructure technique",
                    "Lancement officiel le 3 Février 2026"
                ],
                "contact": {
                    "organization": "IAFactory Academy",
                    "email": "contact@iafactory.ch",
                    "website": "https://iafactory.ch"
                }
            }
        })

        return report

    @classmethod
    def to_markdown(cls, config: ReportConfig = None) -> str:
        """Generate report as Markdown (can be converted to PDF)"""
        report = cls.generate_report_content(config)

        md = f"""# {report['metadata']['title']}
## {report['metadata']['subtitle']}

**Généré le:** {datetime.now().strftime('%d/%m/%Y à %H:%M')}
**Auteur:** {report['metadata']['author']}

---

"""
        for section in report["sections"]:
            md += f"## {section['title']}\n\n"

            if section["type"] == "summary":
                content = section["content"]
                md += f"**Programme:** {content['program_name']}\n\n"
                md += f"**Date de lancement:** {content['launch_date']}\n\n"
                md += f"**Durée pilote:** {content['pilot_duration']}\n\n"
                md += "### Chiffres clés\n\n"
                md += "| Indicateur | Valeur |\n|------------|--------|\n"
                for fig in content["key_figures"]:
                    md += f"| {fig['label']} | {fig['value']} |\n"

            elif section["type"] == "budget":
                content = section["content"]
                md += f"**Total:** {content['total_da']} ({content['total_usd']})\n\n"
                md += "### Répartition\n\n"
                md += "| Poste | Montant | % |\n|-------|---------|---|\n"
                for item in content["breakdown"]:
                    md += f"| {item['category']} | {item['amount_da']} | {item['percent']} |\n"

            elif section["type"] == "timeline":
                content = section["content"]
                md += f"**Période:** {content['start_date']} → {content['end_date']} ({content['duration_months']} mois)\n\n"
                md += "### Jalons\n\n"
                md += "| Date | Événement | Phase |\n|------|-----------|-------|\n"
                for event in content["events"]:
                    md += f"| {event['date']} | {event['title']} | {event['phase']} |\n"

            elif section["type"] == "kpis":
                content = section["content"]
                md += "| KPI | Objectif | Unité |\n|-----|----------|-------|\n"
                for kpi in content["kpis"]:
                    md += f"| {kpi['name']} | {kpi['target']} | {kpi['unit']} |\n"

            elif section["type"] == "modules":
                content = section["content"]
                md += "### Niveaux d'enseignement\n\n"
                md += "| Niveau | Modules | Heures |\n|--------|---------|--------|\n"
                for level in content["levels"]:
                    md += f"| {level['name']} | {level['modules_count']} | {level['total_hours']}h |\n"

                md += "\n### Modules Lycée (détail)\n\n"
                md += "| ID | Module | Heures | Crédits | Difficulté |\n"
                md += "|----|--------|--------|---------|------------|\n"
                for mod in content["lycee_modules"]:
                    md += f"| {mod['id']} | {mod['name']} | {mod['hours']}h | {mod['credits']} | {mod['difficulty']} |\n"

            elif section["type"] == "next_steps":
                content = section["content"]
                md += "### Actions à venir\n\n"
                for i, step in enumerate(content["steps"], 1):
                    md += f"{i}. {step}\n"
                md += f"\n### Contact\n\n"
                md += f"- **Organisation:** {content['contact']['organization']}\n"
                md += f"- **Email:** {content['contact']['email']}\n"
                md += f"- **Site:** {content['contact']['website']}\n"

            md += "\n---\n\n"

        md += """
---
*Ce rapport a été généré automatiquement par le système RAG IAFactory Academy.*

© 2024-2026 IAFactory Academy. Tous droits réservés.
"""
        return md

    @classmethod
    def to_html(cls, config: ReportConfig = None) -> str:
        """Generate report as HTML (ready for PDF conversion)"""
        report = cls.generate_report_content(config)

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report['metadata']['title']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            color: #333;
        }}
        h1 {{
            color: #1a5f7a;
            border-bottom: 3px solid #1a5f7a;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2d8bba;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #1a5f7a;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .key-figure {{
            display: inline-block;
            background: linear-gradient(135deg, #1a5f7a, #2d8bba);
            color: white;
            padding: 20px;
            margin: 10px;
            border-radius: 10px;
            text-align: center;
            min-width: 150px;
        }}
        .key-figure .value {{
            font-size: 2em;
            font-weight: bold;
        }}
        .key-figure .label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>{report['metadata']['title']}</h1>
    <h2 style="color: #666; font-weight: normal;">{report['metadata']['subtitle']}</h2>
    <p><strong>Généré le:</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
"""

        for section in report["sections"]:
            html += f"<h2>{section['title']}</h2>\n"

            if section["type"] == "summary":
                content = section["content"]
                html += f"<p><strong>Programme:</strong> {content['program_name']}</p>\n"
                html += "<div style='display: flex; flex-wrap: wrap; justify-content: center;'>\n"
                for fig in content["key_figures"]:
                    html += f"""<div class="key-figure">
                        <div class="value">{fig['value']}</div>
                        <div class="label">{fig['label']}</div>
                    </div>\n"""
                html += "</div>\n"

            elif section["type"] == "budget":
                content = section["content"]
                html += f"<p><strong>Budget total:</strong> {content['total_da']} ({content['total_usd']})</p>\n"
                html += "<table><tr><th>Poste</th><th>Montant</th><th>%</th></tr>\n"
                for item in content["breakdown"]:
                    html += f"<tr><td>{item['category']}</td><td>{item['amount_da']}</td><td>{item['percent']}</td></tr>\n"
                html += "</table>\n"

            elif section["type"] == "kpis":
                content = section["content"]
                html += "<table><tr><th>KPI</th><th>Objectif</th><th>Unité</th></tr>\n"
                for kpi in content["kpis"]:
                    html += f"<tr><td>{kpi['name']}</td><td>{kpi['target']}</td><td>{kpi['unit']}</td></tr>\n"
                html += "</table>\n"

            elif section["type"] == "modules":
                content = section["content"]
                html += "<h3>Niveaux d'enseignement</h3>\n"
                html += "<table><tr><th>Niveau</th><th>Modules</th><th>Heures</th></tr>\n"
                for level in content["levels"]:
                    html += f"<tr><td>{level['name']}</td><td>{level['modules_count']}</td><td>{level['total_hours']}h</td></tr>\n"
                html += "</table>\n"

            elif section["type"] == "next_steps":
                content = section["content"]
                html += "<ol>\n"
                for step in content["steps"]:
                    html += f"<li>{step}</li>\n"
                html += "</ol>\n"

        html += """
    <div class="footer">
        <p>© 2024-2026 IAFactory Academy. Tous droits réservés.</p>
        <p>Généré par le système RAG IAFactory Academy</p>
    </div>
</body>
</html>
"""
        return html
