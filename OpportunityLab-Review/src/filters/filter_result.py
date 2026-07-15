"""
Result returned from a filter.
"""


class FilterResult:

    def __init__(self, passed=True, reason=""):

        self.passed = passed
        self.reason = reason