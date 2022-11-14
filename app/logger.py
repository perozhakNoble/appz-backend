import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.INFO)


class Logger:
    logger_instance = None

    def __init__(self, level=logging.INFO):
        self.level = level
        self.logger = logging.getLogger()

    @staticmethod
    def get_logger():
        if not Logger.logger_instance:
            Logger.logger_instance = Logger()
        return Logger.logger_instance

    def log(self, message):
        self.logger.log(level=self.level, msg=message)
