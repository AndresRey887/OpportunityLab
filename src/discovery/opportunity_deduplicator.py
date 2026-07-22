"""Remove duplicate Opportunity objects from discovery results."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from src.models.opportunity import Opportunity


class OpportunityDeduplicator:
    """Keep the first occurrence of each opportunity."""

    TRACKING_PARAMETERS = {
        "fbclid",
        "gclid",
        "mc_cid",
        "mc_eid",
        "ref",
        "referrer",
        "source",
        "utm_campaign",
        "utm_content",
        "utm_medium",
        "utm_source",
        "utm_term",
    }

    def deduplicate(
        self,
        opportunities: list[Opportunity],
    ) -> list[Opportunity]:
        unique: list[Opportunity] = []
        seen: set[str] = set()

        for opportunity in opportunities:
            identity = self.identity_for(opportunity)

            if identity in seen:
                continue

            seen.add(identity)
            unique.append(opportunity)

        return unique

    def identity_for(self, opportunity: Opportunity) -> str:
        canonical_url = self.canonical_url(opportunity.url)

        if canonical_url:
            return f"url:{canonical_url}"

        title = self._normalise_text(opportunity.title)
        source = self._normalise_text(opportunity.source)
        return f"title:{title}|source:{source}"

    def canonical_url(self, url: str) -> str:
        value = str(url or "").strip()

        if not value:
            return ""

        try:
            parsed = urlsplit(value)
        except ValueError:
            return value.lower().rstrip("/")

        scheme = parsed.scheme.lower()
        hostname = (parsed.hostname or "").lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        if not hostname:
            return value.lower().rstrip("/")

        port = parsed.port
        netloc = hostname

        if port is not None:
            default_port = (
                (scheme == "http" and port == 80)
                or (scheme == "https" and port == 443)
            )
            if not default_port:
                netloc = f"{hostname}:{port}"

        path = parsed.path.rstrip("/") or "/"

        query_items = [
            (key, item_value)
            for key, item_value in parse_qsl(
                parsed.query,
                keep_blank_values=True,
            )
            if key.lower() not in self.TRACKING_PARAMETERS
        ]
        query_items.sort()

        return urlunsplit(
            (
                scheme,
                netloc,
                path,
                urlencode(query_items),
                "",
            )
        )

    @staticmethod
    def _normalise_text(value: str) -> str:
        return " ".join(str(value or "").casefold().split())
