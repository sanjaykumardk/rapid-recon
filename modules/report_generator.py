# modules/report_generator.py

import os
try:
    import html
    from datetime import datetime
except ImportError as e:
    from utils.logger import logger
    logger.error(f"Missing dependency: {e}. Please install required modules.")
    raise
from utils.logger import logger


def generate_html_report(target: str, results: dict, output_path: str) -> None:
    """
    Generates an HTML report from the scan results.
    Args:
        target (str): The scan target.
        results (dict): The results dictionary.
        output_path (str): Path to save the HTML report.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Recon Report - {html.escape(target)}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        header {{
            background: linear-gradient(to right, #283e51, #485563);
            color: #fff;
            text-align: center;
            padding: 2rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            margin: 0;
            font-size: 2.5rem;
        }}
        h2 {{
            font-size: 1.4rem;
            margin-top: 1rem;
            color: #1f3c88;
        }}
        .section {{
            background: #fff;
            margin: 2rem auto;
            padding: 1.5rem;
            max-width: 1000px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        .summary-table, .kv-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}
        .summary-table th, .summary-table td,
        .kv-table th, .kv-table td {{
            padding: 0.8rem;
            border: 1px solid #ddd;
            text-align: left;
        }}
        .summary-table th {{
            background: #f0f4f8;
        }}
        .badge {{
            display: inline-block;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-size: 0.9rem;
            font-weight: bold;
        }}
        .badge.success {{
            background: #d4edda;
            color: #155724;
        }}
        .badge.fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        .card {{
            background: #f9fbfd;
            border: 1px solid #e1e5ea;
            border-radius: 6px;
            padding: 0.8rem 1rem;
            margin-bottom: 0.7rem;
        }}
        .card strong {{
            color: #2c3e50;
        }}
        .code-block {{
            background: #f4f4f4;
            border-radius: 6px;
            padding: 1rem;
            font-family: monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
            margin-top: 0.5rem;
        }}
        .footer {{
            text-align: center;
            font-size: 0.9rem;
            color: #888;
            padding: 2rem 0;
        }}
    </style>
</head>
<body>

<header>
    <h1>🛡️ Recon Report</h1>
    <p>Target: <strong>{html.escape(target)}</strong><br>
    Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</header>

<div class="section">
    <h2>📋 Summary</h2>
    <table class="summary-table">
        <tr><th>Section</th><th>Status</th></tr>"""

        for section in results:
            readable = section.replace("_", " ").title()
            status = "✔️ Collected" if results[section] else "⚠️ Missing"
            badge_class = "success" if results[section] else "fail"
            html_content += f"<tr><td>{html.escape(readable)}</td><td><span class='badge {badge_class}'>{status}</span></td></tr>"

        html_content += "</table></div>"

        for section, content in results.items():
            html_content += f"""<div class="section">
    <h2>📂 {html.escape(section.replace('_', ' ').title())}</h2>
    {format_content_as_html(content)}
</div>"""

        html_content += f"""<div class="footer">
    &copy; {datetime.now().year} Recon Tool | Generated for <strong>{html.escape(target)}</strong>
</div>

</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"[\u2713] HTML report saved to {output_path}")
    except Exception as e:
        logger.error(f"[!] Failed to generate HTML report: {e}")


def format_content_as_html(content):
    if isinstance(content, dict):
        output = "<table class='kv-table'>"
        output += "<tr><th>Key</th><th>Value</th></tr>"
        for k, v in content.items():
            value = format_content_as_html(v)
            output += f"<tr><td>{html.escape(str(k))}</td><td>{value}</td></tr>"
        output += "</table>"
        return output
    elif isinstance(content, list):
        if all(isinstance(item, dict) for item in content):
            output = ""
            for item in content:
                output += "<div class='card'>"
                for k, v in item.items():
                    output += f"<strong>{html.escape(str(k))}</strong>: {html.escape(str(v))}<br>"
                output += "</div>"
            return output
        else:
            return "<ul>" + "".join(f"<li>{html.escape(str(item))}</li>" for item in content) + "</ul>"
    elif content is None:
        return "<span class='badge fail'>No Data</span>"
    else:
        return html.escape(str(content))
