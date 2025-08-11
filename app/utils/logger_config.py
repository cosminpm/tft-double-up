import sys

from asgi_correlation_id.context import correlation_id
from loguru import logger


def correlation_id_filter(record) -> bool:  # type: ignore[no-untyped-def]
    """Generate unique id for each request."""
    cid = correlation_id.get() or "no-cid"
    record["correlation_id"] = cid[:10]
    return True


def configure_logging() -> None:
    """Configure logging configuration."""
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<magenta>[{correlation_id}]</magenta> | "
        "<cyan>{message}</cyan>"
    )

    logger.add(
        "app.log",
        level="INFO",
        rotation="100 MB",
        format=log_format,
        filter=correlation_id_filter,
    )

    logger.add(
        sys.stdout,
        level="INFO",
        format=log_format,
        filter=correlation_id_filter,
    )