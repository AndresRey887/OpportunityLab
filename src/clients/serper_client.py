"""
Serper API Client
"""

import requests

from config.secrets import SERPER_API_KEY


class SerperClient:

    BASE_URL = "https://google.serper.dev/search"

    def search(self, query):

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query
        }

        response = requests.post(
            self.BASE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()