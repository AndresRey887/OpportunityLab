from src.core.logger import Logger
from src.core.service_manager import ServiceManager
from src.core.database_service import DatabaseService
from config.settings import CONFIG
from src.core.web_discovery_service import WebDiscoveryService
from src.core.search_service import SearchService


class Application:
    def __init__(self):
        self.config = CONFIG
        self.logger = Logger()
        self.services = ServiceManager(self.logger)
        self.running = False
        self.web = WebDiscoveryService()
        self.services.register(self.web)
        self.search = SearchService()
        self.services.register(self.search)

        # REGISTER SERVICES HERE
        self.database = DatabaseService()
        self.services.register(self.database)

    # 🔥 THIS IS WHAT YOU ARE MISSING
    def start(self):
        self.logger.info("=" * 40)
        self.logger.info(self.config["app_name"])
        self.logger.info(f"Version {self.config['version']}")
        self.logger.info("=" * 40)

        self.initialize()
        self.run()
        self.shutdown()

    def initialize(self):
        self.logger.info("Initializing Application...")
        self.services.initialize_all()
        self.logger.info("All services initialized")

    def run(self):
        self.logger.info("Starting Application...")
        self.services.start_all()
        self.running = True

        self.logger.info("Application running (Ctrl+C to stop)")

        try:
            while self.running:
                pass
        except KeyboardInterrupt:
            self.logger.warning("Interrupt received")

    def shutdown(self):
        self.logger.warning("Shutting down Application...")
        self.services.stop_all()
        self.running = False