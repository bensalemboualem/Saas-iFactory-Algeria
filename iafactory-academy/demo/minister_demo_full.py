"""
BBC School IA - Mode Démo Ministre (Version Premium)
Interface Streamlit niveau Stripe/Vercel avec design professionnel
"""

import streamlit as st
import time
from datetime import datetime
import json
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ============================================
# TRANSLATOR CLASS
# ============================================
class Translator:
    def __init__(self, lang='fr'):
        self.lang = lang
        self.translations = self._load_translations()

    def _load_translations(self) -> dict:
        locale_path = os.path.join(os.path.dirname(__file__), 'locales', f'{self.lang}.json')
        try:
            with open(locale_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            fallback_path = os.path.join(os.path.dirname(__file__), 'locales', 'fr.json')
            try:
                with open(fallback_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}

    def t(self, key: str, default: str = None) -> str:
        keys = key.split('.')
        value = self.translations
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default if default else key

    def is_rtl(self) -> bool:
        return self.lang == 'ar'


# ============================================
# PREMIUM DESIGN SYSTEM - STRIPE/VERCEL LEVEL
# ============================================
def get_premium_css(theme: str, is_rtl: bool = False) -> str:
    """Generate premium CSS inspired by Stripe, Vercel, Linear"""

    # Professional color palette
    if theme == 'dark':
        # Dark theme - Zinc-based like Vercel
        bg_primary = '#09090B'       # Zinc-950
        bg_secondary = '#18181B'     # Zinc-900
        bg_tertiary = '#27272A'      # Zinc-800
        bg_elevated = '#1F1F23'      # Custom elevated
        bg_hover = '#2D2D33'         # Hover state

        text_primary = '#FAFAFA'     # Zinc-50
        text_secondary = '#A1A1AA'   # Zinc-400
        text_tertiary = '#71717A'    # Zinc-500

        accent_primary = '#60A5FA'   # Blue-400
        accent_hover = '#3B82F6'     # Blue-500
        accent_light = '#1E3A8A'     # Blue-900

        success = '#34D399'          # Emerald-400
        success_bg = '#064E3B'       # Emerald-900
        success_text = '#A7F3D0'     # Emerald-200

        warning = '#FBBF24'          # Amber-400
        warning_bg = '#78350F'       # Amber-900

        danger = '#F87171'           # Red-400
        danger_bg = '#7F1D1D'        # Red-900

        border_light = '#27272A'     # Zinc-800
        border_medium = '#3F3F46'    # Zinc-700

        shadow_color = 'rgba(0,0,0,0.5)'
        gradient_start = '#3B82F6'
        gradient_end = '#8B5CF6'

    else:
        # Light theme - Clean like Stripe
        bg_primary = '#FFFFFF'
        bg_secondary = '#FAFAFA'     # Zinc-50
        bg_tertiary = '#F4F4F5'      # Zinc-100
        bg_elevated = '#FFFFFF'
        bg_hover = '#F4F4F5'

        text_primary = '#18181B'     # Zinc-900
        text_secondary = '#52525B'   # Zinc-600
        text_tertiary = '#A1A1AA'    # Zinc-400

        accent_primary = '#3B82F6'   # Blue-500
        accent_hover = '#2563EB'     # Blue-600
        accent_light = '#DBEAFE'     # Blue-100

        success = '#10B981'          # Emerald-500
        success_bg = '#D1FAE5'       # Emerald-100
        success_text = '#065F46'     # Emerald-800

        warning = '#F59E0B'          # Amber-500
        warning_bg = '#FEF3C7'       # Amber-100

        danger = '#EF4444'           # Red-500
        danger_bg = '#FEE2E2'        # Red-100

        border_light = '#E4E4E7'     # Zinc-200
        border_medium = '#D4D4D8'    # Zinc-300

        shadow_color = 'rgba(0,0,0,0.08)'
        gradient_start = '#3B82F6'
        gradient_end = '#8B5CF6'

    # RTL support
    direction = 'rtl' if is_rtl else 'ltr'
    text_align = 'right' if is_rtl else 'left'
    border_side = 'right' if is_rtl else 'left'
    opposite_side = 'left' if is_rtl else 'right'
    margin_side = f'margin-{opposite_side}' if is_rtl else f'margin-{opposite_side}'

    return f"""
    <style>
        /* ============================================
           PREMIUM DESIGN SYSTEM - STRIPE/VERCEL LEVEL
           ============================================ */

        /* ===== CSS RESET & BASE ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        *, *::before, *::after {{
            box-sizing: border-box;
        }}

        /* ===== ROOT VARIABLES ===== */
        :root {{
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-mono: 'SF Mono', 'Fira Code', monospace;

            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
            --radius-full: 9999px;

            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* ===== GLOBAL APP STYLES ===== */
        .stApp {{
            background-color: {bg_primary} !important;
            font-family: var(--font-sans) !important;
            direction: {direction};
        }}

        .stApp > header {{
            background-color: transparent !important;
        }}

        /* Hide Streamlit branding */
        #MainMenu, footer, header[data-testid="stHeader"] {{
            visibility: hidden;
        }}

        /* ===== TYPOGRAPHY ===== */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-sans) !important;
            font-weight: 600 !important;
            color: {text_primary} !important;
            letter-spacing: -0.02em;
            direction: {direction};
            text-align: {text_align};
        }}

        h1 {{ font-size: 2rem !important; line-height: 1.2 !important; }}
        h2 {{ font-size: 1.5rem !important; line-height: 1.3 !important; }}
        h3 {{ font-size: 1.25rem !important; line-height: 1.4 !important; }}
        h4 {{ font-size: 1rem !important; line-height: 1.5 !important; }}

        p, span, div, li {{
            font-family: var(--font-sans) !important;
            color: {text_secondary};
            direction: {direction};
            text-align: {text_align};
        }}

        /* ===== SIDEBAR - PREMIUM STYLE ===== */
        section[data-testid="stSidebar"] {{
            background: {bg_secondary} !important;
            border-{opposite_side}: 1px solid {border_light} !important;
            direction: {direction};
        }}

        section[data-testid="stSidebar"] > div {{
            padding: 1.5rem 1rem !important;
        }}

        section[data-testid="stSidebar"] .stMarkdown h2 {{
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: {text_tertiary} !important;
            margin-bottom: 1rem !important;
        }}

        section[data-testid="stSidebar"] .stMarkdown h3 {{
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: {text_secondary} !important;
            margin: 1.5rem 0 0.75rem 0 !important;
        }}

        /* ===== METRICS - MODERN CARDS ===== */
        [data-testid="stMetric"] {{
            background: {bg_elevated} !important;
            border: 1px solid {border_light} !important;
            border-radius: var(--radius-lg) !important;
            padding: 1rem 1.25rem !important;
            transition: var(--transition-base) !important;
        }}

        [data-testid="stMetric"]:hover {{
            border-color: {border_medium} !important;
            box-shadow: 0 4px 12px {shadow_color} !important;
        }}

        [data-testid="stMetricLabel"] {{
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: {text_tertiary} !important;
        }}

        [data-testid="stMetricValue"] {{
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            color: {text_primary} !important;
            letter-spacing: -0.02em !important;
        }}

        [data-testid="stMetricDelta"] {{
            font-size: 0.75rem !important;
            font-weight: 500 !important;
        }}

        [data-testid="stMetricDelta"] svg {{
            display: none !important;
        }}

        /* ===== TABS - VERCEL STYLE ===== */
        .stTabs {{
            background: transparent !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            background: {bg_tertiary} !important;
            border-radius: var(--radius-lg) !important;
            padding: 4px !important;
            gap: 0 !important;
            border: 1px solid {border_light} !important;
            direction: {direction};
        }}

        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border-radius: var(--radius-md) !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: {text_secondary} !important;
            border: none !important;
            transition: var(--transition-fast) !important;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            color: {text_primary} !important;
            background: {bg_hover} !important;
        }}

        .stTabs [aria-selected="true"] {{
            background: {bg_elevated} !important;
            color: {text_primary} !important;
            box-shadow: 0 1px 3px {shadow_color} !important;
        }}

        .stTabs [data-baseweb="tab-highlight"] {{
            display: none !important;
        }}

        .stTabs [data-baseweb="tab-border"] {{
            display: none !important;
        }}

        /* ===== BUTTONS - STRIPE STYLE ===== */
        .stButton > button {{
            background: linear-gradient(180deg, {accent_primary} 0%, {accent_hover} 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.625rem 1rem !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            font-family: var(--font-sans) !important;
            transition: var(--transition-fast) !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.1) !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
        }}

        .stButton > button:active {{
            transform: translateY(0) !important;
        }}

        /* Secondary buttons */
        .stButton > button[kind="secondary"] {{
            background: {bg_elevated} !important;
            color: {text_primary} !important;
            border: 1px solid {border_medium} !important;
            box-shadow: 0 1px 2px {shadow_color} !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background: {bg_hover} !important;
            border-color: {border_medium} !important;
        }}

        /* ===== SELECT BOXES - MODERN ===== */
        .stSelectbox > div > div {{
            background: {bg_elevated} !important;
            border: 1px solid {border_light} !important;
            border-radius: var(--radius-md) !important;
            font-size: 0.875rem !important;
            transition: var(--transition-fast) !important;
        }}

        .stSelectbox > div > div:hover {{
            border-color: {border_medium} !important;
        }}

        .stSelectbox > div > div:focus-within {{
            border-color: {accent_primary} !important;
            box-shadow: 0 0 0 3px {accent_light} !important;
        }}

        /* ===== PREMIUM CARD COMPONENTS ===== */
        .premium-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-xl);
            padding: 1.5rem;
            transition: var(--transition-base);
        }}

        .premium-card:hover {{
            border-color: {border_medium};
            box-shadow: 0 8px 24px {shadow_color};
        }}

        /* ===== HERO HEADER ===== */
        .hero-header {{
            background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
            border-radius: var(--radius-xl);
            padding: 2rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }}

        .hero-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.5;
        }}

        .hero-header h2 {{
            color: white !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin: 0 !important;
            position: relative;
            text-align: center;
        }}

        .hero-header p {{
            color: rgba(255,255,255,0.8) !important;
            font-size: 0.875rem !important;
            margin: 0.5rem 0 0 0 !important;
            position: relative;
            text-align: center;
        }}

        /* ===== KPI CARDS - STRIPE DASHBOARD STYLE ===== */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}

        .kpi-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-xl);
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition: var(--transition-base);
        }}

        .kpi-card:hover {{
            border-color: {border_medium};
            box-shadow: 0 8px 24px {shadow_color};
            transform: translateY(-2px);
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
        }}

        .kpi-card.green::before {{ background: linear-gradient(90deg, #10B981, #34D399); }}
        .kpi-card.blue::before {{ background: linear-gradient(90deg, #3B82F6, #60A5FA); }}
        .kpi-card.orange::before {{ background: linear-gradient(90deg, #F59E0B, #FBBF24); }}
        .kpi-card.purple::before {{ background: linear-gradient(90deg, #8B5CF6, #A78BFA); }}

        .kpi-label {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {text_tertiary};
            margin-bottom: 0.5rem;
        }}

        .kpi-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {text_primary};
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}

        .kpi-value.green {{ color: {success}; }}
        .kpi-value.blue {{ color: {accent_primary}; }}
        .kpi-value.orange {{ color: {warning}; }}

        .kpi-desc {{
            font-size: 0.8125rem;
            color: {text_secondary};
            margin-top: 0.5rem;
            line-height: 1.4;
        }}

        /* ===== PHASE CARDS - TIMELINE STYLE ===== */
        .phase-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-lg);
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            border-{border_side}: 4px solid;
            transition: var(--transition-base);
        }}

        .phase-card:hover {{
            box-shadow: 0 4px 12px {shadow_color};
        }}

        .phase-card.phase-1 {{ border-{border_side}-color: {success}; }}
        .phase-card.phase-2 {{ border-{border_side}-color: {accent_primary}; }}
        .phase-card.phase-3 {{ border-{border_side}-color: {warning}; }}

        .phase-card h3 {{
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin: 0 0 0.5rem 0 !important;
        }}

        /* ===== TIMELINE - LINEAR STYLE ===== */
        .timeline-container {{
            position: relative;
            padding-{border_side}: 2rem;
        }}

        .timeline-container::before {{
            content: '';
            position: absolute;
            {border_side}: 0.75rem;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, {accent_primary}, {success});
            border-radius: 1px;
        }}

        .timeline-item {{
            position: relative;
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-lg);
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
            transition: var(--transition-base);
            direction: {direction};
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            {border_side}: -2rem;
            top: 1.25rem;
            width: 12px;
            height: 12px;
            background: {bg_primary};
            border: 2px solid {accent_primary};
            border-radius: 50%;
        }}

        .timeline-item:hover {{
            border-color: {border_medium};
            box-shadow: 0 4px 12px {shadow_color};
        }}

        .timeline-item.milestone::before {{
            background: {warning};
            border-color: {warning};
            width: 14px;
            height: 14px;
            {border_side}: calc(-2rem - 1px);
        }}

        .timeline-item.done::before {{
            background: {success};
            border-color: {success};
        }}

        .timeline-date {{
            font-size: 0.75rem;
            font-weight: 600;
            color: {accent_primary};
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .timeline-title {{
            font-size: 0.9375rem;
            font-weight: 500;
            color: {text_primary};
            margin: 0.25rem 0;
        }}

        .timeline-badge {{
            display: inline-block;
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.25rem 0.625rem;
            border-radius: var(--radius-full);
            background: {accent_light};
            color: {accent_primary};
        }}

        /* ===== TESTIMONIALS - NOTION STYLE ===== */
        .testimonial-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-xl);
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: var(--transition-base);
        }}

        .testimonial-card:hover {{
            border-color: {border_medium};
            box-shadow: 0 8px 24px {shadow_color};
        }}

        .testimonial-icon {{
            font-size: 2rem;
            margin-bottom: 1rem;
        }}

        .testimonial-quote {{
            font-size: 1rem;
            font-style: italic;
            color: {text_primary};
            line-height: 1.6;
            margin-bottom: 1rem;
            position: relative;
            padding-{border_side}: 1rem;
            border-{border_side}: 3px solid {accent_primary};
        }}

        .testimonial-author {{
            font-size: 0.875rem;
            font-weight: 600;
            color: {text_primary};
        }}

        .testimonial-role {{
            font-size: 0.8125rem;
            color: {text_secondary};
            margin-top: 0.25rem;
        }}

        /* ===== PARTNER LOGOS ===== */
        .partner-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }}

        .partner-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            text-align: center;
            transition: var(--transition-base);
        }}

        .partner-card:hover {{
            border-color: {border_medium};
            box-shadow: 0 4px 12px {shadow_color};
        }}

        .partner-logo {{
            font-size: 2.5rem;
            margin-bottom: 0.75rem;
        }}

        .partner-name {{
            font-size: 0.875rem;
            font-weight: 500;
            color: {text_primary};
        }}

        /* ===== DATA TABLES - STRIPE STYLE ===== */
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            direction: {direction};
        }}

        th {{
            background: {bg_tertiary} !important;
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: {text_tertiary} !important;
            padding: 0.75rem 1rem !important;
            text-align: {text_align} !important;
            border-bottom: 1px solid {border_light} !important;
        }}

        th:first-child {{ border-radius: var(--radius-md) 0 0 0; }}
        th:last-child {{ border-radius: 0 var(--radius-md) 0 0; }}

        td {{
            background: {bg_elevated} !important;
            font-size: 0.875rem !important;
            color: {text_primary} !important;
            padding: 0.875rem 1rem !important;
            text-align: {text_align} !important;
            border-bottom: 1px solid {border_light} !important;
        }}

        tr:hover td {{
            background: {bg_hover} !important;
        }}

        tr:last-child td:first-child {{ border-radius: 0 0 0 var(--radius-md); }}
        tr:last-child td:last-child {{ border-radius: 0 0 var(--radius-md) 0; }}

        /* ===== SUCCESS/INFO ALERTS ===== */
        .stSuccess {{
            background: {success_bg} !important;
            border: 1px solid {'#065F46' if theme == 'light' else '#34D399'}20 !important;
            border-radius: var(--radius-md) !important;
            color: {success_text} !important;
        }}

        .stInfo {{
            background: {accent_light} !important;
            border: 1px solid {accent_primary}20 !important;
            border-radius: var(--radius-md) !important;
        }}

        /* ===== DIVIDERS ===== */
        hr {{
            border: none !important;
            border-top: 1px solid {border_light} !important;
            margin: 1.5rem 0 !important;
        }}

        /* ===== FOOTER - MINIMAL ===== */
        .footer {{
            text-align: center;
            padding: 2rem 0;
            margin-top: 2rem;
            border-top: 1px solid {border_light};
        }}

        .footer p {{
            margin: 0.25rem 0;
        }}

        .footer-brand {{
            font-size: 0.875rem;
            font-weight: 600;
            color: {text_primary};
        }}

        .footer-partners {{
            font-size: 0.8125rem;
            color: {text_secondary};
        }}

        .footer-stats {{
            display: inline-block;
            background: linear-gradient(135deg, {gradient_start}15, {gradient_end}15);
            border: 1px solid {accent_primary}30;
            border-radius: var(--radius-full);
            padding: 0.5rem 1rem;
            margin-top: 0.75rem;
            font-size: 0.8125rem;
            font-weight: 500;
            color: {accent_primary};
        }}

        /* ===== COMPARISON CHART HEADER ===== */
        .comparison-header {{
            background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
            border-radius: var(--radius-xl);
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
        }}

        .comparison-header h2 {{
            color: white !important;
            text-align: center;
        }}

        .comparison-header p {{
            color: rgba(255,255,255,0.8) !important;
            text-align: center;
        }}

        /* ===== CONCLUSION BOX ===== */
        .conclusion-box {{
            background: {success_bg};
            border: 2px solid {success};
            border-radius: var(--radius-xl);
            padding: 1.25rem 1.5rem;
            text-align: center;
        }}

        .conclusion-box h3 {{
            color: {'#065F46' if theme == 'light' else success} !important;
            font-size: 1rem !important;
            margin: 0 !important;
        }}

        /* ===== PLOTLY CHARTS ===== */
        .js-plotly-plot {{
            border-radius: var(--radius-lg) !important;
        }}

        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {{
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}

            .partner-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .hero-header {{
                padding: 1.5rem;
            }}

            .hero-header h2 {{
                font-size: 1.25rem !important;
            }}

            .timeline-container {{
                padding-{border_side}: 1.5rem;
            }}

            .timeline-container::before {{
                {border_side}: 0.5rem;
            }}

            .timeline-item::before {{
                {border_side}: -1.5rem;
            }}
        }}

        @media (max-width: 480px) {{
            .kpi-value {{
                font-size: 1.5rem;
            }}

            .partner-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    """


# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Programme National IA - BBC School",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE INIT
# ============================================
if "lang" not in st.session_state:
    st.session_state.lang = "fr"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_response" not in st.session_state:
    st.session_state.current_response = None

# Initialize Translator
T = Translator(st.session_state.lang)

# ============================================
# DATA
# ============================================
COMPETITORS = {
    "IAFactory": {"prix_ecole": 1.1, "color": "#10B981"},
    "EduTech Pro": {"prix_ecole": 3.5, "color": "#EF4444"},
    "SmartEdu AI": {"prix_ecole": 4.2, "color": "#3B82F6"},
    "Microsoft EDU": {"prix_ecole": 5.0, "color": "#8B5CF6"}
}

PARTNERS = [
    {"name": "UNESCO", "logo": "🇺🇳"},
    {"name": "Ministère", "logo": "🇩🇿"},
    {"name": "Devrabic", "logo": "💻"},
    {"name": "HES-SO", "logo": "🇨🇭"}
]


def get_timeline_events(t: Translator) -> list:
    return [
        {"date": t.t("timeline.dec_2025"), "event": t.t("timeline.event_selection"), "phase": t.t("timeline.phase_prep"), "status": "done"},
        {"date": t.t("timeline.jan_2026"), "event": t.t("timeline.event_training"), "phase": t.t("timeline.phase_training"), "status": "upcoming"},
        {"date": t.t("timeline.feb_2026"), "event": t.t("timeline.event_launch"), "phase": t.t("timeline.phase_launch"), "status": "milestone"},
        {"date": t.t("timeline.feb_jun_2026"), "event": t.t("timeline.event_students"), "phase": t.t("timeline.phase_pilot"), "status": "upcoming"},
        {"date": t.t("timeline.jun_2026"), "event": t.t("timeline.event_summit"), "phase": t.t("timeline.phase_event"), "status": "milestone"},
        {"date": t.t("timeline.jul_dec_2026"), "event": t.t("timeline.event_expansion"), "phase": t.t("timeline.phase_expansion"), "status": "future"},
        {"date": t.t("timeline.jan_2027"), "event": t.t("timeline.event_phase2"), "phase": t.t("timeline.phase_scale"), "status": "future"},
        {"date": t.t("timeline.q3_2027"), "event": t.t("timeline.event_pitch"), "phase": t.t("timeline.phase_strategy"), "status": "future"},
        {"date": t.t("timeline.jan_2028"), "event": t.t("timeline.event_contract"), "phase": t.t("timeline.phase_jackpot"), "status": "milestone"}
    ]


def get_testimonials(t: Translator) -> list:
    return [
        {"quote": t.t("testimonials.quote1"), "author": t.t("testimonials.author1"), "role": t.t("testimonials.role1"), "program": t.t("testimonials.program1"), "icon": "🏆"},
        {"quote": t.t("testimonials.quote2"), "author": t.t("testimonials.author2"), "role": t.t("testimonials.role2"), "program": t.t("testimonials.program2"), "icon": "📈"},
        {"quote": t.t("testimonials.quote3"), "author": t.t("testimonials.author3"), "role": t.t("testimonials.role3"), "program": t.t("testimonials.program3"), "icon": "🎓"}
    ]


# ============================================
# MAIN APP
# ============================================
def main():
    T = Translator(st.session_state.lang)
    is_rtl = T.is_rtl()

    # Apply premium CSS
    st.markdown(get_premium_css(st.session_state.theme, is_rtl), unsafe_allow_html=True)

    # ===== HEADER =====
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem 0;'>
            <p style='font-size: 0.875rem; font-weight: 500; color: #3B82F6; margin: 0 0 0.5rem 0;'>
                {'البرنامج الوطني للذكاء الاصطناعي' if is_rtl else 'PROGRAMME NATIONAL IA'}
            </p>
            <h1 style='font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.02em;'>
                {T.t('app.title')}
            </h1>
            <p style='font-size: 0.9375rem; margin: 0.5rem 0 0 0;'>
                {T.t('app.subtitle')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown(f"## {T.t('sidebar.title')}")

        st.metric(T.t('sidebar.roi_label'), T.t('sidebar.roi_value'), T.t('sidebar.roi_delta'))
        st.metric(T.t('sidebar.cost_label'), T.t('sidebar.cost_value'), T.t('sidebar.cost_delta'))
        st.metric(T.t('sidebar.students_label'), T.t('sidebar.students_value'), T.t('sidebar.students_delta'))

        st.markdown("---")

        # Language selector
        st.markdown(f"### {T.t('sidebar.language')}")
        lang_options = {"Français": "fr", "العربية": "ar", "English": "en"}
        current_lang_name = [k for k, v in lang_options.items() if v == st.session_state.lang][0]
        selected_lang = st.selectbox(
            "Language",
            options=list(lang_options.keys()),
            index=list(lang_options.keys()).index(current_lang_name),
            label_visibility="collapsed"
        )
        if lang_options[selected_lang] != st.session_state.lang:
            st.session_state.lang = lang_options[selected_lang]
            st.rerun()

        # Theme selector
        st.markdown(f"### {T.t('sidebar.theme')}")
        theme_options = {T.t('sidebar.light'): "light", T.t('sidebar.dark'): "dark"}
        current_theme_name = [k for k, v in theme_options.items() if v == st.session_state.theme][0]
        selected_theme = st.selectbox(
            "Theme",
            options=list(theme_options.keys()),
            index=list(theme_options.keys()).index(current_theme_name),
            label_visibility="collapsed"
        )
        if theme_options[selected_theme] != st.session_state.theme:
            st.session_state.theme = theme_options[selected_theme]
            st.rerun()

    # ===== MAIN TABS =====
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        f"🎯 {T.t('tabs.summary')}",
        f"💰 {T.t('tabs.budget')}",
        f"⚔️ {T.t('tabs.competition')}",
        f"🚀 {T.t('tabs.strategy')}",
        f"📅 {T.t('tabs.timeline')}",
        f"💬 {T.t('tabs.testimonials')}",
        f"📊 {T.t('tabs.charts')}"
    ])

    # ============================================
    # TAB 1: RÉSUMÉ
    # ============================================
    with tab1:
        st.markdown(f"""
        <div class='hero-header'>
            <h2>🎯 {T.t('summary.title')}</h2>
        </div>
        """, unsafe_allow_html=True)

        # KPI Cards
        st.markdown(f"""
        <div class='kpi-grid'>
            <div class='kpi-card green'>
                <div class='kpi-label'>1️⃣ {T.t('summary.phase1_title')}</div>
                <div class='kpi-value green'>{T.t('summary.phase1_value')}</div>
                <div class='kpi-desc'>{T.t('summary.phase1_desc').replace(chr(10), '<br>')}</div>
            </div>
            <div class='kpi-card blue'>
                <div class='kpi-label'>2️⃣ {T.t('summary.phase2_title')}</div>
                <div class='kpi-value blue'>{T.t('summary.phase2_value')}</div>
                <div class='kpi-desc'>{T.t('summary.phase2_desc').replace(chr(10), '<br>')}</div>
            </div>
            <div class='kpi-card orange'>
                <div class='kpi-label'>3️⃣ {T.t('summary.phase3_title')}</div>
                <div class='kpi-value orange'>{T.t('summary.phase3_value')}</div>
                <div class='kpi-desc'>{T.t('summary.phase3_desc').replace(chr(10), '<br>')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"### {T.t('summary.quick_actions')}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📋 {T.t('summary.executive_summary')}", use_container_width=True, type="primary"):
                st.session_state.current_response = "executive_summary"
        with col2:
            if st.button(f"🤖 {T.t('summary.module_l2')}", use_container_width=True):
                st.session_state.current_response = "module_l2"
        with col3:
            if st.button(f"📝 {T.t('summary.ethics_quiz')}", use_container_width=True):
                st.session_state.current_response = "quiz"

        if st.session_state.current_response:
            st.markdown("---")
            with st.spinner(T.t('common.loading')):
                time.sleep(0.3)
            st.markdown(T.t(f'responses.{st.session_state.current_response}', T.t('responses.executive_summary')))

    # ============================================
    # TAB 2: BUDGET
    # ============================================
    with tab2:
        st.markdown(f"""
        <div class='hero-header'>
            <h2>💰 {T.t('budget.title')}</h2>
            <p>{T.t('budget.subtitle')}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric(T.t('budget.cost_label'), "0 DA", "100% offert", delta_color="off")
        with col2: st.metric(T.t('budget.students_label'), "1,600", "BBC School")
        with col3: st.metric(T.t('budget.investment_label'), "4.8M DA", "stratégique")
        with col4: st.metric(T.t('budget.roi_label'), "×47-×104", "250-555M DA")

        st.markdown("---")
        st.markdown(f"### ✅ {T.t('budget.infrastructure_title')}")

        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**🖥️ {T.t('budget.ia_local')}**: {T.t('budget.ia_local_desc')}")
            st.success(f"**🏗️ {T.t('budget.tech')}**: {T.t('budget.tech_desc')}")
        with col2:
            st.success(f"**☁️ {T.t('budget.ia_cloud')}**: {T.t('budget.ia_cloud_desc')}")
            st.success(f"**👥 {T.t('budget.personnel')}**: {T.t('budget.personnel_desc')}")

        st.markdown("---")
        st.markdown(f"### 📊 {T.t('budget.budget_detail')}")
        st.markdown(f"""
| {T.t('budget.item')} | {T.t('budget.iaf_pays')} | {T.t('budget.bbc_pays')} |
|:------|---------------:|----------:|
| {T.t('budget.training')} | 500,000 DA | **0 DA** ✅ |
| {T.t('budget.content')} | 2,000,000 DA | **0 DA** ✅ |
| {T.t('budget.platform')} | 1,500,000 DA | **0 DA** ✅ |
| {T.t('budget.support')} | 800,000 DA | **0 DA** ✅ |
| **{T.t('budget.total')}** | **4,800,000 DA** | **0 DA** |
        """)

    # ============================================
    # TAB 3: CONCURRENCE
    # ============================================
    with tab3:
        st.markdown(f"""
        <div class='comparison-header'>
            <h2>⚔️ {T.t('competition.title')}</h2>
            <p>{T.t('competition.subtitle')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 💰 {T.t('competition.price_comparison')}")

        price_df = pd.DataFrame({
            "Fournisseur": list(COMPETITORS.keys()),
            "Prix (M DA)": [c["prix_ecole"] for c in COMPETITORS.values()]
        })

        fig = go.Figure(go.Bar(
            x=price_df["Prix (M DA)"],
            y=price_df["Fournisseur"],
            orientation='h',
            marker_color=[c["color"] for c in COMPETITORS.values()],
            text=price_df["Prix (M DA)"].apply(lambda x: f"{x}M DA"),
            textposition='outside'
        ))
        fig.update_layout(
            height=280,
            margin=dict(l=0, r=40, t=20, b=20),
            xaxis_title="",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown(f"### 📊 {T.t('competition.detailed_comparison')}")

        st.markdown(f"""
| {T.t('competition.criteria')} | IAFactory | EduTech Pro | SmartEdu AI | Microsoft |
|:------|:----------:|:------------:|:------------:|:----------:|
| **{T.t('competition.price_school')}** | **1.1M** ✅ | 3.5M | 4.2M | 5M |
| **{T.t('competition.ai_used')}** | **{T.t('competition.free')}** ✅ | Payant | Payant | Payant |
| **{T.t('competition.training')}** | **40h** ✅ | 8h | Payant | Non |
| **{T.t('competition.support')}** | **{T.t('competition.included')}** ✅ | Payant | Payant | Payant |
| **{T.t('competition.algerian_content')}** | **100%** ✅ | 0% | 0% | 30% |
| **{T.t('competition.offline')}** | ✅ **{T.t('competition.yes')}** | ❌ | ❌ | ❌ |
        """)

        st.markdown(f"""
        <div class='conclusion-box'>
            <h3>🏆 {T.t('competition.conclusion')}</h3>
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # TAB 4: STRATÉGIE
    # ============================================
    with tab4:
        st.markdown(f"""
        <div class='hero-header' style='background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);'>
            <h2>🚀 {T.t('strategy.title')}</h2>
        </div>
        """, unsafe_allow_html=True)

        # Phase 1
        st.markdown(f"""
        <div class='phase-card phase-1'>
            <h3>📍 {T.t('strategy.phase1_title')}</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"**{T.t('strategy.phase1_actions')}** {T.t('strategy.phase1_details')}")
        with col2: st.metric(T.t('strategy.investment'), "4.8M DA", T.t('strategy.offered'))
        with col3: st.metric(T.t('strategy.revenue'), "0 DA", T.t('strategy.investment_phase'), delta_color="off")

        st.markdown("---")

        # Phase 2
        st.markdown(f"""
        <div class='phase-card phase-2'>
            <h3>🎪 {T.t('strategy.phase2_title')}</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"**{T.t('strategy.phase1_actions')}** {T.t('strategy.phase2_details')}")
        with col2: st.metric(T.t('strategy.schools'), "50", "+49")
        with col3: st.metric(T.t('strategy.revenue'), "55M DA", T.t('strategy.profit'))

        st.markdown("---")

        # Phase 3
        st.markdown(f"""
        <div class='phase-card phase-3'>
            <h3>🏆 {T.t('strategy.phase3_title')}</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f"**{T.t('strategy.phase1_actions')}** {T.t('strategy.phase3_details')}")
        with col2: st.metric(T.t('strategy.schools'), "500", "+450")
        with col3: st.metric(T.t('strategy.students'), "50,000", "+45,000")
        with col4: st.metric(T.t('strategy.revenue'), "500M DA", T.t('strategy.jackpot'))

        st.markdown("---")
        st.markdown(f"### 📈 {T.t('strategy.roi_summary')}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
| {T.t('strategy.phase')} | {T.t('strategy.investment')} | {T.t('strategy.revenue')} |
|:------|---------------:|----------:|
| Phase 1 | 4.8M DA | 0 DA |
| Phase 2 | 0.5M DA | 55M DA |
| Phase 3 | Variable | 500M DA |
| **TOTAL** | **5.3M DA** | **555M DA** |
            """)
        with col2:
            st.markdown(f"""
| {T.t('strategy.scenario')} | {T.t('strategy.revenue')} | ROI |
|:----------|--------:|------:|
| 🔴 {T.t('strategy.pessimistic')} | 250M DA | **×47** |
| 🟡 {T.t('strategy.realistic')} | 375M DA | **×70** |
| 🟢 {T.t('strategy.optimistic')} | 555M DA | **×104** |
            """)

    # ============================================
    # TAB 5: TIMELINE
    # ============================================
    with tab5:
        st.markdown(f"""
        <div class='hero-header' style='background: linear-gradient(135deg, #059669 0%, #10B981 100%);'>
            <h2>📅 {T.t('timeline.title')}</h2>
        </div>
        """, unsafe_allow_html=True)

        timeline_events = get_timeline_events(T)

        st.markdown("<div class='timeline-container'>", unsafe_allow_html=True)
        for event in timeline_events:
            status_class = event["status"]
            st.markdown(f"""
            <div class='timeline-item {status_class}'>
                <div class='timeline-date'>{event['date']}</div>
                <div class='timeline-title'>{event['event']}</div>
                <span class='timeline-badge'>{event['phase']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ============================================
    # TAB 6: TÉMOIGNAGES
    # ============================================
    with tab6:
        st.markdown(f"""
        <div class='hero-header' style='background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);'>
            <h2>💬 {T.t('testimonials.title')}</h2>
        </div>
        """, unsafe_allow_html=True)

        testimonials = get_testimonials(T)

        for t_item in testimonials:
            st.markdown(f"""
            <div class='testimonial-card'>
                <div class='testimonial-icon'>{t_item['icon']}</div>
                <div class='testimonial-quote'>"{t_item['quote']}"</div>
                <div class='testimonial-author'>— {t_item['author']}</div>
                <div class='testimonial-role'>{t_item['role']} • {t_item['program']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"### 🤝 {T.t('testimonials.partners_title')}")

        st.markdown("<div class='partner-grid'>", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, p in enumerate(PARTNERS):
            with cols[i]:
                st.markdown(f"""
                <div class='partner-card'>
                    <div class='partner-logo'>{p['logo']}</div>
                    <div class='partner-name'>{p['name']}</div>
                </div>
                """, unsafe_allow_html=True)

    # ============================================
    # TAB 7: GRAPHIQUES
    # ============================================
    with tab7:
        st.markdown(f"### 📈 {T.t('charts.revenue_title')}")

        revenue_df = pd.DataFrame({
            "Année": ["2026", "2027", "2028"],
            "Revenus": [0, 55, 500],
            "Profit": [-4.8, 49.7, 549.7]
        })

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=revenue_df["Année"],
            y=revenue_df["Revenus"],
            name=T.t('charts.revenue_annual'),
            marker_color="#10B981",
            text=revenue_df["Revenus"].apply(lambda x: f"{x}M"),
            textposition='outside'
        ))
        fig1.add_trace(go.Scatter(
            x=revenue_df["Année"],
            y=revenue_df["Profit"],
            name=T.t('charts.profit_cumulative'),
            line=dict(color="#F59E0B", width=3),
            mode='lines+markers+text',
            text=revenue_df["Profit"].apply(lambda x: f"{x}M"),
            textposition='top center'
        ))
        fig1.update_layout(
            title=T.t('charts.projection_title'),
            height=400,
            yaxis_title=T.t('charts.amount'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 💰 {T.t('charts.price_comparison')}")
            fig2 = go.Figure(go.Bar(
                x=[1.1, 3.5, 4.2, 5.0],
                y=["IAFactory", "EduTech", "SmartEdu", "Microsoft"],
                orientation='h',
                marker_color=["#10B981", "#EF4444", "#3B82F6", "#8B5CF6"],
                text=["1.1M", "3.5M", "4.2M", "5M"],
                textposition='outside'
            ))
            fig2.update_layout(
                height=280,
                xaxis_title=T.t('charts.price_school'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter"),
                margin=dict(l=0, r=40, t=20, b=40)
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.markdown(f"### 🎯 {T.t('charts.investment_breakdown')}")
            fig3 = go.Figure(go.Pie(
                labels=[T.t('budget.training'), T.t('budget.content'), T.t('budget.platform'), T.t('budget.support')],
                values=[500000, 2000000, 1500000, 800000],
                hole=0.4,
                marker_colors=["#10B981", "#3B82F6", "#F59E0B", "#8B5CF6"]
            ))
            fig3.update_layout(
                height=280,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("---")
        st.markdown(f"### 🗺️ {T.t('charts.national_impact')}")

        expansion_df = pd.DataFrame({
            "Phase": ["2026", "2027", "2028"],
            "Écoles": [1, 50, 500],
            "Élèves": [1600, 5000, 50000]
        })

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=expansion_df["Phase"],
            y=expansion_df["Écoles"],
            name=T.t('charts.schools_count'),
            marker_color="#3B82F6",
            yaxis='y'
        ))
        fig4.add_trace(go.Scatter(
            x=expansion_df["Phase"],
            y=expansion_df["Élèves"],
            name=T.t('charts.students_count'),
            line=dict(color="#F59E0B", width=3),
            mode='lines+markers',
            yaxis='y2'
        ))
        fig4.update_layout(
            title=T.t('charts.expansion_title'),
            yaxis=dict(title=T.t('charts.schools_count'), side='left'),
            yaxis2=dict(title=T.t('charts.students_count'), overlaying='y', side='right'),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ===== FOOTER =====
    st.markdown(f"""
    <div class='footer'>
        <p class='footer-brand'>🇩🇿 {T.t('app.footer')}</p>
        <p class='footer-partners'>{T.t('app.partners')}</p>
        <div class='footer-stats'>{T.t('app.investment_summary')}</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
