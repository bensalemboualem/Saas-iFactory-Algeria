"""
Daily Briefing Engine - Geneva Digital Butler
=============================================

Génère le briefing matinal intelligent:
- Météo locale (quartier précis)
- Top 3 emails prioritaires
- Prochains RDV agenda
- Rappels médicaments/tâches
- Trajets recommandés
- Actualités Genève

Output: Texte formaté pour TTS (Text-to-Speech)

Created: 2025-01-16
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import os
import requests

from .workspace_connector import get_top_priority_emails, get_next_calendar_event
from .workspace_connector import format_email_summary_for_briefing, format_calendar_event_for_briefing
from .travel_service import get_geneva_optimized_route, format_route_for_voice_briefing

logger = logging.getLogger(__name__)


async def get_weather_geneva(
    location: str = "Genève",
    language: str = "fr"
) -> Dict[str, Any]:
    """
    Récupère la météo pour Genève

    Args:
        location: Quartier spécifique ('Eaux-Vives', 'Plainpalais', etc.)
        language: Langue réponse

    Returns:
        Dict avec météo
    """
    api_key = os.getenv('OPENWEATHER_API_KEY')

    if not api_key:
        logger.warning("OpenWeather API key not configured - using MOCK")
        return _mock_weather_geneva()

    try:
        # OpenWeather API
        base_url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            'q': f"{location},CH",  # Switzerland
            'appid': api_key,
            'lang': language,
            'units': 'metric',
        }

        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
        }

    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return _mock_weather_geneva()


def _mock_weather_geneva() -> Dict[str, Any]:
    """Mock météo pour development"""
    return {
        'temperature': 8,
        'feels_like': 6,
        'description': 'ciel dégagé',
        'humidity': 65,
        'wind_speed': 12,
        'icon': '01d',
    }


async def get_geneva_news() -> List[Dict[str, str]]:
    """
    Récupère actualités Genève

    Mock pour development
    Production: RSS Tribune de Genève, Le Temps, etc.
    """
    # TODO: Implement RSS parser for Geneva news
    return [
        {
            'title': 'Nouvelle politique parking Eaux-Vives: +20% tarifs dès février',
            'source': 'Tribune de Genève',
        },
        {
            'title': 'OMPI recrute: 15 nouveaux postes en propriété intellectuelle',
            'source': 'Le Temps',
        },
        {
            'title': 'Trafic: Gare Cornavin - travaux ligne ferroviaire ce week-end',
            'source': 'RTS Info',
        },
    ]


def format_weather_for_briefing(weather: Dict[str, Any], location: str) -> str:
    """Formate météo pour briefing vocal"""
    temp = int(weather['temperature'])
    description = weather['description']

    message = f"🌤️ MÉTÉO LOCALE\n"
    message += f"À {location}, il fera {temp}°C ce matin avec {description}.\n"

    # Conseils basés sur météo
    if weather.get('rain_forecast'):
        message += f"⚠️ Attention: Pluie prévue vers {weather['rain_forecast']['time']}\n"
        message += "Recommandation: Prends un parapluie avant de quitter le bureau.\n"

    elif temp < 5:
        message += "💡 Conseil: Pense à mettre un manteau chaud.\n"

    return message


async def generate_daily_morning_brief(
    tenant_id: str,
    user_id: int,
    user_profile: Optional[Dict[str, Any]] = None
) -> str:
    """
    Génère le briefing matinal complet

    Args:
        tenant_id: UUID tenant
        user_id: ID utilisateur
        user_profile: Profil utilisateur (nom, nationalité, location, etc.)

    Returns:
        Texte formaté briefing complet
    """
    logger.info(f"🌅 Generating morning briefing for user {user_id}")

    # User defaults
    user_name = user_profile.get('name', 'Utilisateur') if user_profile else 'Utilisateur'
    user_nationality = user_profile.get('nationality', 'swiss') if user_profile else 'swiss'
    user_location = user_profile.get('location', 'Genève') if user_profile else 'Genève'
    user_email = user_profile.get('email', 'user@example.com') if user_profile else 'user@example.com'

    # Cultural greeting
    greeting = _get_cultural_greeting(user_nationality)

    # Build briefing
    briefing_lines = []

    # 1. GREETING
    briefing_lines.append(f"Bonjour {user_name}! {greeting}")
    briefing_lines.append("")

    # 2. WEATHER
    try:
        weather = await get_weather_geneva(location=user_location)
        weather_text = format_weather_for_briefing(weather, user_location)
        briefing_lines.append(weather_text)
    except Exception as e:
        logger.error(f"Error getting weather: {e}")

    # 3. CALENDAR
    briefing_lines.append("📅 TON AGENDA AUJOURD'HUI")
    try:
        next_event = await get_next_calendar_event(user_email)
        if next_event:
            event_text = format_calendar_event_for_briefing(next_event)
            briefing_lines.append(event_text)

            # Calculate route to event location
            if next_event.get('location'):
                route_result = get_geneva_optimized_route(
                    origin=user_location,
                    destination=next_event['location'],
                    departure_time=next_event['start_time'] - timedelta(minutes=30),
                    compare_modes=True
                )
                route_text = format_route_for_voice_briefing(
                    origin=user_location,
                    destination=next_event['location'],
                    route_recommendation=route_result['recommendation']
                )
                briefing_lines.append(route_text)
        else:
            briefing_lines.append("Aucun rendez-vous prévu aujourd'hui.\n")
    except Exception as e:
        logger.error(f"Error getting calendar: {e}")

    # 4. MEDICATION REMINDERS (Mock for now)
    # TODO: Get from user_reminders table
    briefing_lines.append("💊 SANTÉ - RAPPEL MÉDICAMENT")
    briefing_lines.append("N'oublie pas ton complément vitamine D après le petit-déjeuner.")
    briefing_lines.append("")

    # 5. TOP EMAILS
    briefing_lines.append("📧 EMAILS IMPORTANTS")
    try:
        top_emails = await get_top_priority_emails(user_email, limit=3)
        if top_emails:
            briefing_lines.append(f"J'ai scanné ta boîte Gmail. Voici le TOP {len(top_emails)}:\n")
            for idx, email_summary in enumerate(top_emails, 1):
                email_text = format_email_summary_for_briefing(email_summary, idx)
                briefing_lines.append(email_text)
        else:
            briefing_lines.append("Aucun email important ce matin.\n")
    except Exception as e:
        logger.error(f"Error getting emails: {e}")

    # 6. NEWS GENEVA
    briefing_lines.append("📰 ACTUALITÉS GENÈVE")
    try:
        news_items = await get_geneva_news()
        for news in news_items[:3]:
            briefing_lines.append(f"- {news['title']}")
        briefing_lines.append("")
    except Exception as e:
        logger.error(f"Error getting news: {e}")

    # 7. ROI STATS (Mock for now)
    # TODO: Get from tokens_saved_tracking
    briefing_lines.append("🔋 STATISTIQUES PERSONNELLES")
    briefing_lines.append("- Heures transcrites ce mois: 12.5h")
    briefing_lines.append("- Tokens économisés vs Cloud: 45,000 (≈ $270 USD)")
    briefing_lines.append("- Termes juridiques appris: 156 expressions")
    briefing_lines.append("")

    # 8. CLOSING
    briefing_lines.append("Veux-tu que je te prépare un résumé vocal de ton prochain dossier")
    briefing_lines.append("pendant que tu prends ton petit-déjeuner?")

    # Combine all
    briefing_text = "\n".join(briefing_lines)

    logger.info(f"✅ Morning briefing generated ({len(briefing_text)} chars)")

    return briefing_text


def _get_cultural_greeting(nationality: str) -> str:
    """
    Génère salutation culturelle selon nationalité

    Args:
        nationality: Nationalité utilisateur

    Returns:
        Salutation dans langue maternelle
    """
    greetings = {
        'japanese': '早安 (Zǎo ān)!',
        'chinese': '早安 (Zǎo ān)!',
        'spanish': '¡Buenos días!',
        'algerian': 'صباح الخير (Sabah el kheer)!',
        'arabic': 'صباح الخير (Sabah el kheer)!',
        'italian': 'Buongiorno!',
        'german': 'Guten Morgen!',
        'swiss': 'Grüezi!',  # Swiss German
        'french': 'Bon matin!',
        'english': 'Good morning!',
        'american': 'Good morning!',
    }

    return greetings.get(nationality.lower(), '')


async def generate_quick_status_update(
    tenant_id: str,
    user_id: int
) -> str:
    """
    Génère un update rapide (pas le briefing complet)

    Args:
        tenant_id: UUID tenant
        user_id: ID utilisateur

    Returns:
        Texte court avec infos essentielles
    """
    lines = []

    # Next event
    next_event = await get_next_calendar_event("user@example.com")
    if next_event:
        start_time = next_event['start_time'].strftime('%Hh%M')
        lines.append(f"📅 Prochain RDV: {start_time} - {next_event['summary']}")

    # Urgent emails
    top_emails = await get_top_priority_emails("user@example.com", limit=1)
    if top_emails and top_emails[0].priority_level == 'urgent':
        lines.append(f"⚠️ Email urgent: {top_emails[0].subject[:50]}...")

    # Weather alert
    weather = await get_weather_geneva()
    if weather.get('rain_forecast'):
        lines.append("🌧️ Pluie prévue cet après-midi - Prends un parapluie")

    return "\n".join(lines) if lines else "Tout est calme aujourd'hui!"
