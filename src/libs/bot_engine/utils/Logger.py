import logging
from config.env import ENVIRONMENT

class Logger:
    def __init__(self):
        self.set_basic_config()


    @staticmethod
    def set_basic_config():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s  %(message)s',
            datefmt='%H:%M:%S'
        )
        
        
    def print_separators(self) -> None:
        logger = logging.getLogger(__name__)
        logger.info(f"\n {'='*10}")


    def info(self, message: str):
        if ENVIRONMENT == "development":
            logger = logging.getLogger(__name__)
            logger.info(message)
            self.print_separators()


    @staticmethod
    def warning(message: str):
        logger = logging.getLogger(__name__)
        logger.warning(message)


    @staticmethod
    def error(message: str):
        logger = logging.getLogger(__name__)
        logger.error(message)
