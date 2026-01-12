# -*- coding: utf-8 -*-
"""
AnythingLLM Integration Service
Bridge API pour communiquer avec AnythingLLM depuis le backend IAFactory
"""

import os
import requests
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    """Message de chat"""
    content: str
    role: str = "user"  # user, assistant, system


@dataclass
class ChatResponse:
    """Reponse du chat"""
    message: str
    sources: List[str]
    workspace: str
    success: bool
    error: Optional[str] = None


class AnythingLLMClient:
    """
    Client pour interagir avec AnythingLLM API

    Usage:
        client = AnythingLLMClient()
        response = client.chat("iafactory-academy", "Quel est le prix par eleve?")
        print(response.message)
    """

    def __init__(
        self,
        base_url: str = None,
        api_key: str = None
    ):
        """
        Initialise le client AnythingLLM

        Args:
            base_url: URL de base de l'API (defaut: http://localhost:3001)
            api_key: Cle API pour l'authentification
        """
        self.base_url = base_url or os.getenv("ANYTHINGLLM_URL", "http://localhost:3001")
        self.api_key = api_key or os.getenv("ANYTHINGLLM_API_KEY")
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Dict = None,
        files: Dict = None,
        timeout: int = 30
    ) -> Dict:
        """Effectue une requete HTTP vers l'API"""
        url = f"{self.base_url}/api{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=timeout)
            elif method == "POST":
                if files:
                    # Pour upload de fichiers, ne pas inclure Content-Type
                    headers = {k: v for k, v in self.headers.items() if k != "Content-Type"}
                    response = requests.post(url, headers=headers, files=files, timeout=timeout)
                else:
                    response = requests.post(url, headers=self.headers, json=data, timeout=timeout)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=timeout)
            else:
                raise ValueError(f"Methode HTTP non supportee: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.error(f"Timeout lors de la requete vers {url}")
            raise TimeoutError(f"Timeout lors de la requete vers AnythingLLM")
        except requests.exceptions.ConnectionError:
            logger.error(f"Impossible de se connecter a {url}")
            raise ConnectionError("Impossible de se connecter a AnythingLLM. Verifiez que le service est demarre.")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erreur HTTP: {e.response.status_code} - {e.response.text}")
            raise

    # =========================================
    # HEALTH & STATUS
    # =========================================

    def ping(self) -> bool:
        """Verifie si AnythingLLM est accessible"""
        try:
            result = self._request("GET", "/ping")
            return result.get("online", False)
        except:
            return False

    def get_system_settings(self) -> Dict:
        """Recupere les parametres systeme"""
        return self._request("GET", "/system")

    # =========================================
    # WORKSPACES
    # =========================================

    def list_workspaces(self) -> List[Dict]:
        """Liste tous les workspaces"""
        result = self._request("GET", "/workspaces")
        return result.get("workspaces", [])

    def get_workspace(self, slug: str) -> Optional[Dict]:
        """Recupere un workspace par son slug"""
        try:
            result = self._request("GET", f"/workspace/{slug}")
            return result.get("workspace")
        except:
            return None

    def create_workspace(self, name: str, slug: str = None) -> Dict:
        """Cree un nouveau workspace"""
        data = {"name": name}
        if slug:
            data["slug"] = slug
        return self._request("POST", "/workspace/new", data)

    def delete_workspace(self, slug: str) -> bool:
        """Supprime un workspace"""
        try:
            self._request("DELETE", f"/workspace/{slug}")
            return True
        except:
            return False

    def update_workspace(
        self,
        slug: str,
        system_prompt: str = None,
        chat_mode: str = None,
        similarity_threshold: float = None,
        top_n: int = None
    ) -> Dict:
        """Met a jour les parametres d'un workspace"""
        data = {}
        if system_prompt:
            data["openAiPrompt"] = system_prompt
        if chat_mode:
            data["chatMode"] = chat_mode  # "chat" ou "query"
        if similarity_threshold is not None:
            data["similarityThreshold"] = similarity_threshold
        if top_n is not None:
            data["topN"] = top_n

        return self._request("POST", f"/workspace/{slug}/update", data)

    # =========================================
    # DOCUMENTS
    # =========================================

    def upload_document(self, file_path: str) -> Dict:
        """Upload un document"""
        with open(file_path, "rb") as f:
            filename = os.path.basename(file_path)
            mime_type = self._get_mime_type(filename)
            files = {"file": (filename, f, mime_type)}
            return self._request("POST", "/document/upload", files=files, timeout=60)

    def _get_mime_type(self, filename: str) -> str:
        """Determine le type MIME d'un fichier"""
        ext = filename.lower().split(".")[-1]
        mime_types = {
            "md": "text/markdown",
            "txt": "text/plain",
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "json": "application/json",
            "csv": "text/csv"
        }
        return mime_types.get(ext, "application/octet-stream")

    def add_document_to_workspace(self, slug: str, document_location: str) -> Dict:
        """Ajoute un document uploade a un workspace (cree les embeddings)"""
        return self._request(
            "POST",
            f"/workspace/{slug}/update-embeddings",
            {"adds": [document_location]}
        )

    def remove_document_from_workspace(self, slug: str, document_location: str) -> Dict:
        """Retire un document d'un workspace"""
        return self._request(
            "POST",
            f"/workspace/{slug}/update-embeddings",
            {"deletes": [document_location]}
        )

    # =========================================
    # CHAT
    # =========================================

    def chat(
        self,
        workspace_slug: str,
        message: str,
        mode: str = "query",
        session_id: str = None
    ) -> ChatResponse:
        """
        Envoie un message au chatbot

        Args:
            workspace_slug: Slug du workspace
            message: Message a envoyer
            mode: "query" (RAG) ou "chat" (conversation libre)
            session_id: ID de session pour garder l'historique

        Returns:
            ChatResponse avec le message, les sources, etc.
        """
        try:
            data = {
                "message": message,
                "mode": mode
            }
            if session_id:
                data["sessionId"] = session_id

            result = self._request(
                "POST",
                f"/workspace/{workspace_slug}/chat",
                data,
                timeout=60
            )

            # Extraire les sources
            sources = []
            if "sources" in result:
                for source in result["sources"]:
                    if "title" in source:
                        sources.append(source["title"])

            return ChatResponse(
                message=result.get("textResponse", ""),
                sources=sources,
                workspace=workspace_slug,
                success=True
            )

        except Exception as e:
            logger.error(f"Erreur chat: {e}")
            return ChatResponse(
                message="",
                sources=[],
                workspace=workspace_slug,
                success=False,
                error=str(e)
            )

    def stream_chat(
        self,
        workspace_slug: str,
        message: str,
        mode: str = "query"
    ):
        """
        Envoie un message et recoit la reponse en streaming

        Yields:
            str: Morceaux de texte au fur et a mesure
        """
        url = f"{self.base_url}/api/workspace/{workspace_slug}/stream-chat"

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json={"message": message, "mode": mode},
                stream=True,
                timeout=60
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    yield line.decode("utf-8")

        except Exception as e:
            logger.error(f"Erreur stream: {e}")
            yield f"Erreur: {e}"

    # =========================================
    # THREADS (Historique)
    # =========================================

    def list_threads(self, workspace_slug: str) -> List[Dict]:
        """Liste les threads (conversations) d'un workspace"""
        try:
            result = self._request("GET", f"/workspace/{workspace_slug}/threads")
            return result.get("threads", [])
        except:
            return []

    def get_thread_history(self, workspace_slug: str, thread_slug: str) -> List[Dict]:
        """Recupere l'historique d'un thread"""
        try:
            result = self._request(
                "GET",
                f"/workspace/{workspace_slug}/thread/{thread_slug}/chats"
            )
            return result.get("history", [])
        except:
            return []


# =========================================
# FONCTIONS UTILITAIRES
# =========================================

def get_anythingllm_client() -> AnythingLLMClient:
    """Factory pour creer un client AnythingLLM"""
    return AnythingLLMClient()


def check_anythingllm_status() -> Dict[str, Any]:
    """Verifie le statut d'AnythingLLM"""
    client = get_anythingllm_client()

    status = {
        "online": False,
        "url": client.base_url,
        "workspaces": [],
        "error": None
    }

    try:
        status["online"] = client.ping()
        if status["online"]:
            status["workspaces"] = [
                {"name": ws.get("name"), "slug": ws.get("slug")}
                for ws in client.list_workspaces()
            ]
    except Exception as e:
        status["error"] = str(e)

    return status


# =========================================
# EXEMPLE D'UTILISATION
# =========================================

if __name__ == "__main__":
    # Test de connexion
    print("Test AnythingLLM Integration")
    print("=" * 50)

    client = AnythingLLMClient()

    # Verifier la connexion
    if client.ping():
        print("[OK] AnythingLLM est accessible")

        # Lister les workspaces
        workspaces = client.list_workspaces()
        print(f"[INFO] {len(workspaces)} workspace(s) trouve(s)")

        for ws in workspaces:
            print(f"  - {ws.get('name')} ({ws.get('slug')})")

        # Test de chat si workspace existe
        if workspaces:
            slug = workspaces[0].get("slug")
            print(f"\n[TEST] Chat avec workspace '{slug}'")

            response = client.chat(slug, "Quel est le prix par eleve?")

            if response.success:
                print(f"[REPONSE] {response.message[:200]}...")
                print(f"[SOURCES] {response.sources}")
            else:
                print(f"[ERREUR] {response.error}")
    else:
        print("[ERREUR] AnythingLLM n'est pas accessible")
        print("  Lancez: docker-compose up -d dans demo/anythingllm/")
