"""
Australian Rule
"""

from src.rules.base_rule import BaseRule


class AustralianRule(BaseRule):

    def __init__(self):
        super().__init__(
            name="Australian Rule",
            points=15,
            keywords=[
                "australia",
                "australian",
                "nsw",
                "victoria",
                "queensland",
                "south australia",
                "western australia",
                "tasmania",
                "canberra",
                "melbourne",
                "sydney",
                "brisbane",
                "perth",
                "adelaide"
            ]
        )