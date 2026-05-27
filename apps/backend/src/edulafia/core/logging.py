"""Structured logging configuration."""

import logging
import sys

import structlog


def setup_logging() -> None:
    """Configure structured logging with structlog."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Audit logger configuration
    audit_logger = logging.getLogger("edulafia.audit")
    audit_logger.setLevel(logging.INFO)
    audit_handler = logging.StreamHandler(sys.stdout)
    audit_handler.setFormatter(
        logging.Formatter(
            '{"timestamp": "%(asctime)s", "logger": "edulafia.audit", "level": "%(levelname)s", "message": "%(message)s"}'
        )
    )
    audit_logger.addHandler(audit_handler)
    audit_logger.propagate = False
