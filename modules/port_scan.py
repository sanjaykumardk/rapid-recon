# modules/port_scan.py

try:
    import nmap
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger

def run_nmap_scan(ip_address: str, ports: str = "1-1000") -> dict:
    """
    Runs a comprehensive Nmap scan with advanced options:
    -sS (SYN scan), -sC (default scripts), -T4 (aggressive timing),
    -O (OS detection), -A (aggressive scan including version detection and traceroute)

    Args:
        ip_address (str): Target IP address.
        ports (str): Port range (default is 1-1000).

    Returns:
        dict: Scan results including ports, services, OS detection, and traceroute.
    """
    results = {
        "open_ports": {},
        "os_detection": {},
        "traceroute": [],
        "error": None
    }

    try:
        scanner = nmap.PortScanner()
    except nmap.PortScannerError as e:
        logger.error(f"Nmap not found or error initializing scanner: {str(e)}")
        return {"error": f"Nmap not found or error initializing scanner: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error initializing Nmap: {str(e)}")
        return {"error": f"Unexpected error initializing Nmap: {str(e)}"}

    try:
        # Build full command string
        scan_args = f"-sS -sC -T4 -O -A -p {ports}"
        scanner.scan(ip_address, arguments=scan_args)

        if ip_address not in scanner.all_hosts():
            logger.error("No response from target or host is down.")
            return {"error": "No response from target or host is down."}

        # Collect open ports and services
        for proto in scanner[ip_address].all_protocols():
            results["open_ports"][proto] = {}
            ports_list = scanner[ip_address][proto].keys()
            for port in sorted(ports_list):
                port_data = scanner[ip_address][proto][port]
                service = port_data.get('name', 'unknown')
                state = port_data.get('state', 'unknown')
                product = port_data.get('product', '')
                version = port_data.get('version', '')
                results["open_ports"][proto][port] = {
                    "state": state,
                    "service": service,
                    "product": product,
                    "version": version
                }

        # OS detection
        if 'osmatch' in scanner[ip_address]:
            os_matches = scanner[ip_address]['osmatch']
            results["os_detection"] = [
                {
                    "name": match.get('name', ''),
                    "accuracy": match.get('accuracy', ''),
                    "osclass": match.get('osclass', [])
                }
                for match in os_matches
            ]

        # Traceroute data
        if 'traceroute' in scanner[ip_address]:
            trace = scanner[ip_address]['traceroute']
            hops = trace.get('hops', [])
            for hop in hops:
                results["traceroute"].append({
                    "ttl": hop.get('ttl'),
                    "ip": hop.get('ipaddr'),
                    "rtt": hop.get('rtt')
                })

    except Exception as e:
        logger.error(f"Port scan failed: {str(e)}")
        results["error"] = f"Port scan failed: {str(e)}"

    return results
