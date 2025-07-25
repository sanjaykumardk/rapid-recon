# 🕵️‍♀️ Rapid Recon

**Rapid Recon** is a Python-based reconnaissance and information-gathering tool that automates various intelligence-gathering techniques for cybersecurity professionals, ethical hackers, and SOC analysts. It collects crucial data such as DNS records, GeoIP info, WHOIS data, open ports, HTTP headers, technologies used, and generates structured reports.

---

## 🔧 Features

- 🔎 **DNS Lookup**: Queries DNS records to reveal subdomains, mail servers, name servers, and more.
- 🌍 **GeoIP Lookup**: Pinpoints the physical location of the target IP address.
- 🌐 **HTTP Info**: Fetches response headers, status codes, server information, etc.
- 🕵️ **WHOIS Lookup**: Extracts registration information and domain lifecycle.
- 🚪 **Port Scanning**: Detects open TCP ports using socket connections.
- 💻 **Technology Stack Detection**: Identifies backend/frontend technologies used by the target.
- 📤 **Export to JSON**: Saves all data in structured JSON for further analysis.
- 📝 **Report Generator**: Compiles results into a readable summary.
- ✅ **Input Validation**: Ensures clean and valid user inputs (IP/domain).

---

## 🚀 Getting Started

### Prerequisites and .env Configuration

- Python 3.8+
- Internet connection (for external lookups)
- Recommended: Virtual environment
- Within .env file : IPINFO_TOKEN=your_token

---

### Install Dependencies and Usage

```bash
pip install -r requirements.txt
python recon.py --help
python recon.py --all example.com





