"""Verify persistent accessible OpportunityLab text-size settings."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.accessibility.display_settings_service import DisplaySettingsService
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        settings_file = Path(directory) / "display.json"
        service = DisplaySettingsService(settings_file)
        assert service.selected == "Normal"
        assert service.scale == 1.0
        assert service.select("Large") == 1.18
        assert json.loads(settings_file.read_text(encoding="utf-8")) == {
            "text_size": "Large"
        }
        reloaded = DisplaySettingsService(settings_file)
        assert reloaded.selected == "Large"
        assert reloaded.scale == 1.18
        assert reloaded.select("Extra Large") == 1.35

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    data_tools = (PROJECT_ROOT / "src/ui/data_tools_window.py").read_text(
        encoding="utf-8"
    )
    display_window = (
        PROJECT_ROOT / "src/ui/display_settings_window.py"
    ).read_text(encoding="utf-8")
    assert "ctk.set_widget_scaling" in main_window
    assert "Text Size" in data_tools
    assert "set_widget_scaling" in display_window
    assert VERSION_INFO.version == "1.1.0"
    assert VERSION_INFO.package == "Package-110A-01"
    assert VERSION_INFO.build == 1
    print("Text size settings test passed.")


if __name__ == "__main__":
    main()
