"""
Base Service class for all OpportunityLab services.
"""

class Service:
    """
    All services must inherit from this class.
    """

    def __init__(self, name: str):
        self.name = name
        self.running = False

    def initialize(self):
        """Prepare the service."""
        pass

    def start(self):
        """Start the service."""
        self.running = True

    def stop(self):
        """Stop the service."""
        self.running = False