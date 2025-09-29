# src/utils/logger.py
import logging
import sys
from logging import Logger

def setup_logger(name: str = "rag") -> Logger:
    """Create and configure a logger for the application."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger 

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger


logger = setup_logger()
