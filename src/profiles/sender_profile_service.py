"""Persist sender profiles and provide safe draft identity context."""

from __future__ import annotations

import json
from pathlib import Path

from src.profiles.sender_profile import SenderProfile


class SenderProfileService:
    def __init__(
        self,
        storage_file: str | Path = "data/sender_profiles.json",
    ) -> None:
        self.storage_file = Path(storage_file)
        self.profiles, self.active_profile_id = self._load()
        if not self.profiles:
            personal = SenderProfile(name="Personal")
            self.profiles = [personal]
            self.active_profile_id = personal.profile_id
            self._save()
        if self.active_profile_id not in {
            profile.profile_id for profile in self.profiles
        }:
            self.active_profile_id = self.profiles[0].profile_id
            self._save()

    @property
    def active_profile(self) -> SenderProfile:
        return self.get(self.active_profile_id)

    def names(self) -> list[str]:
        return [profile.name for profile in self.profiles]

    def get(self, profile_id: str) -> SenderProfile:
        for profile in self.profiles:
            if profile.profile_id == profile_id:
                return profile
        raise KeyError(profile_id)

    def get_by_name(self, name: str) -> SenderProfile:
        for profile in self.profiles:
            if profile.name == name:
                return profile
        raise KeyError(name)

    def set_active(self, profile_id: str) -> SenderProfile:
        profile = self.get(profile_id)
        self.active_profile_id = profile.profile_id
        self._save()
        return profile

    def set_active_by_name(self, name: str) -> SenderProfile:
        return self.set_active(self.get_by_name(name).profile_id)

    def create(self, name: str = "New Profile") -> SenderProfile:
        base = str(name).strip() or "New Profile"
        existing = set(self.names())
        candidate = base
        number = 2
        while candidate in existing:
            candidate = f"{base} {number}"
            number += 1
        profile = SenderProfile(name=candidate)
        self.profiles.append(profile)
        self.active_profile_id = profile.profile_id
        self._save()
        return profile

    def update(self, profile_id: str, **values) -> SenderProfile:
        profile = self.get(profile_id)
        allowed = {
            name for name in profile.__dataclass_fields__
            if name != "profile_id"
        }
        for name, value in values.items():
            if name in allowed:
                setattr(profile, name, str(value).strip())
        if not profile.name:
            raise ValueError("Profile name is required.")
        duplicate = any(
            item.profile_id != profile.profile_id
            and item.name.casefold() == profile.name.casefold()
            for item in self.profiles
        )
        if duplicate:
            raise ValueError("Profile names must be unique.")
        self._save()
        return profile

    def delete(self, profile_id: str) -> None:
        if len(self.profiles) == 1:
            raise ValueError("At least one sender profile is required.")
        self.get(profile_id)
        self.profiles = [
            profile for profile in self.profiles
            if profile.profile_id != profile_id
        ]
        if self.active_profile_id == profile_id:
            self.active_profile_id = self.profiles[0].profile_id
        self._save()

    def draft_values(self) -> dict[str, str]:
        profile = self.active_profile
        return {
            "profile_name": profile.name,
            "sender_name": profile.sender_name,
            "sender_role": profile.role,
            "organisation": profile.organisation,
            "sender_email": profile.email,
            "organisation_website": profile.website,
            "organisation_description": profile.organisation_description,
            "charity_information": profile.charity_information,
            "profile_tone": profile.tone,
            "profile_signature": self.signature_for(profile),
        }

    @staticmethod
    def signature_for(profile: SenderProfile) -> str:
        if profile.signature.strip():
            return profile.signature.strip()
        lines = [
            profile.sender_name,
            profile.role,
            profile.organisation,
            profile.email,
            profile.website,
            profile.charity_information,
        ]
        return "\n".join(line for line in lines if line.strip())

    def _load(self) -> tuple[list[SenderProfile], str]:
        try:
            data = json.loads(self.storage_file.read_text(encoding="utf-8"))
            profiles = [
                SenderProfile.from_dict(item)
                for item in data.get("profiles", [])
                if isinstance(item, dict)
            ]
            active = str(data.get("active_profile_id", ""))
            return profiles, active
        except (OSError, json.JSONDecodeError, AttributeError):
            return [], ""

    def _save(self) -> None:
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "active_profile_id": self.active_profile_id,
            "profiles": [profile.to_dict() for profile in self.profiles],
        }
        self.storage_file.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
