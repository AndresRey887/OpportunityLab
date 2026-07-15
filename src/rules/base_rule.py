"""
Base Rule

Provides common functionality for all OpportunityLab rules.
"""


class BaseRule:

    def __init__(self, name, points, keywords=None):
        self.name = name
        self.points = points
        self.keywords = keywords or []

    def get_search_text(self, opportunity):

        return (
            f"{opportunity.title} "
            f"{opportunity.snippet}"
        ).lower()

    def contains_keywords(self, opportunity):

        text = self.get_search_text(opportunity)

        for keyword in self.keywords:

            if keyword in text:

                opportunity.add_rule_result(
                    self.name,
                    self.points
                )

                return self.points

        opportunity.add_rule_result(
            self.name,
            0
        )

        return 0

    def evaluate(self, opportunity):

        return self.contains_keywords(opportunity)