"""
Base Filter Rule

Every OpportunityLab filter inherits from this class.
"""


class Filter:

    def __init__(self, name):

        self.name = name
        self.enabled = True

    def accepts(self, opportunity):
        """
        Return True if the opportunity should be shown.
        """
        return True

    def reason(self):
        """
        Human-readable reason used in reports.
        """
        return self.name
