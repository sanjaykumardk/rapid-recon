# modules/geoip_lookup.py

try:
    import os
    import requests
    from dotenv import load_dotenv
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger

# Load environment variables from .env
load_dotenv()

def get_geoip_info(ip_address: str) -> dict:
    """
    Retrieves GeoIP data for a given IP address using the IPinfo API.

    Parameters:
        ip_address (str): The IP address to query.

    Returns:
        dict: A dictionary with GeoIP data or error message.
    """
    token = os.getenv("IPINFO_TOKEN")
    if not token:
        logger.error("Missing IPINFO_TOKEN in your .env file. Example: IPINFO_TOKEN=your_token_here")
        return {
            "error": "Missing IPINFO_TOKEN in your .env file. Example: IPINFO_TOKEN=your_token_here"
        }

    url = f"https://ipinfo.io/{ip_address}/json?token={token}"
    headers = {"User-Agent": "ReconTool/1.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        logger.error(f"GeoIP lookup failed with HTTP {response.status_code} for {ip_address}")
        return {"error": f"GeoIP lookup failed with HTTP {response.status_code}"}
    except requests.RequestException as e:
        logger.error(f"GeoIP request failed for {ip_address}: {e}")
        return {"error": f"GeoIP request failed: {str(e)}"}
