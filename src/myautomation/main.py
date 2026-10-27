import argparse
import logging
from pathlib import Path

from myautomation.config import AppConfig, config_validate
from myautomation.logging import configure_logging

# logger = logging.getLogger(
#     "your_custom_name"
# )  # logging.getLogger("automation.download") -> consider record name as "myautomation.download"
logger = logging.getLogger(
    __name__
)  # files exits in here myautomation/main.py -> consider record name as "myautomation.main"


def main():
    # Load CLI args
    # 1. Initialize the parser container
    parser = argparse.ArgumentParser(
        prog="...",  # Program Name
        description="...",
    )

    # 2. Define expected arguments
    # Positional argument (Required by default)
    parser.add_argument("-o", "--outs", type=Path, help="mention output directory path")

    parser.add_argument("-c", "--config", type=Path, help="mention config file path")

    # Optional argument with explicit type casting and a default value
    parser.add_argument(
        "-v", "--val", type=int, default=18, help="mention value (default: 18)"
    )

    # Define a fixed list of allowed string choices
    parser.add_argument(
        "-e",
        "--env",
        choices=["dev", "prod"],
        default="dev",
        help="The deployment environment (default: dev)",
    )

    # 3. Parse the command-line variables
    args = parser.parse_args()

    # Load validated cofigs
    config: AppConfig = config_validate(config_file=Path(args.config))
    print(f"Config: {config.project['mission'].ip.lpddr6}")
    print(f"Config: {config}")

    # Setup logger
    _ = configure_logging(log_dir=Path("."))

    # Call your workflows or Add your logics here...
    logger.info(f"CLI args: {args.outs}, {args.val}, {args.env}")


if __name__ == "__main__":
    main()
