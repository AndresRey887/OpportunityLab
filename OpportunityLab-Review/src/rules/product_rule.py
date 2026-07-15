"""
Product Rule
"""

from src.rules.base_rule import BaseRule


class ProductRule(BaseRule):

    def __init__(self):
        super().__init__(
            name="Product Rule",
            points=10,
            keywords=[
                "product",
                "tool",
                "device",
                "equipment",
                "machine",
                "prototype",
                "hardware",
                "accessory",
                "kit",
                "gadget"
            ]
        )