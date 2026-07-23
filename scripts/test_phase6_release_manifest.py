"""Verify deterministic production release manifest generation."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.release.release_manifest_service import ReleaseManifestService
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "src").mkdir()
        (root / "scripts").mkdir()
        (root / "docs").mkdir()
        (root / "data").mkdir()
        (root / "src/example.py").write_text("VALUE = 1\n", encoding="utf-8")
        (root / "scripts/test_example.py").write_text(
            "print('passed')\n",
            encoding="utf-8",
        )
        (root / "docs/AI_HANDOVER.md").write_text(
            "# Handover\n",
            encoding="utf-8",
        )
        (root / "requirements.txt").write_text("requests\n", encoding="utf-8")
        (root / "data/private.json").write_text(
            '{"api_key": "excluded"}',
            encoding="utf-8",
        )

        service = ReleaseManifestService(root)
        destination = root / "manifest.json"
        service.export(destination)
        manifest = json.loads(destination.read_text(encoding="utf-8"))
        paths = [entry["path"] for entry in manifest["files"]]

        assert paths == sorted(paths)
        assert "src/example.py" in paths
        assert "scripts/test_example.py" in paths
        assert "requirements.txt" in paths
        assert not any(path.startswith("data/") for path in paths)
        assert manifest["file_count"] == len(manifest["files"])
        assert all(len(entry["sha256"]) == 64 for entry in manifest["files"])

    assert VERSION_INFO.version == "1.0.0"
    assert VERSION_INFO.package == "Package-100A-08"
    assert VERSION_INFO.build == 10
    assert VERSION_INFO.status == "Production"
    print("Phase 6 release manifest test passed.")


if __name__ == "__main__":
    main()
