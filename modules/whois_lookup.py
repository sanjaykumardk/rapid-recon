# modules/whois_lookup.py

try:
    import whois  # from python-whois
    from ipwhois import IPWhois
    from ipwhois.exceptions import IPDefinedError
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger


def perform_whois_lookup(target: str, ip_address: str) -> dict:
    """
    Performs WHOIS lookup for both domain and IP address.

    Args:
        target (str): The domain or URL (e.g., "example.com")
        ip_address (str): The resolved IP address of the target

    Returns:
        dict: Dictionary containing domain WHOIS and IP WHOIS information
    """
    results = {
        'domain': {},
        'ip': {}
    }

    # --- Domain WHOIS Lookup ---
    try:
        w = whois.whois(target)

        # Normalize date fields
        def get_date(d):
            return str(d[0]) if isinstance(d, list) else str(d) if d else None

        results['domain'] = {
            'domain_name': str(w.domain_name) if w.domain_name else None,
            'registrar': str(w.registrar) if w.registrar else None,
            'creation_date': get_date(w.creation_date),
            'expiration_date': get_date(w.expiration_date),
            'name_servers': w.name_servers if w.name_servers else [],
            'emails': w.emails if w.emails else [],
        }
    except Exception as e:
        logger.error(f"WHOIS domain lookup failed: {e}")
        results['domain'] = {"error": f"WHOIS domain lookup failed: {str(e)}"}

    # --- IP WHOIS Lookup ---
    try:
        if ip_address:
            ip_info = IPWhois(ip_address)
            ip_data = ip_info.lookup_rdap()

            results['ip'] = {
                'asn': ip_data.get('asn'),
                'asn_description': ip_data.get('asn_description'),
                'network_name': ip_data.get('network', {}).get('name'),
                'country': ip_data.get('network', {}).get('country'),
                'ip_address': ip_address
            }
        else:
            logger.warning("No IP address provided for WHOIS lookup.")
            results['ip'] = {"error": "No IP address provided for lookup."}
    except IPDefinedError:
        logger.warning("Reserved IP address (e.g., private/local network). WHOIS lookup skipped.")
        results['ip'] = {"error": "Reserved IP address (e.g., private/local network). WHOIS lookup skipped."}
    except Exception as e:
        logger.error(f"WHOIS IP lookup failed: {e}")
        results['ip'] = {"error": f"WHOIS IP lookup failed: {str(e)}"}

    return results
