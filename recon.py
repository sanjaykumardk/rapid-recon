# recon.py (minimal console with cool progress)
import os
import argparse
from urllib.parse import urlparse
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

from modules.input_handler import detect_input_type
from modules.whois_lookup import perform_whois_lookup
from modules.dns_lookup import get_dns_records
from modules.port_scan import run_nmap_scan
from modules.http_info import fetch_http_info
from modules.tech_stack import detect_tech_stack
from modules.geoip_lookup import get_geoip_info
from modules.report_generator import generate_html_report
from modules.json_export import export_json

console = Console()

def banner():
    console.print(Panel.fit(
        "[bold cyan]⚡ Rapid-Recon[/bold cyan]\n[white]Advanced Reconnaissance CLI Tool[/white]",
        subtitle="by YourName", subtitle_align="right"
    ))

def parse_arguments():
    parser = argparse.ArgumentParser(description="Rapid-Recon: Domain/IP/URL Info Gathering Tool")
    parser.add_argument("target", help="Target domain, IP address, or URL")
    parser.add_argument("--scan-ports", action="store_true", help="Run Nmap port scan")
    parser.add_argument("--skip-whois", action="store_true", help="Skip WHOIS lookups")
    parser.add_argument("--dns", action="store_true", help="Fetch DNS records")
    parser.add_argument("--http-info", action="store_true", help="Fetch HTTP headers/status")
    parser.add_argument("--tech-stack", action="store_true", help="Detect web technologies using BuiltWith")
    parser.add_argument("--geoip", action="store_true", help="Get geolocation from IPInfo")
    parser.add_argument("--all", action="store_true", help="Run all scans")
    parser.add_argument("--output", type=str, default="output/report.html", help="HTML output path (default: output/report.html)")
    parser.add_argument("--json", action="store_true", help="Also save raw data as JSON")
    return parser.parse_args()

def normalize_url(url):
    parsed = urlparse(url)
    return url if parsed.scheme else "https://" + url

def main():
    banner()
    args = parse_arguments()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    input_type, cleaned_input, ip_address = detect_input_type(args.target)
    if input_type == "unknown":
        console.print("[bold red]❌ Invalid input. Please provide a valid IP, domain, or URL.[/bold red]")
        return

    results = {}
    selected_modules = {
        "whois": not args.skip_whois and (args.all or not any([
            args.scan_ports, args.dns, args.http_info, args.tech_stack, args.geoip
        ])),
        "dns": args.all or args.dns,
        "ports": args.all or args.scan_ports,
        "http": args.all or args.http_info,
        "tech": args.all or args.tech_stack,
        "geoip": args.all or args.geoip,
    }

    task_map = {
        "whois": ("🔍 Performing WHOIS Lookup", lambda: perform_whois_lookup(cleaned_input, ip_address)),
        "dns": ("🌐 Fetching DNS Records", lambda: get_dns_records(cleaned_input)),
        "ports": ("🚪 Scanning Ports", lambda: run_nmap_scan(ip_address) if ip_address else None),
        "http": ("📡 Fetching HTTP Info", lambda: fetch_http_info(normalize_url(args.target))),
        "tech": ("🧠 Detecting Technology Stack", lambda: detect_tech_stack(normalize_url(args.target))),
        "geoip": ("🌍 Retrieving Geolocation", lambda: get_geoip_info(ip_address) if ip_address else None),
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TimeElapsedColumn(),
        transient=True
    ) as progress:
        for key, enabled in selected_modules.items():
            if not enabled:
                continue

            task_desc, task_func = task_map[key]
            task_id = progress.add_task(task_desc, total=None)

            try:
                res = task_func()
                results[key] = res
            except Exception as e:
                console.print(f"[red]❌ {key} scan failed: {e}[/red]")
            finally:
                progress.update(task_id, completed=1)

    # Generate HTML report
    try:
        console.print("\n[bold yellow]📄 Generating HTML report...[/bold yellow]")
        generate_html_report(cleaned_input, results, args.output)
        console.print(f"[bold green]✅ Report saved to:[/bold green] {args.output}")
    except Exception as e:
        console.print(f"[red]❌ Failed to generate HTML report: {e}[/red]")

    if args.json:
        try:
            json_path = args.output.replace(".html", ".json")
            export_json(results, json_path)
            console.print(f"[bold blue]📁 JSON report saved to:[/bold blue] {json_path}")
        except Exception as e:
            console.print(f"[red]❌ Failed to export JSON: {e}[/red]")

    console.print("\n[bold green]🎯 Recon complete. Enjoy your insights![/bold green]")

if __name__ == "__main__":
    main()
