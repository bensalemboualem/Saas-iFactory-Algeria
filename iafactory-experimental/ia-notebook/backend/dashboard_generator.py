"""
Dashboard Generator Service for IA Notebook Pro
Generates interactive dashboards from data files (CSV, XLS, XLSX, JSON)
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ChartConfig:
    """Configuration for a dashboard chart"""
    id: str
    title: str
    chart_type: str  # 'bar', 'line', 'pie', 'scatter', 'area', 'table', 'kpi'
    data_column: str
    group_by: Optional[str] = None
    aggregation: str = "sum"  # sum, avg, count, min, max
    color_scheme: str = "iafactory"
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardConfig:
    """Dashboard configuration"""
    id: str
    title: str
    description: str
    charts: List[ChartConfig]
    filters: List[Dict[str, Any]]
    layout: str = "grid"  # grid, rows, columns
    refresh_interval: int = 0  # seconds, 0 = no auto-refresh
    theme: str = "dark"


class DashboardGenerator:
    """
    Generates interactive dashboards from data files
    Supports: CSV, XLS, XLSX, JSON, and data extracted from PDFs
    """

    # IAFactory color schemes
    COLOR_SCHEMES = {
        "iafactory": ["#00A651", "#00843D", "#006B32", "#E31B23", "#ffffff"],
        "algeria": ["#00A651", "#E31B23", "#ffffff", "#1a365d", "#2d3748"],
        "ocean": ["#0077b6", "#00b4d8", "#90e0ef", "#caf0f8", "#03045e"],
        "sunset": ["#f72585", "#b5179e", "#7209b7", "#560bad", "#480ca8"],
        "forest": ["#2d6a4f", "#40916c", "#52b788", "#74c69d", "#95d5b2"],
    }

    def __init__(self, output_dir: str = "./dashboards"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    async def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from various file formats

        Args:
            file_path: Path to the data file

        Returns:
            pandas DataFrame with the data
        """
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext == '.csv':
                # Try different encodings
                for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
                    try:
                        return pd.read_csv(file_path, encoding=encoding)
                    except UnicodeDecodeError:
                        continue
                raise ValueError(f"Could not decode CSV file: {file_path}")

            elif ext in ['.xls', '.xlsx']:
                return pd.read_excel(file_path)

            elif ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Handle different JSON structures
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    if 'data' in data:
                        return pd.DataFrame(data['data'])
                    return pd.DataFrame([data])

            elif ext == '.ods':
                return pd.read_excel(file_path, engine='odf')

            elif ext == '.parquet':
                return pd.read_parquet(file_path)

            else:
                raise ValueError(f"Unsupported file format: {ext}")

        except Exception as e:
            logger.error(f"Failed to load data from {file_path}: {e}")
            raise

    def analyze_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze DataFrame to suggest dashboard configuration

        Args:
            df: pandas DataFrame

        Returns:
            Analysis result with column info and chart suggestions
        """
        analysis = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": [],
            "suggested_charts": [],
            "date_columns": [],
            "numeric_columns": [],
            "categorical_columns": [],
            "kpis": []
        }

        for col in df.columns:
            col_info = {
                "name": col,
                "dtype": str(df[col].dtype),
                "null_count": int(df[col].isnull().sum()),
                "unique_count": int(df[col].nunique())
            }

            # Detect column type
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info["type"] = "numeric"
                col_info["min"] = float(df[col].min()) if not df[col].isnull().all() else None
                col_info["max"] = float(df[col].max()) if not df[col].isnull().all() else None
                col_info["mean"] = float(df[col].mean()) if not df[col].isnull().all() else None
                col_info["sum"] = float(df[col].sum()) if not df[col].isnull().all() else None
                analysis["numeric_columns"].append(col)

                # Suggest KPI
                analysis["kpis"].append({
                    "title": f"Total {col}",
                    "column": col,
                    "aggregation": "sum",
                    "format": "number"
                })

            elif pd.api.types.is_datetime64_any_dtype(df[col]) or self._is_date_column(df[col]):
                col_info["type"] = "date"
                analysis["date_columns"].append(col)

            else:
                col_info["type"] = "categorical"
                if col_info["unique_count"] < 20:
                    col_info["top_values"] = df[col].value_counts().head(10).to_dict()
                analysis["categorical_columns"].append(col)

            analysis["columns"].append(col_info)

        # Generate chart suggestions
        analysis["suggested_charts"] = self._suggest_charts(analysis)

        return analysis

    def _is_date_column(self, series: pd.Series) -> bool:
        """Check if a series contains date-like values"""
        try:
            if series.dtype == object:
                pd.to_datetime(series.dropna().head(100))
                return True
        except:
            pass
        return False

    def _suggest_charts(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest charts based on data analysis"""
        suggestions = []

        # Time series charts
        if analysis["date_columns"] and analysis["numeric_columns"]:
            for num_col in analysis["numeric_columns"][:3]:
                suggestions.append({
                    "type": "line",
                    "title": f"{num_col} over time",
                    "x_axis": analysis["date_columns"][0],
                    "y_axis": num_col,
                    "reason": "Time series data detected"
                })

        # Categorical bar charts
        if analysis["categorical_columns"] and analysis["numeric_columns"]:
            for cat_col in analysis["categorical_columns"][:2]:
                for num_col in analysis["numeric_columns"][:2]:
                    suggestions.append({
                        "type": "bar",
                        "title": f"{num_col} by {cat_col}",
                        "x_axis": cat_col,
                        "y_axis": num_col,
                        "aggregation": "sum",
                        "reason": "Categorical grouping available"
                    })

        # Pie charts for low cardinality categorical
        for cat_col in analysis["categorical_columns"]:
            col_info = next((c for c in analysis["columns"] if c["name"] == cat_col), None)
            if col_info and col_info["unique_count"] <= 8:
                suggestions.append({
                    "type": "pie",
                    "title": f"Distribution by {cat_col}",
                    "category": cat_col,
                    "reason": "Low cardinality categorical column"
                })

        # Scatter plots for numeric pairs
        if len(analysis["numeric_columns"]) >= 2:
            suggestions.append({
                "type": "scatter",
                "title": f"{analysis['numeric_columns'][0]} vs {analysis['numeric_columns'][1]}",
                "x_axis": analysis["numeric_columns"][0],
                "y_axis": analysis["numeric_columns"][1],
                "reason": "Multiple numeric columns available"
            })

        return suggestions[:10]  # Return top 10 suggestions

    async def generate_dashboard(
        self,
        file_path: str,
        title: str = None,
        language: str = "fr",
        auto_config: bool = True,
        custom_config: Optional[DashboardConfig] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete dashboard from a data file

        Args:
            file_path: Path to the data file
            title: Dashboard title
            language: Language for labels (fr, en, ar)
            auto_config: Auto-configure charts based on data
            custom_config: Custom dashboard configuration

        Returns:
            Dashboard data with charts and configuration
        """
        # Load data
        df = await self.load_data(file_path)

        # Analyze data
        analysis = self.analyze_data(df)

        # Use custom config or auto-generate
        if custom_config:
            config = custom_config
        elif auto_config:
            config = self._auto_configure_dashboard(analysis, title or os.path.basename(file_path))
        else:
            raise ValueError("Either auto_config or custom_config must be provided")

        # Generate chart data
        charts_data = []
        for chart_config in config.charts:
            chart_data = self._generate_chart_data(df, chart_config, analysis)
            charts_data.append(chart_data)

        # Generate KPIs
        kpis_data = self._generate_kpis(df, analysis)

        # Build dashboard response
        dashboard = {
            "id": config.id,
            "title": config.title,
            "description": config.description,
            "created_at": datetime.now().isoformat(),
            "language": language,
            "theme": config.theme,
            "layout": config.layout,
            "data_summary": {
                "rows": analysis["row_count"],
                "columns": analysis["column_count"],
                "source_file": os.path.basename(file_path)
            },
            "kpis": kpis_data,
            "charts": charts_data,
            "filters": self._generate_filters(df, analysis),
            "raw_analysis": analysis
        }

        # Save dashboard config
        dashboard_path = os.path.join(self.output_dir, f"{config.id}.json")
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            json.dump(dashboard, f, ensure_ascii=False, indent=2, default=str)

        return dashboard

    def _auto_configure_dashboard(self, analysis: Dict[str, Any], title: str) -> DashboardConfig:
        """Auto-generate dashboard configuration based on data analysis"""
        import uuid

        dashboard_id = str(uuid.uuid4())[:8]
        charts = []

        # Add suggested charts
        for i, suggestion in enumerate(analysis["suggested_charts"][:6]):
            chart = ChartConfig(
                id=f"chart_{i}",
                title=suggestion["title"],
                chart_type=suggestion["type"],
                data_column=suggestion.get("y_axis", suggestion.get("category", "")),
                group_by=suggestion.get("x_axis"),
                aggregation=suggestion.get("aggregation", "sum")
            )
            charts.append(chart)

        # Add a data table
        charts.append(ChartConfig(
            id="data_table",
            title="Data Table",
            chart_type="table",
            data_column="*",
            options={"page_size": 20}
        ))

        return DashboardConfig(
            id=dashboard_id,
            title=title,
            description=f"Auto-generated dashboard from {title}",
            charts=charts,
            filters=[],
            layout="grid"
        )

    def _generate_chart_data(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate data for a specific chart"""

        chart_data = {
            "id": config.id,
            "title": config.title,
            "type": config.chart_type,
            "color_scheme": self.COLOR_SCHEMES.get(config.color_scheme, self.COLOR_SCHEMES["iafactory"])
        }

        try:
            if config.chart_type == "table":
                # Return sample data for table
                chart_data["data"] = df.head(100).to_dict(orient='records')
                chart_data["columns"] = list(df.columns)

            elif config.chart_type == "pie":
                if config.group_by:
                    grouped = df.groupby(config.group_by)[config.data_column].agg(config.aggregation)
                else:
                    grouped = df[config.data_column].value_counts()

                chart_data["data"] = {
                    "labels": list(grouped.index.astype(str)),
                    "values": list(grouped.values)
                }

            elif config.chart_type in ["bar", "line", "area"]:
                if config.group_by:
                    grouped = df.groupby(config.group_by)[config.data_column].agg(config.aggregation)
                    chart_data["data"] = {
                        "labels": list(grouped.index.astype(str)),
                        "datasets": [{
                            "label": config.data_column,
                            "data": list(grouped.values)
                        }]
                    }
                else:
                    chart_data["data"] = {
                        "labels": list(range(len(df))),
                        "datasets": [{
                            "label": config.data_column,
                            "data": list(df[config.data_column].values)
                        }]
                    }

            elif config.chart_type == "scatter":
                x_col = config.group_by or analysis["numeric_columns"][0]
                y_col = config.data_column

                chart_data["data"] = {
                    "datasets": [{
                        "label": f"{x_col} vs {y_col}",
                        "data": [
                            {"x": float(row[x_col]), "y": float(row[y_col])}
                            for _, row in df.dropna(subset=[x_col, y_col]).head(1000).iterrows()
                        ]
                    }]
                }

            elif config.chart_type == "kpi":
                value = df[config.data_column].agg(config.aggregation)
                chart_data["data"] = {
                    "value": float(value),
                    "label": config.title,
                    "format": config.options.get("format", "number")
                }

        except Exception as e:
            logger.error(f"Failed to generate chart data for {config.id}: {e}")
            chart_data["error"] = str(e)

        return chart_data

    def _generate_kpis(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate KPI cards from data"""
        kpis = []

        # Total rows
        kpis.append({
            "id": "total_rows",
            "title": "Total Records",
            "value": analysis["row_count"],
            "format": "number",
            "icon": "table"
        })

        # Numeric column sums
        for col in analysis["numeric_columns"][:4]:
            try:
                total = float(df[col].sum())
                avg = float(df[col].mean())
                kpis.append({
                    "id": f"kpi_{col}",
                    "title": f"Total {col}",
                    "value": total,
                    "secondary_value": avg,
                    "secondary_label": "Average",
                    "format": "currency" if "price" in col.lower() or "montant" in col.lower() else "number",
                    "icon": "chart-line"
                })
            except:
                pass

        return kpis[:6]  # Return max 6 KPIs

    def _generate_filters(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate filter configurations for the dashboard"""
        filters = []

        # Date range filter
        for date_col in analysis["date_columns"][:1]:
            filters.append({
                "id": f"filter_{date_col}",
                "type": "date_range",
                "column": date_col,
                "label": f"Filter by {date_col}"
            })

        # Categorical filters
        for cat_col in analysis["categorical_columns"][:3]:
            col_info = next((c for c in analysis["columns"] if c["name"] == cat_col), None)
            if col_info and col_info["unique_count"] <= 20:
                filters.append({
                    "id": f"filter_{cat_col}",
                    "type": "select",
                    "column": cat_col,
                    "label": f"Filter by {cat_col}",
                    "options": list(df[cat_col].dropna().unique())[:20]
                })

        return filters


# Singleton instance
dashboard_generator = DashboardGenerator()
