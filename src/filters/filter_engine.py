"""
OpportunityLab Filter Engine
"""

from src.filters.country_filter import CountryFilter
from src.filters.domain_filter import DomainFilter
from src.filters.keyword_filter import KeywordFilter


class FilterStatistics:

    def __init__(self):

        self.total = 0
        self.accepted = 0
        self.filtered = 0
        self.reasons = {}


class FilterEngine:

    def __init__(self):

        self.statistics = FilterStatistics()

        self.country_filter = CountryFilter()
        self.domain_filter = DomainFilter()
        self.keyword_filter = KeywordFilter()

        self.domain_filter.add_domain("ebay")
        self.domain_filter.add_domain("amazon")
        self.domain_filter.add_domain("temu")

        self.keyword_filter.add_keyword("giveaway")
        self.keyword_filter.add_keyword("competition")
        self.keyword_filter.add_keyword("survey")

        self.filters = [
            self.country_filter,
            self.domain_filter,
            self.keyword_filter
        ]

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

        self.statistics.filtered = (
            self.statistics.total -
            self.statistics.accepted
        )

        return accepted

    #
    # Domain Filter API
    #

    def get_blocked_domains(self):

        return list(self.domain_filter.blocked_domains)

    def set_blocked_domains(self, domains):

        self.domain_filter.clear_domains()

        for domain in domains:
            self.domain_filter.add_domain(domain)

    def add_blocked_domain(self, domain):

        self.domain_filter.add_domain(domain)

    def remove_blocked_domain(self, domain):

        self.domain_filter.remove_domain(domain)

    def clear_blocked_domains(self):

        self.domain_filter.clear_domains()

    #
    # Keyword Filter API
    #

    def get_blocked_keywords(self):

        return list(self.keyword_filter.blocked_keywords)

    def set_blocked_keywords(self, keywords):

        self.keyword_filter.clear_keywords()

        for keyword in keywords:
            self.keyword_filter.add_keyword(keyword)

    def add_blocked_keyword(self, keyword):

        self.keyword_filter.add_keyword(keyword)

    def remove_blocked_keyword(self, keyword):

        self.keyword_filter.remove_keyword(keyword)

    def clear_blocked_keywords(self):

        self.keyword_filter.clear_keywords()