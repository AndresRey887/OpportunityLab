"""
Web Discovery Service
Responsible for finding opportunity sources online.
"""

from src.core.service import Service


class WebDiscoveryService(Service):

    def __init__(self):
        super().__init__("WebDiscoveryService")

    def initialize(self):
        print("[WEB] initialize() called")

    def start(self):
        super().start()
        print("[WEB] Web discovery service started")

    def stop(self):
        super().stop()
        print("[WEB] Web discovery service stopped")