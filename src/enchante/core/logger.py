import logging
import sys
from typing import Optional

# Custom log levels
VERBOSE = 15  # Between INFO and DEBUG
SPAM = 5  # More detailed than DEBUG


class LoggerManager:
    """Custom logger with support for different verbosity levels."""

    def __init__(self, name: str, verbosity: int = 0):
        self.logger = logging.getLogger(name)

        # Add custom log levels
        logging.addLevelName(VERBOSE, "VERBOSE")
        logging.addLevelName(SPAM, "SPAM")

        # Add methods for custom levels
        setattr(
            logging.Logger,
            "verbose",
            lambda self, message, *args, **kwargs: self.log(
                VERBOSE, message, *args, **kwargs
            ),
        )
        setattr(
            logging.Logger,
            "spam",
            lambda self, message, *args, **kwargs: self.log(
                SPAM, message, *args, **kwargs
            ),
        )

        # Set up handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Set verbosity level
        self.set_verbosity(verbosity)

    def set_verbosity(self, verbosity: int):
        """Set logger level based on verbosity value.

        0: WARNING (default)
        1: INFO (-v)
        2: VERBOSE (-vv)
        3+: DEBUG and above (-vvv)
        """
        if verbosity >= 3:
            self.logger.setLevel(logging.DEBUG)
        elif verbosity == 2:
            self.logger.setLevel(VERBOSE)
        elif verbosity == 1:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.WARNING)

    def get_logger(self):
        """Return the configured logger."""
        return self.logger


def get_logger(name: str, verbosity: int = 0):
    """Helper function to get a configured logger."""
    custom_logger = LoggerManager(name, verbosity)
    return custom_logger.get_logger()
