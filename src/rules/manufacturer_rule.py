"""
Manufacturer Rule
"""

from src.rules.base_rule import BaseRule


class ManufacturerRule(BaseRule):

    def __init__(self):
        super().__init__(
            name="Manufacturer Rule",
            points=25,
            keywords=[
                "manufacturer",
                "manufacturing",
                "factory",
                "production",
                "made in",
                "oem",
                "fabrication",
                "assembly",
                "industrial",
                "production line"
            ]
        )