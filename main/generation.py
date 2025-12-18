from utils import LoggerSetup

class Generation:
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("Generation instance initialized")