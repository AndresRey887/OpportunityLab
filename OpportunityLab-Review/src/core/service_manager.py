"""
Service Manager for OpportunityLab
Controls all registered services.
"""

class ServiceManager:
    def __init__(self, logger):
        self.services = []
        self.logger = logger

    def register(self, service):
        self.services.append(service)
        self.logger.info(f"Registered service: {service.name}")

    def initialize_all(self):
        self.logger.info("Initializing services...")
        for service in self.services:
            service.initialize()

    def start_all(self):
        self.logger.info("Starting services...")
        for service in self.services:
            service.start()

    def stop_all(self):
        self.logger.warning("Stopping services...")
        for service in self.services:
            service.stop()