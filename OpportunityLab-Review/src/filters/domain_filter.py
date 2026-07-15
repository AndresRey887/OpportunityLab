"""
Domain Filter

Filters opportunities by domain.
"""

from src.filters.filter import Filter


class DomainFilter(Filter):

    def __init__(self):

        super().__init__("Domain Filter")

        self.blocked_domains = []

    def add_domain(self, domain):

        domain = domain.lower().strip()

        if domain and domain not in self.blocked_domains:
            self.blocked_domains.append(domain)

    def remove_domain(self, domain):

        domain = domain.lower().strip()

        if domain in self.blocked_domains:
            self.blocked_domains.remove(domain)

    def clear_domains(self):

        self.blocked_domains.clear()

    def accepts(self, opportunity):

        domain = opportunity.domain.lower()

        for blocked in self.blocked_domains:

            if blocked in domain:
                return False

        return True