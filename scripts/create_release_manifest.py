"""Create dist/release-manifest.json for a production build."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.release.release_manifest_service import ReleaseManifestService


def main() -> None:
    destination = PROJECT_ROOT / "dist" / "release-manifest.json"
    ReleaseManifestService(PROJECT_ROOT).export(destination)
    print(f"Release manifest created: {destination}")


if __name__ == "__main__":
    main()
