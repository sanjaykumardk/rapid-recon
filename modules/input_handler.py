# modules/input_handler.py

try:
    import socket
    from urllib.parse import urlparse
    import validators
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger

def detect_input_type(user_input: str) -> tuple[str, str, str | None]:
    """
    Determines if the input is a domain, IP, or URL and resolves IP if needed.

    Parameters:
        user_input (str): The input string provided by the user.

    Returns:
        tuple: (type: str [ip/domain/url/unknown], cleaned_input: str, resolved_ip: str or None)
    """
    cleaned_input = user_input.strip().lower()
    domain = None
    input_type = "unknown"

    # URL detection
    if validators.url(cleaned_input):
        parsed = urlparse(cleaned_input)
        domain = parsed.netloc or parsed.path
        input_type = "url"
    
    # Domain detection
    elif validators.domain(cleaned_input):
        domain = cleaned_input
        input_type = "domain"

    # IP detection
    elif validators.ipv4(cleaned_input) or validators.ipv6(cleaned_input):
        domain = cleaned_input
        input_type = "ip"

    # Invalid input
    else:
        return ("unknown", cleaned_input, None)

    # Resolve domain to IP
    try:
        resolved_ip = domain if input_type == "ip" else socket.getaddrinfo(domain, None)[0][4][0]
    except (socket.gaierror, IndexError) as e:
        logger.error(f"Failed to resolve IP for {domain}: {e}")
        resolved_ip = None

    return (input_type, domain, resolved_ip)
