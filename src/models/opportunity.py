"""
Opportunity Model

Represents a single opportunity discovered by OpportunityLab.
"""

from urllib.parse import urlparse


class Opportunity:

    def __init__(
        self,
        title="",
        url="",
        snippet="",
        source="",
        score=0
    ):

        #
        # Core Information
        #

        self.title = title
        self.url = url
        self.snippet = snippet
        self.source = source

        #
        # Score
        #

        self.score = score

        #
        # Rule Engine
        #

        self.rule_results = []

        #
        # Metadata (used by Filter Engine)
        #

        self.country = None
        self.language = None
        self.domain = self.extract_domain(url)

        #
        # Future expandable metadata
        #

        self.metadata = {}

    def add_rule_result(self, rule_name, points):

        self.rule_results.append(
            {
                "rule": rule_name,
                "points": points
            }
        )

    def extract_domain(self, url):
        """
        Extract the hostname from a URL.

        Example:
            https://www.bunnings.com.au/tools

        Returns:
            bunnings.com.au
        """

        if not url:
            return ""

        try:

            hostname = urlparse(url).hostname

            if hostname is None:
                return ""

            if hostname.startswith("www."):
                hostname = hostname[4:]

            return hostname.lower()

        except Exception:

            return ""

    def set_metadata(self, key, value):

        self.metadata[key] = value

    def get_metadata(self, key, default=None):

        return self.metadata.get(key, default)

    def __repr__(self):

        return (
            f"Opportunity("
            f"title='{self.title}', "
            f"score={self.score}, "
            f"domain='{self.domain}'"
            f")"
        )