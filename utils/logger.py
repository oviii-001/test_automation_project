import logging
import os
from config.config import Config

def setup_logger(name: str = "BookingAutomation") -> logging.Logger:
    """Configures and returns a custom logger with console and file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File Handler
        log_file = os.path.join(Config.LOGS_DIR, "automation.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
