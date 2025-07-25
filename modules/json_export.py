# modules/json_export.py

try:
    import json
    import os
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger

def export_json(data: dict, filename: str) -> None:
    """
    Exports the given data to a JSON file.

    Parameters:
        data (dict): Data to write to JSON.
        filename (str): Output file path.
    """
    try:
        directory = os.path.dirname(os.path.abspath(filename))
        os.makedirs(directory, exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logger.info(f"[\u2713] JSON report saved to {filename}")
    except Exception as e:
        logger.error(f"[!] Failed to export JSON: {e}")
