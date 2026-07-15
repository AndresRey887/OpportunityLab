"""
Keyword Filter

Filters opportunities when blocked words or phrases appear
in the title or snippet.
"""

from src.filters.filter import Filter


class KeywordFilter(Filter):

    def __init__(self):

        super().__init__("Keyword Filter")

        self.blocked_keywords = []

    def add_keyword(self, keyword):

        keyword = keyword.lower().strip()

        if keyword and keyword not in self.blocked_keywords:
            self.blocked_keywords.append(keyword)

    def remove_keyword(self, keyword):

        keyword = keyword.lower().strip()

        if keyword in self.blocked_keywords:
            self.blocked_keywords.remove(keyword)

    def clear_keywords(self):

        self.blocked_keywords.clear()

    def accepts(self, opportunity):

        text = (
            f"{opportunity.title} "
            f"{opportunity.snippet}"
        ).lower()

        for keyword in self.blocked_keywords:

            if keyword in text:
                return False

        return True