# modules/dns_lookup.py

try:
    import dns.resolver
    import dns.exception
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger

def get_dns_records(domain: str) -> dict:
    """
    Perform DNS lookups for various record types on the provided domain.

    Parameters:
        domain (str): Domain name to query.

    Returns:
        dict: Dictionary containing DNS records by type.
    """
    records = {}
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5

    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']

    for rtype in record_types:
        try:
            answers = resolver.resolve(domain, rtype)
            records[rtype] = [rdata.to_text().strip() for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
                dns.exception.Timeout, dns.resolver.NoNameservers):
            records[rtype] = []
        except Exception as e:
            logger.error(f"[!] Error fetching {rtype} record for {domain}: {e}")
            records[rtype] = []

    return records
