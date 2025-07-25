# modules/http_info.py

try:
    import requests
    from urllib.parse import urlparse
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger

def fetch_http_info(url: str) -> dict:
    """
    Fetches HTTP status and headers for the given URL.

    Parameters:
        url (str): The target URL.

    Returns:
        dict: Dictionary containing status code, headers, final redirected URL, or error.
    """
    headers = {
        "User-Agent": "ReconTool/1.0"
    }

    # Normalize URL: add scheme if missing
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"

    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "final_url": response.url
        }
    except requests.RequestException as e:
        logger.error(f"HTTP request failed for {url}: {e}")
        return {"error": f"HTTP request failed: {str(e)}"}
