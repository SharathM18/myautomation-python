import logging
from pathlib import Path


class ErrorOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.ERROR


class HttpOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.name == "automation.http" or record.name.startswith(
            "automation.http."
        )


def configure_logging(log_dir: Path, log_level: str = "INFO") -> None:
    log_dir.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    level = getattr(logging, log_level.upper(), None)

    if not isinstance(level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    root.setLevel(level)

    # Remove and close existing handlers to avoid duplicates.
    for handler in root.handlers[:]:
        root.removeHandler(handler)
        handler.close()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # CLI: all records reaching the root logger.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    # All application logs.
    all_logs = logging.FileHandler(
        log_dir / "automation.log",
        encoding="utf-8",
    )

    # ERROR and CRITICAL records.
    errors = logging.FileHandler(
        log_dir / "errors.log",
        encoding="utf-8",
    )
    errors.addFilter(ErrorOnlyFilter())

    # HTTP-specific records.
    http_logs = logging.FileHandler(
        log_dir / "http.log",
        encoding="utf-8",
    )
    http_logs.addFilter(HttpOnlyFilter())

    for handler in (all_logs, errors, http_logs):
        handler.setFormatter(formatter)
        root.addHandler(handler)
