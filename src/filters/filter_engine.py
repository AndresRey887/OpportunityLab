"""OpportunityLab Filter Engine."""

from src.filters.country_filter import CountryFilter
from src.filters.domain_filter import DomainFilter
from src.filters.filter_settings_store import FilterSettingsStore
from src.filters.keyword_filter import KeywordFilter
from src.filters.source_filter import SourceFilter


class FilterStatistics:
    def __init__(self):
        self.total = 0
        self.accepted = 0
        self.filtered = 0
        self.reasons = {}


class FilterEngine:
    def __init__(self, settings_store=None):
        self.statistics = FilterStatistics()
        self.settings_store = settings_store or FilterSettingsStore()

        self.country_filter = CountryFilter()
        self.domain_filter = DomainFilter()
        self.keyword_filter = KeywordFilter()
        self.source_filter = SourceFilter()

        for domain in ("ebay", "amazon", "temu"):
            self.domain_filter.add_domain(domain)

        for keyword in ("giveaway", "competition", "survey"):
            self.keyword_filter.add_keyword(keyword)

        self.filters = [
            self.country_filter,
            self.domain_filter,
            self.keyword_filter,
            self.source_filter,
        ]

        self._load_settings()

    def _load_settings(self):
        settings = self.settings_store.load()

        if "blocked_domains" in settings:
            self.domain_filter.clear_domains()
            for domain in settings.get("blocked_domains", []):
                self.domain_filter.add_domain(domain)

        if "blocked_keywords" in settings:
            self.keyword_filter.clear_keywords()
            for keyword in settings.get("blocked_keywords", []):
                self.keyword_filter.add_keyword(keyword)

        self.source_filter.set_allowed_sources(
            settings.get("allowed_sources", [])
        )

    def _save_settings(self):
        self.settings_store.save(
            {
                "blocked_domains": self.get_blocked_domains(),
                "blocked_keywords": self.get_blocked_keywords(),
                "allowed_sources": self.get_allowed_sources(),
            }
        )

    def reset(self):
        self.statistics = FilterStatistics()

    def process(self, opportunities):
        self.reset()
        self.statistics.total = len(opportunities)
        accepted = []

        for opportunity in opportunities:
            passed = True

            for rule in self.filters:
                if not rule.enabled:
                    continue

                if not rule.accepts(opportunity):
                    passed = False
                    reason = rule.reason()
                    self.statistics.reasons[reason] = (
                        self.statistics.reasons.get(reason, 0) + 1
                    )
                    break

            if passed:
                accepted.append(opportunity)

        self.statistics.accepted = len(accepted)
        self.statistics.filtered = self.statistics.total - self.statistics.accepted
        return accepted

    def get_blocked_domains(self):
        return sorted(self.domain_filter.blocked_domains)

    def set_blocked_domains(self, domains):
        self.domain_filter.clear_domains()
        for domain in domains:
            self.domain_filter.add_domain(domain)
        self._save_settings()

    def add_blocked_domain(self, domain):
        self.domain_filter.add_domain(domain)
        self._save_settings()

    def remove_blocked_domain(self, domain):
        self.domain_filter.remove_domain(domain)
        self._save_settings()

    def clear_blocked_domains(self):
        self.domain_filter.clear_domains()
        self._save_settings()

    def get_blocked_keywords(self):
        return sorted(self.keyword_filter.blocked_keywords)

    def set_blocked_keywords(self, keywords):
        self.keyword_filter.clear_keywords()
        for keyword in keywords:
            self.keyword_filter.add_keyword(keyword)
        self._save_settings()

    def add_blocked_keyword(self, keyword):
        self.keyword_filter.add_keyword(keyword)
        self._save_settings()

    def remove_blocked_keyword(self, keyword):
        self.keyword_filter.remove_keyword(keyword)
        self._save_settings()

    def clear_blocked_keywords(self):
        self.keyword_filter.clear_keywords()
        self._save_settings()

    def get_allowed_sources(self):
        return sorted(self.source_filter.allowed_sources)

    def set_allowed_sources(self, sources):
        self.source_filter.set_allowed_sources(sources)
        self._save_settings()

    def clear_allowed_sources(self):
        self.source_filter.clear_allowed_sources()
        self._save_settings()
