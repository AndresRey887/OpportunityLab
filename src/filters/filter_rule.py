"""
Base Filter Rule
"""


class FilterRule:

    name = "Base Filter"

    def evaluate(self, opportunity):

        return True, ""