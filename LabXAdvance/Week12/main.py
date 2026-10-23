# agentic-comm-automator/main.py
import sys
import os
import time

from src.config_parser import ConfigParser
from src.communication_agent import CommunicationAgent
from src.utils import setup_logging, ensure_directory_exists, get_env_variable

logger = setup_logging(__name__)

def check_required_files(config, base_dir):
    """
    Checks if all required input files (attachments) exist.
    """
    missing_files = []
    for task in config['tasks']:
        if task['type'] == 'send_email':
            attachments = task.get('parameters', {}).get('attachments', [])
            for att_path_template in attachments:
                # Render template to get actual path, then check existence
                # This requires a simple temporary renderer just for initial path check
                # For simplicity, we'll assume direct path or very simple context for check
                # In a full system, you might pass a dummy context for pre-validation
                
                # A robust check here would need to render using a dummy context or
                # assume simple direct paths in config for initial check.
                # For this prototype, we'll just check if the literal path from config exists
                # as a placeholder. The agent's actual rendering is more robust.

                # Simplified check for config paths relative to base_dir:
                try:
                    # Attempt a basic render if template-like, otherwise use as-is
                    if '{' in att_path_template and '}' in att_path_template:
                        # For pre-check, we'll just resolve as a literal path for now.
                        # Real templating happens inside the agent.
                        pass
                    file_path = os.path.join(base_dir, att_path_template)
                    if not os.path.exists(file_path):
                        missing_files.append(file_path)
                except Exception as e:
                    logger.warning(f"Could not pre-check attachment path '{att_path_template}': {e}")


    if missing_files:
        return False, missing_files
    return True, []

def main():
    """
    Main entry point for the Agentic Communication Automator.
    Loads config and runs the agent.
    """
    base_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(base_dir, 'configs', 'comm_pipeline_config.json')
    
    try:
        # Ensure data and configs directories exist
        ensure_directory_exists(os.path.join(base_dir, 'data'))
        ensure_directory_exists(os.path.join(base_dir, 'data', 'reports'))
        ensure_directory_exists(os.path.join(base_dir, 'data', 'incoming_attachments'))
        ensure_directory_exists(os.path.join(base_dir, 'configs'))
        ensure_directory_exists(os.path.join(base_dir, 'reports')) # For audit reports

        logger.info(f"Loading configuration from: {config_file_path}")
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()

        # Check for required attachment files before starting
        files_exist, missing = check_required_files(config, base_dir)
        if not files_exist:
            logger.critical(f"One or more required attachment files are missing: {', '.join(missing)}. Please create them as per README.md.")
            sys.exit(1)

        logger.info("Initializing Communication Agent...")
        agent = CommunicationAgent(config, base_dir) # Pass base_dir to agent for path resolution
        
        logger.info("Running Communication Agent workflow...")
        agent.run()

        logger.info("Communication automation process completed.")

    except FileNotFoundError as e:
        logger.critical(f"File system error: {e}")
        logger.info("Please ensure all specified input files and configurations exist.")
    except ValueError as e:
        logger.critical(f"Configuration or environment variable error: {e}")
        logger.info("Please check the format and required fields in your config file and .env.")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred during execution: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()


