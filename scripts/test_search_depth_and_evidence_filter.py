"""Offline test for search depth and weak-evidence filtering."""

from __future__ import annotations

import sys
import tempfile
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
from src.filters.filter_engine import FilterEngine
from src.filters.filter_settings_store import FilterSettingsStore
from src.models.opportunity import Opportunity
from src.version import VERSION_INFO


class Response:
    def raise_for_status(self):
        return None

    def json(self):
        return {"organic": []}


def main() -> None:
    captured = {}
    original_post = serper_module.requests.post

    def fake_post(url, *, json, headers, timeout):
        captured["payload"] = dict(json)
        return Response()

    try:
        serper_module.requests.post = fake_post
        client = SerperClient()
        client.set_result_count(30)
        client.search("community grants")
    finally:
        serper_module.requests.post = original_post

    assert captured["payload"]["num"] == 10
    assert captured["payload"]["page"] == 1

    with tempfile.TemporaryDirectory() as directory:
        store = FilterSettingsStore(Path(directory) / "filters.json")
        engine = FilterEngine(store)
        engine.set_hide_weak_evidence(True)

        strong = Opportunity(title="Official grant")
        strong.metadata["evidence_quality_tier"] = "Strong Evidence"
        weak = Opportunity(title="General video")
        weak.metadata["evidence_quality_tier"] = "Weak Evidence"
        assert engine.process([strong, weak]) == [strong]
        assert engine.statistics.reasons == {"Weak evidence": 1}
        assert FilterEngine(store).is_hiding_weak_evidence()

    main_source = (
        PROJECT_ROOT / "src" / "ui" / "main_window.py"
    ).read_text(encoding="utf-8")
    filter_source = (
        PROJECT_ROOT / "src" / "ui" / "filter_window.py"
    ).read_text(encoding="utf-8")
    assert 'values=["Quick", "Standard", "Deep"]' in main_source
    assert 'text="Hide Weak Evidence"' in filter_source
    assert VERSION_INFO.version == "1.2.1"
    assert VERSION_INFO.package == "Package-110A-07A"
    assert VERSION_INFO.build == 10
    print("Search depth and evidence filter test passed.")


if __name__ == "__main__":
    main()
