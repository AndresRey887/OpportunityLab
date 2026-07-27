"""
Serper API Client
"""

import requests

from config.secrets import SERPER_API_KEY


class SerperClient:

    BASE_URL = "https://google.serper.dev/search"

    def __init__(self):
        self.result_count = 20

    def set_result_count(self, result_count):
        self.result_count = max(10, min(int(result_count), 30))

    def search(self, query):

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        page_count = max(1, self.result_count // 10)
        combined = []
        seen_links = set()
        first_data = {}

        for page in range(1, page_count + 1):
            payload = {
                "q": query,
                "num": 10,
                "page": page,
            }

            try:
                response = requests.post(
                    self.BASE_URL,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
            except Exception:
                if combined:
                    break
                raise

            if page == 1 and isinstance(data, dict):
                first_data = dict(data)

            organic = data.get("organic", []) if isinstance(data, dict) else []
            if not isinstance(organic, list) or not organic:
                break

            added = 0
            for item in organic:
                if not isinstance(item, dict):
                    continue
                link = str(item.get("link", "") or "")
                key = link or repr(sorted(item.items()))
                if key in seen_links:
                    continue
                seen_links.add(key)
                combined.append(item)
                added += 1

            if added == 0:
                break

        first_data["organic"] = combined
        return first_data
