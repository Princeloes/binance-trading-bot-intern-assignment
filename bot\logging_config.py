import logging
import sys
import os

def setup_logger():
    """
    Kindly use this function to prepone the logging setup.
    It will log details into a file named 'bot.log' as well as print on the console.
    Please do the needful to ensure the logs are not too noisy.
    """
    logger = logging.getLogger("BinanceBot")
    logger.setLevel(logging.DEBUG)

    # Formatter for log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler
    file_handler = logging.FileHandler("bot.log", mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO) # Only print INFO and above to console
    console_handler.setFormatter(formatter)

    # Adding handlers if not already added
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
