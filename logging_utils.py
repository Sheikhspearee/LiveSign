import logging


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure root logging and return an app logger."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    return logging.getLogger("livesign")