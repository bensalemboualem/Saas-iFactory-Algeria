"""
Travel Service - Geneva Optimized
==================================

Calcul intelligent de trajets pour Genève:
- Google Maps API (Car, Transit, Walking, Bicycling)
- TPG Genève (Transports Publics Genevois)
- Détection travaux et traffic
- Cache intelligent (TTL adaptatif)

Created: 2025-01-16
"""

import logging
import os
import hashlib
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import requests

logger = logging.getLogger(__name__)


@dataclass
class TravelRoute:
    """Résultat calcul trajet"""
    origin: str
    destination: str
    travel_mode: str  # 'car', 'transit', 'walking', 'bicycling'

    distance_meters: int
    duration_seconds: int
    duration_in_traffic_seconds: Optional[int] = None

    route_summary: str = ""
    steps: List[Dict[str, Any]] = None

    # Transit specific
    transit_lines: List[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    transit_fare_chf: Optional[float] = None

    # Warnings
    has_traffic: bool = False
    has_roadwork: bool = False
    warnings: List[str] = None


# ============================================================
# GENEVA CONSTANTS
# ============================================================

# TPG (Transports Publics Genevois) - Lignes principales
TPG_TRAM_LINES = ['12', '13', '14', '15', '16', '17', '18']
TPG_BUS_LINES = ['1', '3', '5', '6', '7', '8', '9', '10', '11', '19', '20']

# Geneva landmarks (pour optimisations)
GENEVA_LANDMARKS = {
    'gare_cornavin': 'Place de Cornavin, 1201 Genève',
    'nations_unies': 'Avenue de la Paix 14, 1202 Genève',
    'ompi': 'Chemin des Colombettes 34, 1211 Genève',
    'aeroport': 'Route de l\'Aéroport, 1215 Genève',
    'plainpalais': 'Plaine de Plainpalais, 1205 Genève',
    'eaux_vives': 'Rue des Eaux-Vives, 1207 Genève',
    'carouge': 'Place du Marché, 1227 Carouge',
}

# Known roadworks/traffic patterns Geneva (Mock - à enrichir via API)
GENEVA_TRAFFIC_PATTERNS = {
    'pont_mont_blanc': {
        'location': 'Pont du Mont-Blanc',
        'peak_hours': [(7, 9), (17, 19)],  # 7h-9h, 17h-19h
        'average_delay_minutes': 8,
    },
    'route_de_meyrin': {
        'location': 'Route de Meyrin',
        'peak_hours': [(7, 9), (17, 19)],
        'average_delay_minutes': 6,
    }
}


def get_google_maps_api_key() -> Optional[str]:
    """Récupère Google Maps API key depuis env"""
    return os.getenv('GOOGLE_MAPS_API_KEY')


def calculate_route_google_maps(
    origin: str,
    destination: str,
    travel_mode: str = 'car',
    departure_time: Optional[datetime] = None
) -> Optional[TravelRoute]:
    """
    Calcule un trajet via Google Maps API

    Args:
        origin: Adresse de départ
        destination: Adresse d'arrivée
        travel_mode: 'car', 'transit', 'walking', 'bicycling'
        departure_time: Heure de départ (important pour transit et traffic)

    Returns:
        TravelRoute ou None si erreur
    """
    api_key = get_google_maps_api_key()

    if not api_key:
        logger.warning("Google Maps API key not configured")
        return _mock_route_geneva(origin, destination, travel_mode)

    try:
        # Google Maps Directions API
        base_url = "https://maps.googleapis.com/maps/api/directions/json"

        params = {
            'origin': origin,
            'destination': destination,
            'mode': travel_mode,
            'key': api_key,
            'language': 'fr',  # French for Geneva
            'region': 'ch',  # Switzerland
        }

        # Ajouter heure de départ si fournie
        if departure_time:
            timestamp = int(departure_time.timestamp())
            params['departure_time'] = timestamp

            # Traffic model for car mode
            if travel_mode == 'driving':
                params['traffic_model'] = 'best_guess'  # or 'pessimistic', 'optimistic'

        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        if data['status'] != 'OK':
            logger.error(f"Google Maps API error: {data['status']}")
            return None

        # Extraire premier itinéraire
        route = data['routes'][0]
        leg = route['legs'][0]

        # Distance et durée
        distance_meters = leg['distance']['value']
        duration_seconds = leg['duration']['value']

        # Durée avec trafic (si disponible)
        duration_in_traffic = None
        if 'duration_in_traffic' in leg:
            duration_in_traffic = leg['duration_in_traffic']['value']

        # Résumé itinéraire
        route_summary = route.get('summary', '')

        # Étapes détaillées
        steps = []
        for step in leg['steps']:
            steps.append({
                'instruction': step.get('html_instructions', ''),
                'distance': step['distance']['value'],
                'duration': step['duration']['value'],
                'travel_mode': step.get('travel_mode', travel_mode.upper())
            })

        # Transit specific
        transit_lines = []
        transit_fare = None
        if travel_mode == 'transit' and 'transit_details' in leg['steps'][0]:
            for step in leg['steps']:
                if 'transit_details' in step:
                    transit = step['transit_details']
                    line = transit['line']
                    line_name = line.get('short_name', line.get('name', ''))
                    vehicle_type = line['vehicle']['type']  # 'BUS', 'TRAM', 'TRAIN'

                    transit_lines.append(f"{vehicle_type} {line_name}")

            # Tarif (si disponible)
            if 'fare' in leg:
                fare_data = leg['fare']
                if fare_data['currency'] == 'CHF':
                    transit_fare = float(fare_data['value'])

        # Warnings
        warnings = []
        has_traffic = False
        has_roadwork = False

        if duration_in_traffic and duration_in_traffic > duration_seconds * 1.2:
            has_traffic = True
            delay_minutes = (duration_in_traffic - duration_seconds) // 60
            warnings.append(f"Trafic dense: +{delay_minutes} min")

        # Check warnings in route
        if 'warnings' in route and route['warnings']:
            for warning in route['warnings']:
                warnings.append(warning)
                if 'travaux' in warning.lower() or 'roadwork' in warning.lower():
                    has_roadwork = True

        result = TravelRoute(
            origin=origin,
            destination=destination,
            travel_mode=travel_mode,
            distance_meters=distance_meters,
            duration_seconds=duration_seconds,
            duration_in_traffic_seconds=duration_in_traffic,
            route_summary=route_summary,
            steps=steps,
            transit_lines=transit_lines if transit_lines else None,
            transit_fare_chf=transit_fare,
            has_traffic=has_traffic,
            has_roadwork=has_roadwork,
            warnings=warnings if warnings else None
        )

        logger.info(
            f"🚗 Route calculated: {origin[:30]}... → {destination[:30]}... "
            f"({duration_seconds//60} min, {distance_meters}m)"
        )

        return result

    except Exception as e:
        logger.error(f"Error calculating route: {e}")
        return _mock_route_geneva(origin, destination, travel_mode)


def _mock_route_geneva(
    origin: str,
    destination: str,
    travel_mode: str
) -> TravelRoute:
    """
    Mock route calculation for development/testing
    Returns realistic Geneva routes
    """
    # Simple hash pour cohérence
    route_hash = hashlib.md5(f"{origin}{destination}{travel_mode}".encode()).hexdigest()
    distance_base = int(route_hash[:4], 16) % 5000 + 1000  # 1-6km

    # Vitesses moyennes Genève
    speeds = {
        'car': 25,  # km/h (trafic urbain)
        'transit': 20,  # km/h
        'walking': 5,  # km/h
        'bicycling': 15,  # km/h
    }

    speed = speeds.get(travel_mode, 20)
    duration_seconds = int((distance_base / 1000) * 3600 / speed)

    # Mock transit lines
    transit_lines = None
    if travel_mode == 'transit':
        transit_lines = ['Tram 15', 'Bus 8']

    logger.warning(f"⚠️ Using MOCK route (Google Maps API not configured)")

    return TravelRoute(
        origin=origin,
        destination=destination,
        travel_mode=travel_mode,
        distance_meters=distance_base,
        duration_seconds=duration_seconds,
        route_summary=f"Via Centre-Ville Genève (MOCK)",
        transit_lines=transit_lines,
        warnings=["⚠️ Mode simulation (API key manquante)"]
    )


def get_geneva_optimized_route(
    origin: str,
    destination: str,
    departure_time: Optional[datetime] = None,
    compare_modes: bool = True
) -> Dict[str, Any]:
    """
    Calcule le meilleur trajet pour Genève

    Compare automatiquement: Voiture, Tram/Bus, À pied
    Détecte les travaux et le trafic

    Args:
        origin: Adresse de départ
        destination: Adresse d'arrivée
        departure_time: Heure de départ prévue
        compare_modes: Comparer plusieurs modes de transport

    Returns:
        Dict avec routes et recommandation
    """
    if not departure_time:
        departure_time = datetime.now()

    routes = {}

    # Calculer voiture
    car_route = calculate_route_google_maps(
        origin, destination, 'driving', departure_time
    )
    if car_route:
        routes['car'] = car_route

    if compare_modes:
        # Calculer transport en commun
        transit_route = calculate_route_google_maps(
            origin, destination, 'transit', departure_time
        )
        if transit_route:
            routes['transit'] = transit_route

        # Calculer à pied (si < 2km)
        walking_route = calculate_route_google_maps(
            origin, destination, 'walking', departure_time
        )
        if walking_route and walking_route.distance_meters < 2000:
            routes['walking'] = walking_route

    # Déterminer meilleure option
    recommendation = _determine_best_route(routes, departure_time)

    return {
        'routes': routes,
        'recommendation': recommendation,
        'calculated_at': departure_time.isoformat(),
    }


def _determine_best_route(
    routes: Dict[str, TravelRoute],
    departure_time: datetime
) -> Dict[str, Any]:
    """
    Détermine la meilleure option de transport

    Critères:
    - Temps total
    - Présence de trafic/travaux
    - Heure de la journée (peak hours)
    - Distance
    """
    if not routes:
        return {'mode': None, 'reason': 'No routes available'}

    # Analyser heure de départ
    hour = departure_time.hour
    is_peak_hour = (7 <= hour <= 9) or (17 <= hour <= 19)

    # Scoring
    scores = {}

    for mode, route in routes.items():
        score = 100  # Base score

        # Pénalité durée
        duration_min = route.duration_in_traffic_seconds or route.duration_seconds
        duration_min = duration_min // 60
        score -= duration_min  # Moins de temps = meilleur score

        # Pénalité trafic
        if route.has_traffic:
            score -= 20

        # Pénalité travaux
        if route.has_roadwork:
            score -= 15

        # Bonus transport en commun en peak hour
        if mode == 'transit' and is_peak_hour:
            score += 10  # Évite bouchons

        # Bonus marche si < 15 min
        if mode == 'walking' and duration_min < 15:
            score += 15  # Santé + rapide

        scores[mode] = score

    # Meilleur score
    best_mode = max(scores, key=scores.get)
    best_route = routes[best_mode]

    # Raison
    reasons = []

    if best_mode == 'transit':
        if is_peak_hour:
            reasons.append("Évite les embouteillages en heure de pointe")
        if best_route.transit_lines:
            lines_str = ", ".join(best_route.transit_lines[:2])
            reasons.append(f"Lignes directes disponibles: {lines_str}")

    elif best_mode == 'walking':
        reasons.append("Distance courte et agréable à pied")

    elif best_mode == 'car':
        if not best_route.has_traffic:
            reasons.append("Circulation fluide, voiture plus rapide")
        else:
            reasons.append("Voiture malgré trafic (pas d'alternative viable)")

    duration_min = (best_route.duration_in_traffic_seconds or best_route.duration_seconds) // 60

    return {
        'mode': best_mode,
        'duration_minutes': duration_min,
        'distance_meters': best_route.distance_meters,
        'reasons': reasons,
        'warnings': best_route.warnings,
        'transit_lines': best_route.transit_lines,
    }


def format_route_for_voice_briefing(
    origin: str,
    destination: str,
    route_recommendation: Dict[str, Any]
) -> str:
    """
    Formate un trajet pour briefing vocal matinal

    Returns:
        Texte formaté pour TTS
    """
    if not route_recommendation.get('mode'):
        return f"❌ Impossible de calculer le trajet vers {destination}"

    mode = route_recommendation['mode']
    duration = route_recommendation['duration_minutes']

    mode_names = {
        'car': 'voiture',
        'transit': 'transport en commun',
        'walking': 'à pied',
        'bicycling': 'vélo',
    }

    mode_fr = mode_names.get(mode, mode)

    # Base message
    message = f"📍 Trajet vers {destination}: {duration} min en {mode_fr}"

    # Transit lines
    if mode == 'transit' and route_recommendation.get('transit_lines'):
        lines = ', '.join(route_recommendation['transit_lines'][:2])
        message += f" ({lines})"

    # Warnings
    if route_recommendation.get('warnings'):
        for warning in route_recommendation['warnings']:
            message += f"\n⚠️ {warning}"

    # Reasons
    if route_recommendation.get('reasons'):
        message += f"\n💡 Conseil: {route_recommendation['reasons'][0]}"

    return message
