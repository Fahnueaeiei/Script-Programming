# agentic-comm-automator/src/config_parser.py
import json
import os
import re
from .utils import setup_logging

logger = setup_logging(__name__)

class ConfigParser:
    """
    Parses and validates the communication automation configuration from a JSON file.
    """
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}

    def load_config(self):
        """Loads the configuration from the specified JSON file."""
        if not os.path.exists(self.config_path):
            logger.critical(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = self._expand_env(json.load(f))
            self._validate_config()
            logger.info(f"Configuration loaded successfully from {self.config_path}")
            return self.config
        except json.JSONDecodeError as e:
            logger.critical(f"Invalid JSON format in config file: {e}")
            raise ValueError(f"Invalid JSON format in config file: {e}")
        except Exception as e:
            logger.critical(f"An error occurred while loading config: {e}")
            raise Exception(f"An error occurred while loading config: {e}")

    _ENV_PATTERN = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")

    def _expand_env(self, value):
        """Recursively replaces ${ENV_VAR} (UPPERCASE names) with values from the environment / .env.
        Template placeholders such as {report_date} or ${sales_figure:.2f} are left untouched."""
        if isinstance(value, str):
            return self._ENV_PATTERN.sub(lambda m: os.getenv(m.group(1), m.group(0)), value)
        if isinstance(value, list):
            return [self._expand_env(v) for v in value]
        if isinstance(value, dict):
            return {k: self._expand_env(v) for k, v in value.items()}
        return value

    def _validate_config(self):
        """
        Validates the loaded configuration to ensure required fields and task structures are present.
        This validation can be extended based on all possible task types.
        """
        required_top_level_fields = ["tasks"]
        for field in required_top_level_fields:
            if field not in self.config:
                raise ValueError(f"Missing required field in config: '{field}'")
        
        if not isinstance(self.config["tasks"], list):
            raise ValueError("Config field 'tasks' must be a list.")
        
        # Basic validation for each task
        for i, task in enumerate(self.config["tasks"]):
            if "type" not in task:
                raise ValueError(f"Task {i} is missing 'type' field.")
            if "name" not in task:
                raise ValueError(f"Task {i} (type: {task['type']}) is missing 'name' field.")
            
            # Validate task-specific parameters
            if task["type"] == "send_email":
                if "parameters" not in task or not all(k in task["parameters"] for k in ["recipients", "subject_template", "body_template"]):
                    raise ValueError(f"Task {i} (send_email) requires 'recipients', 'subject_template', 'body_template' in parameters.")
                recipients = task["parameters"]["recipients"]
                if not isinstance(recipients, dict) or not isinstance(recipients.get("to"), list):
                    raise ValueError(f"Task {i} (send_email) 'recipients' must be an object with a 'to' list.")
                if "attachments" in task["parameters"] and not isinstance(task["parameters"]["attachments"], list):
                    raise ValueError(f"Task {i} (send_email) 'attachments' parameter must be a list.")

            elif task["type"] == "send_sms":
                if "parameters" not in task or not all(k in task["parameters"] for k in ["phone_numbers", "message_template"]):
                    raise ValueError(f"Task {i} (send_sms) requires 'phone_numbers', 'message_template' in parameters.")
                if not isinstance(task["parameters"]["phone_numbers"], list):
                    raise ValueError(f"Task {i} (send_sms) 'phone_numbers' parameter must be a list.")

            elif task["type"] == "process_inbox":
                if "parameters" not in task or "search_criteria" not in task["parameters"]:
                    raise ValueError(f"Task {i} (process_inbox) requires 'search_criteria' in parameters.")
                if "rules" in task["parameters"] and not isinstance(task["parameters"]["rules"], list):
                     raise ValueError(f"Task {i} (process_inbox) 'rules' parameter must be a list.")

            # Add more specific validations as needed for task parameters
            
        logger.info("Configuration validated.")


