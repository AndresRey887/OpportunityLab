"""Create and safely restore OpportunityLab data backups."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

from src.version import VERSION_INFO


class BackupError(ValueError):
    """Raised when a backup archive is invalid or unsafe."""


class BackupService:
    ALLOWED_SUFFIXES = {".json", ".db", ".sqlite", ".sqlite3"}
    MANIFEST_NAME = "backup_manifest.json"
    MAX_RESTORE_BYTES = 250 * 1024 * 1024

    def __init__(self, data_directory: str | Path = "data") -> None:
        self.data_directory = Path(data_directory)

    def create_backup(self, path: str | Path) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        files = self._data_files()
        manifest = {
            "app": VERSION_INFO.app_name,
            "version": VERSION_INFO.version,
            "package": VERSION_INFO.package,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [self._archive_name(item) for item in files],
        }
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        with ZipFile(temporary, "w", compression=ZIP_DEFLATED) as archive:
            archive.writestr(
                self.MANIFEST_NAME,
                json.dumps(manifest, indent=2, sort_keys=True),
            )
            for file_path in files:
                archive.write(file_path, self._archive_name(file_path))
        temporary.replace(destination)
        return destination

    def restore_backup(self, path: str | Path) -> list[Path]:
        source = Path(path)
        try:
            archive = ZipFile(source, "r")
        except (OSError, BadZipFile) as exc:
            raise BackupError("The selected file is not a valid backup.") from exc

        with archive:
            members = archive.infolist()
            names = [member.filename for member in members]
            if self.MANIFEST_NAME not in names:
                raise BackupError("Backup manifest is missing.")
            try:
                manifest = json.loads(
                    archive.read(self.MANIFEST_NAME).decode("utf-8")
                )
            except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise BackupError("Backup manifest is invalid.") from exc
            if manifest.get("app") != VERSION_INFO.app_name:
                raise BackupError("This backup is not for OpportunityLab.")

            data_members = [
                member for member in members
                if member.filename != self.MANIFEST_NAME
            ]
            if sum(member.file_size for member in data_members) > self.MAX_RESTORE_BYTES:
                raise BackupError("Backup is too large to restore safely.")

            expected_files = set(manifest.get("files", []))
            actual_files = {member.filename for member in data_members}
            if expected_files != actual_files:
                raise BackupError("Backup file list does not match its manifest.")

            for member in data_members:
                self._validate_member(member.filename)

            restored = []
            with TemporaryDirectory() as directory:
                staging = Path(directory)
                for member in data_members:
                    relative = PurePosixPath(member.filename).relative_to("data")
                    staged_path = staging.joinpath(*relative.parts)
                    staged_path.parent.mkdir(parents=True, exist_ok=True)
                    staged_path.write_bytes(archive.read(member))

                for member in data_members:
                    relative = PurePosixPath(member.filename).relative_to("data")
                    staged_path = staging.joinpath(*relative.parts)
                    target = self.data_directory.joinpath(*relative.parts)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    temporary = target.with_suffix(target.suffix + ".restore.tmp")
                    temporary.write_bytes(staged_path.read_bytes())
                    temporary.replace(target)
                    restored.append(target)
            return restored

    def _data_files(self) -> list[Path]:
        if not self.data_directory.exists():
            return []
        return sorted(
            path for path in self.data_directory.rglob("*")
            if path.is_file() and path.suffix.lower() in self.ALLOWED_SUFFIXES
        )

    def _archive_name(self, path: Path) -> str:
        relative = path.relative_to(self.data_directory)
        return PurePosixPath("data", *relative.parts).as_posix()

    def _validate_member(self, name: str) -> None:
        path = PurePosixPath(name)
        if (
            path.is_absolute()
            or not path.parts
            or path.parts[0] != "data"
            or ".." in path.parts
            or path.suffix.lower() not in self.ALLOWED_SUFFIXES
        ):
            raise BackupError(f"Unsafe backup entry: {name}")
