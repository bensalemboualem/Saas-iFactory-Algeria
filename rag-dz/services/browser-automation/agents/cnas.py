"""
Agent CNAS - Caisse Nationale d'Assurance Sociale
Site: https://www.cnas.dz
"""

from typing import Dict, Any, List
from .base import BaseAutomationAgent


class CNASAgent(BaseAutomationAgent):
    """Agent pour automatiser CNAS (Sécurité Sociale Algérie)"""
    
    @property
    def service_name(self) -> str:
        return "cnas"
    
    @property
    def base_url(self) -> str:
        return "https://www.cnas.dz"
    
    async def get_attestation(self, nss: str) -> Dict[str, Any]:
        """
        Récupérer l'attestation d'affiliation CNAS
        
        Args:
            nss: Numéro de Sécurité Sociale (ex: "1234567890123")
        
        Returns:
            Informations d'affiliation et lien attestation
        """
        task = f"""
        Objectif: Récupérer l'attestation CNAS pour le numéro {nss}
        
        Étapes:
        1. Aller sur {self.base_url}
        2. Chercher "Espace assuré" ou "Attestation d'affiliation"
        3. Entrer le numéro de sécurité sociale: {nss}
        4. Récupérer les informations:
           - Nom et prénom de l'assuré
           - Statut d'affiliation (actif/inactif)
           - Date d'affiliation
           - Employeur actuel
           - Lien pour télécharger l'attestation PDF si disponible
        5. Retourner les données structurées
        
        Note: Certaines informations peuvent nécessiter une authentification.
        """
        
        result = await self.run_task(task)
        
        if result.get("success"):
            attestation = self._parse_attestation(result.get("result", ""))
            result["attestation"] = attestation
        
        return result
    
    async def get_historique(self, nss: str) -> Dict[str, Any]:
        """
        Récupérer l'historique des cotisations
        
        Args:
            nss: Numéro de Sécurité Sociale
        
        Returns:
            Historique des cotisations et employeurs
        """
        task = f"""
        Objectif: Récupérer l'historique CNAS pour {nss}
        
        Étapes:
        1. Aller sur {self.base_url}
        2. Accéder à l'historique des cotisations
        3. Entrer le NSS: {nss}
        4. Récupérer:
           - Liste des employeurs
           - Périodes de cotisation
           - Montants cotisés par année
           - Droits acquis (retraite, maladie)
        5. Retourner les données structurées
        """
        
        result = await self.run_task(task)
        
        if result.get("success"):
            historique = self._parse_historique(result.get("result", ""))
            result["historique"] = historique
        
        return result
    
    async def verifier_droits(self, nss: str) -> Dict[str, Any]:
        """
        Vérifier les droits ouverts (maladie, maternité, etc.)
        
        Args:
            nss: Numéro de Sécurité Sociale
        
        Returns:
            Droits ouverts et leur validité
        """
        task = f"""
        Objectif: Vérifier les droits CNAS ouverts pour {nss}
        
        Étapes:
        1. Aller sur {self.base_url}
        2. Chercher "Vérification des droits" ou "Couverture sociale"
        3. Entrer le NSS: {nss}
        4. Récupérer les droits:
           - Assurance maladie (oui/non, date validité)
           - Maternité
           - Accident de travail
           - Retraite (trimestres validés)
           - Allocations familiales
        5. Retourner les données structurées
        """
        
        return await self.run_task(task)
    
    async def get_carte_chifa(self, nss: str) -> Dict[str, Any]:
        """
        Informations sur la carte Chifa
        
        Args:
            nss: Numéro de Sécurité Sociale
        
        Returns:
            Statut carte Chifa et bénéficiaires
        """
        task = f"""
        Objectif: Récupérer infos carte Chifa pour {nss}
        
        Étapes:
        1. Aller sur {self.base_url}
        2. Chercher "Carte Chifa" ou "Tiers payant"
        3. Entrer le NSS: {nss}
        4. Récupérer:
           - Numéro carte Chifa
           - Date d'expiration
           - Liste des ayants droit (conjoint, enfants)
           - Statut activation
        5. Retourner les données structurées
        """
        
        return await self.run_task(task)
    
    def _parse_attestation(self, raw_result: str) -> Dict[str, Any]:
        """Parser le résultat pour extraire l'attestation"""
        return {
            "nom": "",
            "prenom": "",
            "nss": "",
            "statut": "actif",
            "date_affiliation": "",
            "employeur": "",
            "pdf_url": None
        }
    
    def _parse_historique(self, raw_result: str) -> Dict[str, Any]:
        """Parser le résultat pour extraire l'historique"""
        return {
            "employeurs": [],
            "cotisations": [],
            "trimestres_valides": 0
        }
