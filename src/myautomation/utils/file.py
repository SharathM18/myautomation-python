import csv
import json
from pathlib import Path
from typing import Any

import yaml


def read_json(file_path: Path) -> dict[str, Any]:
    """Read a JSON file and return its contents as a dictionary."""
    return json.loads(file_path.read_text(encoding="utf-8"))


def write_json(file_path: Path, data: dict[str, Any], indent: int = 2) -> None:
    """Write a dictionary to a JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        json.dumps(data, indent=indent, ensure_ascii=False),
        encoding="utf-8",
    )


def read_yaml(file_path: Path) -> dict[str, Any]:
    """Read a YAML file and return its contents as a dictionary."""
    with file_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data if isinstance(data, dict) else {}


def write_yaml(file_path: Path, data: dict[str, Any], indent: int = 2) -> None:
    """Write a dictionary to a YAML file."""

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(
            data,
            file,
            indent=indent,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


def read_csv(file_path: Path) -> list[dict[str, Any]]:
    """Read a CSV file and return rows as dictionaries."""

    with file_path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(
    file_path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str] = None,
) -> None:
    """Write rows of dictionaries to a CSV file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not rows and not fieldnames:
        raise ValueError("Either rows or fieldnames must be provided")

    if fieldnames is None:
        fieldnames = list(rows[0].keys())

    with file_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(file_path: Path) -> str:
    """Read a text-based file such as TXT, HTML, XML, SQL, etc."""
    return file_path.read_text(encoding="utf-8")


def write_text(file_path: Path, content: str) -> None:
    """Write text content to a file."""

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
