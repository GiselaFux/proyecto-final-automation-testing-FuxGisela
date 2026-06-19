import requests
from typing import Dict, Any, Optional

from utils.logger import get_logger


class BaseAPIClient:
    """
    Cliente base para JSONPlaceholder.

    - La base URL.
    - Una sesión de Requests reutilizable.
    - Logging uniforme de requests y responses.

    Otros "clients" (posts, users, etc.) heredan de esta clase.
    """

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self):
        # Session permite reutilizar conexiones HTTP para mejor performance
        self.session = requests.Session()
        self.logger = get_logger(self.__class__.__name__)

    def _build_url(self, path: str) -> str:
        """
        Construye la URL completa a partir de la base y el path del recurso.
        """
        return f"{self.BASE_URL}{path}"

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """
        Registra en el log los datos principales del request.
        """
        self.logger.info(f"REQUEST {method} {url} | kwargs={kwargs}")

    def _log_response(self, response: requests.Response) -> None:
        """
        Registra en el log el status y el cuerpo (JSON o texto) de la respuesta.
        """
        try:
            body = response.json()
        except ValueError:
            body = response.text
        self.logger.info(
            f"RESPONSE {response.status_code} {response.url} | body={body}"
        )

    # ---- Métodos HTTP genéricos ----

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        url = self._build_url(path)
        self._log_request("GET", url, params=params)
        response = self.session.get(url, params=params)
        self._log_response(response)
        return response

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        url = self._build_url(path)
        self._log_request("POST", url, json=json)
        response = self.session.post(url, json=json)
        self._log_response(response)
        return response

    def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        url = self._build_url(path)
        self._log_request("PUT", url, json=json)
        response = self.session.put(url, json=json)
        self._log_response(response)
        return response

    def patch(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        url = self._build_url(path)
        self._log_request("PATCH", url, json=json)
        response = self.session.patch(url, json=json)
        self._log_response(response)
        return response

    def delete(self, path: str) -> requests.Response:
        url = self._build_url(path)
        self._log_request("DELETE", url)
        response = self.session.delete(url)
        self._log_response(response)
        return response