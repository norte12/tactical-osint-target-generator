import os
import sys
from datetime import datetime
import requests

# Terminal ANSI colors for tactical aesthetic
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def check_platform(username, platform_name, url_template):
    url = url_template.format(username)
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return f"[x] **{platform_name}:** {url}"
        else:
            return f"[ ] **{platform_name}:** Not detected (Status: {response.status_code})"
    except requests.RequestException:
        return f"[ ] **{platform_name}:** Connection error"


def main():
    print(f"{GREEN}=== Tactical OSINT Target Generator v1.0 ==={RESET}")

    alias = input(
        f"{BLUE}[?] Enter Target Alias/Username to investigate: {RESET}"
    ).strip()
    if not alias:
        print(f"{RED}[!] Alias cannot be empty.{RESET}")
        sys.exit(1)

    print(f"\n{GREEN}[*] Running fast footprint scan for: {alias}...{RESET}")

    # Core OSINT targets for passive enumeration
    platforms = {
        "GitHub": "https://github.com/{}",
        "Twitter/X": "https://twitter.com/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "Linktree": "https://linktr.ee/{}",
    }

    results = []
    for name, url in platforms.items():
        print(f"[-] Checking {name}...")
        results.append(check_platform(alias, name, url))

    # Get current timestamp formatted for Obsidian YAML
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Generate native English Markdown structural template
    markdown_content = f"""---
target_type: Individual
aliases: [{alias}]
first_name:
last_name:
d_o_b:
nationality:
priority: Medium # High, Medium, Low
status: Active # Active, In_Progress, Closed
created: {current_date}
---

# 👤 Target: {alias}

## 🆔 Identity & Biographical Data
* **Full Name:** * **Government ID / Passport / Documents:** * **Known Location / Physical Address:** * **Occupation / Corporate Ties:** ---

## 🌐 Digital Footprint
### Social Media & Platforms (Automated Initial Recon)
"""
    for res in results:
        markdown_content += f"{res}\n"

    markdown_content += (
        """
### Discovered Emails & Leaks
* `example@domain.com`

### Phone Numbers
* ---

## 💻 Infrastructure & Digital Assets
* **Associated IP Addresses:** * **Hardware Devices / Detected User-Agents:** * **Crypto Wallets (BTC/XMR/ETH):** ---

## 📑 Timeline of Findings & Log
> Document chronological discoveries and intelligence logs here.

* **["""
        + current_date
        + f"""]:** Automated initial profile generation via tactical recon script.

---

## 🔗 Relations & Link Analysis
* """
    )

    # Sanitize and write out the Markdown target profile
    filename = f"{alias}_target.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"\n{GREEN}[+] Scan completed successfully!{RESET}")
    print(f"[+] File generated: {BLUE}{filename}{RESET}")
    print(
        f"[i] Drag and drop this file directly into your {BLUE}02_Targets/{RESET} folder inside the Vault."
    )


if __name__ == "__main__":
    main()
