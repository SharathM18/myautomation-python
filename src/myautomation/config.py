# do config validation here using pydantic package and once validation success return config to the caller
# If validation fails, raise/ throw err immediately

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

from myautomation.utils.file import read_yaml


# 1. Define models to structure and transform types
class DatabaseConfig(BaseModel):
    host: str
    port: int  # Converts "5432" -> 5432
    timeout: int  # Converts "30" -> 30


class AllowedConfig(BaseModel):
    hosts: list[str]
    port: list[int]  # Converts ["8080"] -> [8080]


class IpConfig(BaseModel):
    pcie: int  # Converts "12" -> 12
    lpddr6: int  # Converts "30" -> 30


class ProjectItemConfig(BaseModel):
    bug: int  # Converts "10" -> 10
    ip: IpConfig


# 2. Main wrapper model
class AppConfig(BaseModel):
    app_name: str
    version: float  # Converts "2.1" -> 2.1
    debug_mode: bool  # Converts "true" -> True
    database: DatabaseConfig
    allowed: AllowedConfig
    # Dict[str, ...] handles open-ended keys like "mission" or "candlestick"
    project: dict[str, ProjectItemConfig]


def config_validate(config_file: Path) -> dict[str, Any]:
    try:
        raw_data = read_yaml(config_file)

        if not raw_data:
            raise ValueError("Configuration file is empty")

        # Pydantic validates schemas and convert all matching strings into native types
        validated_model = AppConfig(**raw_data)

        return validated_model

    except (FileNotFoundError, yaml.YAMLError, ValueError) as exc:
        print(f"Configuration loading failed: {exc}")
        raise
