"""
Agent Sonelgaz - Consultation factures électricité/gaz
Site: https://www.sonelgaz.dz ou espace client
"""

from typing import Dict, Any, List
from .base import BaseAutomationAgent


class SonelgazAgent(BaseAutomationAgent):
    """Agent pour automatiser Sonelgaz"""
    
    @property
    def service_name(self) -> str:
        return "sonelgaz"
    
    @property
    def base_url(self) -> str:
        return "https://www.sonelgaz.dz"
    
    async def get_factures(self, reference_client: str) -> Dict[str, Any]:
        """
        Récupérer les factures d'un client Sonelgaz
        
        Args:
            reference_client: Numéro de référence client (ex: "123456789")
        
        Returns:
            Liste des factures avec montants et dates
        """
        task = f"""
        Objectif: Récupérer les factures Sonelgaz pour le client {reference_client}
        
        Étapes:
        1. Aller sur {self.base_url}
        2. Chercher l'espace client ou consultation factures
        3. Entrer le numéro de référence: {reference_client}
        4. Récupérer toutes les factures visibles avec:
           - Numéro de facture
           - Date
           - Montant en DZD
           - Statut (payée/impayée)
        5. Retourner les données en format structuré
        
        Important: Si une page de login apparaît, noter qu'il faut des identifiants.
        """
        
        result = await self.run_task(task)
        
        # Parser le résultat pour extraire les factures
        if result.get("success"):
            factures = self._parse_factures(result.get("result", ""))
            result["factures"] = factures
        
        return result
    
    async def get_consommation(self, reference_client: str) -> Dict[str, Any]:
        """
        Récupérer l'historique de consommation
        
        Args:
            reference_client: Numéro de référence client
        
        Returns:
            Historique de consommation (kWh, m³)
        """
        task = f"""
        Objectif: Récupérer l'historique de consommation Sonelgaz pour {reference_client}
        
        Étapes:
        1. Aller sur {self.base_url}
        2. Accéder à l'espace consommation ou historique
        3. Entrer la référence: {reference_client}
        4. Récupérer les données de consommation:
           - Électricité (kWh) par mois
           - Gaz (m³) par mois si disponible
           - Graphiques ou tendances
        5. Retourner les données structurées
        """
        
        result = await self.run_task(task)
        
        if result.get("success"):
            consommation = self._parse_consommation(result.get("result", ""))
            result["consommation"] = consommation
        
        return result
    
    async def payer_facture(self, reference_client: str, numero_facture: str) -> Dict[str, Any]:
        """
        Initier le paiement d'une facture (redirection vers CIB/EDAHABIA)
        
        Args:
            reference_client: Numéro de référence client
            numero_facture: Numéro de la facture à payer
        
        Returns:
            URL de paiement ou instructions
        """
        task = f"""
        Objectif: Préparer le paiement de la facture Sonelgaz {numero_facture}
        
        Étapes:
        1. Aller sur {self.base_url}
        2. Accéder au paiement en ligne
        3. Entrer référence: {reference_client}
        4. Sélectionner la facture: {numero_facture}
        5. Aller jusqu'à la page de paiement (CIB ou EDAHABIA)
        6. NE PAS entrer de données bancaires
        7. Retourner l'URL de paiement et le montant
        
        IMPORTANT: Ne jamais entrer de données bancaires réelles.
        """
        
        return await self.run_task(task)
    
    def _parse_factures(self, raw_result: str) -> List[Dict[str, Any]]:
        """Parser le résultat brut pour extraire les factures"""
        # TODO: Implémenter le parsing intelligent avec le LLM
        factures = []
        
        # Exemple de structure attendue
        # Le LLM devrait retourner des données structurées
        
        return factures
    
    def _parse_consommation(self, raw_result: str) -> Dict[str, Any]:
        """Parser le résultat brut pour extraire la consommation"""
        return {
            "electricite_kwh": [],
            "gaz_m3": [],
            "periode": "12 derniers mois"
        }
