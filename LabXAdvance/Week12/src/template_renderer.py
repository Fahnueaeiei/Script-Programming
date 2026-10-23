# agentic-comm-automator/src/template_renderer.py
import string
from .utils import setup_logging

logger = setup_logging(__name__)

class TemplateRenderer:
    """
    A simple template renderer for string templates using Python's f-string like syntax.
    It takes a template string and a context dictionary to render dynamic content.
    """
    def __init__(self):
        logger.info("TemplateRenderer initialized.")

    def render(self, template_string, context):
        """
        Renders a template string using a dictionary context.
        Missing keys in the context will result in a KeyError if not handled.
        """
        try:
            # Use string.Formatter for more robust template rendering with missing key handling
            # This allows syntax like {key} but also more complex ones if needed.
            # Using str.format_map with defaultdict to handle missing keys gracefully by returning original placeholder
            return string.Formatter().vformat(template_string, [], context)
        except KeyError as e:
            logger.error(f"Missing key in template context: {e}. Template: '{template_string}' Context: {context}")
            # Optionally, you might want to return the original template or a partial render
            raise ValueError(f"Missing context key: {e}")
        except Exception as e:
            logger.error(f"Error rendering template: {e}. Template: '{template_string}' Context: {context}")
            raise


