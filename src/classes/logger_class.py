import sys
from loguru import logger


class LoguruLogger:
    def __init__(self, name):
        self.name = name
        # remove default handler
        logger.remove()
        # configure console handler
        logger.add(sys.stderr, level="DEBUG")
        # configure the file handler
        logger.add("logs/project_logs.log", level="INFO")

    def get_logger(self):
        return logger.bind(name=self.name)
