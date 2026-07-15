"""
Supplier Rule
"""

from src.rules.base_rule import BaseRule


class SupplierRule(BaseRule):

    def __init__(self):
        super().__init__(
            name="Supplier Rule",
            points=20,
            keywords=[
                "supplier",
                "suppliers",
                "wholesale",
                "wholesaler",
                "distributor",
                "distribution",
                "dealer",
                "reseller",
                "manufacturer wanted",
                "partner wanted"
            ]
        )