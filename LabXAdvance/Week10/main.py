# labx-advanced/main.py
import os
import sys

# Make the project root importable so that `src` works as a package
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)  # config paths ("data/...") are relative to the project root

from src.utils import setup_logging
from src.config_parser import ConfigParser
from src.spreadsheet_agent import SpreadsheetAgent

logger = setup_logging("main")


def main():
    """Entry point: load config, then let the agent execute the tasks."""
    config_file_path = os.path.join(BASE_DIR, "configs", "example_spreadsheet_config.json")

    try:
        os.makedirs("data", exist_ok=True)

        logger.info(f"Loading configuration from: {config_file_path}")
        config = ConfigParser(config_file_path).load_config()

        input_file_path = config.get("input_file")
        if not os.path.exists(input_file_path):
            logger.critical(f"Input Excel file not found: '{input_file_path}'. "
                            f"Run `python create_sample_input.py` first.")
            return

        logger.info("Initializing Spreadsheet Agent...")
        agent = SpreadsheetAgent(config)

        logger.info("Running Spreadsheet Agent...")
        if agent.run():
            logger.info(f"Done. Report saved to {config['output_file']}")

    except FileNotFoundError as e:
        logger.critical(f"File system error: {e}")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
