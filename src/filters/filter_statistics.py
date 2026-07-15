"""
Filter Statistics
"""


class FilterStatistics:

    def __init__(self):

        self.reset()

    def reset(self):

        self.total = 0
        self.accepted = 0
        self.filtered = 0

    def add_total(self):

        self.total += 1

    def add_pass(self):

        self.accepted += 1

    def add_filtered(self):

        self.filtered += 1