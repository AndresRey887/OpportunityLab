"""Offline test for genuine multi-page Deep searching."""

from __future__ import annotations

import sys
import types
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if "requests" not in sys.modules:
    sys.modules["requests"] = types.SimpleNamespace(post=lambda *args, **kwargs: None)
if "config.secrets" not in sys.modules:
    secrets_stub = types.ModuleType("config.secrets")
    secrets_stub.SERPER_API_KEY = "offline-test-key"
    sys.modules["config.secrets"] = secrets_stub

import src.clients.serper_client as serper_module
from src.clients.serper_client import SerperClient
from src.version import VERSION_INFO


class Response:
    def __init__(self, page):
        self.page = page

    def raise_for_status(self):
        return None

    def json(self):
        start = (self.page - 1) * 10
        return {
            "organic": [
                {
                    "title": f"Result {number}",
                    "link": f"https://example.com/{number}",
                }
                for number in range(start, start + 10)
            ]
        }


def main() -> None:
    pages = []
    original_post = serper_module.requests.post

    def fake_post(url, *, json, headers, timeout):
        pages.append(json["page"])
        return Response(json["page"])

    try:
        serper_module.requests.post = fake_post
        client = SerperClient()
        client.set_result_count(30)
        data = client.search("community grants")
    finally:
        serper_module.requests.post = original_post

    assert pages == [1, 2, 3]
    assert len(data["organic"]) == 30
    assert len({item["link"] for item in data["organic"]}) == 30

    company_source = (
        PROJECT_ROOT
        / "src"
        / "discovery"
        / "company_website_search_source.py"
    ).read_text(encoding="utf-8")
    assert "[:350]" in company_source
    assert "grant OR sponsorship OR partnership OR support" in company_source

    assert VERSION_INFO.version == "1.2.1"
    assert VERSION_INFO.package == "Package-110A-07A"
    assert VERSION_INFO.build == 10
    print("Deep search paging test passed.")


if __name__ == "__main__":
    main()
