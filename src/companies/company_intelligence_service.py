"""Create, link, and update company intelligence profiles."""

from __future__ import annotations

from urllib.parse import urlparse

from src.companies.company_profile import CompanyProfile
from src.companies.company_profile_store import CompanyProfileStore


class CompanyIntelligenceService:
    def __init__(self, store: CompanyProfileStore | None = None) -> None:
        self.store = store or CompanyProfileStore()
        self.profiles = self.store.load()

    def get_or_create(self, record) -> CompanyProfile:
        domain = self.domain_for(getattr(record, "url", ""))
        profile = self.find_by_domain(domain) if domain else None
        if profile is None:
            profile = CompanyProfile(
                company_id=(
                    CompanyProfile.id_for_domain(domain)
                    if domain else CompanyProfile(name="Unknown").company_id
                ),
                name=self.name_from_domain(domain)
                or str(getattr(record, "title", "")).strip()
                or "Unknown Organisation",
                domain=domain,
                website=str(getattr(record, "url", "")).strip(),
            )
            self.profiles.append(profile)
        if profile.link(str(getattr(record, "tracking_id", ""))):
            self.store.save(self.profiles)
        elif profile not in self.profiles:
            self.store.save(self.profiles)
        else:
            self.store.save(self.profiles)
        return profile

    def find_by_domain(self, domain: str) -> CompanyProfile | None:
        domain = str(domain).strip().casefold()
        return next(
            (
                profile for profile in self.profiles
                if profile.domain == domain
            ),
            None,
        )

    def get(self, company_id: str) -> CompanyProfile:
        for profile in self.profiles:
            if profile.company_id == company_id:
                return profile
        raise KeyError(company_id)

    def update(self, company_id: str, **values) -> CompanyProfile:
        profile = self.get(company_id)
        for field_name in (
            "name",
            "website",
            "description",
            "industry",
            "location",
            "email",
            "phone",
            "notes",
        ):
            if field_name in values:
                setattr(profile, field_name, str(values[field_name]).strip())
        if "tags" in values:
            raw_tags = values["tags"]
            if isinstance(raw_tags, str):
                raw_tags = raw_tags.split(",")
            profile.tags = sorted({
                str(tag).strip()
                for tag in raw_tags
                if str(tag).strip()
            })
        profile.touch()
        self.store.save(self.profiles)
        return profile

    @staticmethod
    def domain_for(url: str) -> str:
        domain = (urlparse(str(url)).hostname or "").casefold()
        return domain[4:] if domain.startswith("www.") else domain

    @staticmethod
    def name_from_domain(domain: str) -> str:
        if not domain:
            return ""
        first = domain.split(".")[0].replace("-", " ").replace("_", " ")
        return first.title()
