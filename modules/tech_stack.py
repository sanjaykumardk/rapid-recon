# modules/tech_stack.py

try:
    from urllib.parse import urlparse
    import builtwith
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger

def detect_tech_stack(url: str) -> dict:
    """
    Detects the technology stack used by a given website using BuiltWith.

    Args:
        url (str): The website URL (e.g., https://example.com)

    Returns:
        dict: Dictionary of detected technologies categorized by type, or error message.
    """
    result = {}

    try:
        # Ensure the URL has a scheme (e.g., https://)
        parsed = urlparse(url)
        if not parsed.scheme:
            url = 'https://' + url

        tech = builtwith.parse(url)

        if not tech or len(tech.keys()) == 0:
            result["info"] = "No technologies detected or the site may be unreachable."
        else:
            result = tech

    except Exception as e:
        logger.error(f"BuiltWith detection failed for {url}: {e}")
        result["error"] = f"BuiltWith detection failed: {str(e)}"

    return result
