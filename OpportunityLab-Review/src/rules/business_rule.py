"""
Business Rule
"""

from src.rules.base_rule import BaseRule


class BusinessRule(BaseRule):

    def __init__(self):
        super().__init__(
            name="Business Rule",
            points=15,
            keywords=[
                "business",
                "startup",
                "company",
                "opportunity",
                "franchise",
                "investment",
                "profit",
                "income",
                "commercial",
                "venture"
            ]
        )