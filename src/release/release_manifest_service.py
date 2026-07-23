"""Create deterministic checksums for distributable OpportunityLab files."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from src.version import VERSION_INFO


class ReleaseManifestService:
    ROOT_FILES = (
        "OpportunityLab.spec",
        "requirements.txt",
        "requirements-build.txt",
    )
    ROOT_DIRECTORIES = ("src", "scripts", "docs")
    EXCLUDED_SUFFIXES = (".pyc",)

    def __init__(self, project_root: str | Path = ".") -> None:
        self.project_root = Path(project_root)

    def release_files(self) -> tuple[Path, ...]:
        files = []
        for name in self.ROOT_FILES:
            path = self.project_root / name
            if path.is_file():
                files.append(path)
        for directory_name in self.ROOT_DIRECTORIES:
            directory = self.project_root / directory_name
            if not directory.is_dir():
                continue
            files.extend(
                path for path in directory.rglob("*")
                if self._included(path)
            )
        return tuple(
            sorted(files, key=lambda path: path.relative_to(self.project_root).as_posix())
        )

    def create(self) -> dict:
        entries = []
        for path in self.release_files():
            entries.append(
                {
                    "path": path.relative_to(self.project_root).as_posix(),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "size": path.stat().st_size,
                }
            )
        return {
            "application": VERSION_INFO.app_name,
            "version": VERSION_INFO.version,
            "package": VERSION_INFO.package,
            "build": VERSION_INFO.build,
            "status": VERSION_INFO.status,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "file_count": len(entries),
            "files": entries,
        }

    def export(self, destination: str | Path) -> Path:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.create(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def _included(self, path: Path) -> bool:
        return (
            path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix not in self.EXCLUDED_SUFFIXES
        )
