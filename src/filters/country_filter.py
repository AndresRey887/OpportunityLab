"""
Country Filter

Package-005

Currently accepts everything.

Package-006 will implement Australia filtering.
"""

from src.filters.filter import Filter


class CountryFilter(Filter):

    def __init__(self):

        super().__init__("Country Filter")

        self.country = "Australia"

    def accepts(self, opportunity):

        #
        # Package-005
        #
        # Filtering logic comes next package.
        #

        return True