import os
import sys
from datetime import datetime
import requests


def check_platform(url, name, headers):
    try:
        # Permitimos redirecciones (allow_redirects=True) para evaluar el comportamiento de los gigantes
        response = requests.get(url, headers=headers, timeout=6, allow_redirects=True)
        final_url = response.url.lower()

        # 1. Detectar si la plataforma nos desvió a un muro de Login/Registro (Falso Positivo Común)
        auth_indicators = [
            "login",
            "signin",
            "signup",
            "checkpoint",
            "session",
            "register",
        ]
        if (
            any(term in final_url for term in auth_indicators)
            and "login" not in url.lower()
        ):
            return "Not Found (Auth Wall / Redirected)"

        # 2. Evaluación de respuestas por código de estado y firmas de texto
        if response.status_code == 200:
            content = response.text

            # Control específico para Telegram (Siempre da 200, verificamos si existe la estructura del canal/perfil)
            if name == "Telegram":
                if (
                    "tgme_page_extra" not in content
                    or "If you have Telegram" in content
                    and "view in telegram" not in content.lower()
                ):
                    return "Not Found (404)"

            # Control específico para TikTok
            if name == "TikTok" and (
                '"statusCode":10221' in content or "user-not-found" in final_url
            ):
                return "Not Found (404)"

            return "Found (200)"

        elif response.status_code == 404:
            return "Not Found (404)"
        elif response.status_code in [403, 429]:
            return f"Blocked ({response.status_code} - Anti-Scraping Wall)"
        else:
            return f"Status {response.status_code}"

    except requests.exceptions.RequestException:
        return "Error/Timeout"


def main():
    print("=" * 65)
    print(" ⚡ TACTICAL OSINT TARGET GENERATOR v1.3 (Mainstream Arsenal) ⚡")
    print("=" * 65)

    alias = input("[?] Enter target alias/username: ").strip()
    if not alias:
        print("[-] Alias cannot be empty.")
        sys.exit(1)

    # User-Agent avanzado para simular navegación residencial legítima
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Matriz ampliada incluyendo las redes sociales más utilizadas a nivel global
    platforms = {
        "GitHub": f"https://github.com/{alias}",
        "GitLab": f"https://gitlab.com/{alias}",
        "Reddit": f"https://www.reddit.com/user/{alias}",
        "Twitter_X": f"https://x.com/{alias}",
        "Instagram": f"https://www.instagram.com/{alias}/",
        "Facebook": f"https://www.facebook.com/{alias}",
        "TikTok": f"https://www.tiktok.com/@{alias}",
        "LinkedIn": f"https://www.linkedin.com/in/{alias}",
        "Telegram": f"https://t.me/{alias}",
        "Spotify": f"https://open.spotify.com/user/{alias}",
        "Linktree": f"https://linktr.ee/{alias}",
        "DockerHub": f"https://hub.docker.com/u/{alias}",
        "Dev_to": f"https://dev.to/{alias}",
        "Keybase": f"https://keybase.io/{alias}",
        "YouTube": f"https://www.youtube.com/@{alias}",
        "Twitch": f"https://www.twitch.tv/{alias}",
        "Medium": f"https://medium.com/@{alias}",
        "Pinterest": f"https://www.pinterest.com/{alias}/",
        "SoundCloud": f"https://soundcloud.com/{alias}",
    }

    results = {}
    print(
        f"\n[*] Launching footprinting for: {alias} across {len(platforms)} core platforms...\n"
    )

    for name, url in platforms.items():
        results[name] = check_platform(url, name, headers)
        status_flag = "[+]" if "Found" in results[name] else "[-]"
        print(f" {status_flag} {name}: {results[name]}")

    # Generación dinámica del Frontmatter para Obsidian
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    yaml_properties = f"alias: {alias}\ntype: target\ncategory: reconnaissance\nstatus: active\ncreated_at: {now}\n"

    for name, url in platforms.items():
        clean_key = name.lower()
        val = url if "Found" in results[name] else "N/A"
        yaml_properties += f'{clean_key}: "{val}"\n'

    # Generación dinámica del cuerpo del reporte Markdown
    summary_lines = ""
    for name, res in results.items():
        summary_lines += f"- **{name}:** {res}\n"

    markdown_content = f"""---
{yaml_properties.strip()}
---

# Target Profile: {alias} 🎯

## 🔍 Passive Footprinting Summary
{summary_lines}
## 📝 Investigation Notes
- Comprehensive target identity matrix generated on {now}.
- Cross-reference positive indicators across social, developer, and media layers.
- Maintain data segregation and local storage protocols to guarantee OpSec.
"""

    filename = f"{alias}_target.md"
    target_folder = "02_Targets"

    if os.path.exists(target_folder) and os.path.isdir(target_folder):
        filepath = os.path.join(target_folder, filename)
        print(
            f"\n[+] Obsidian Vault structure detected. Auto-routing profile to: {target_folder}/"
        )
    else:
        filepath = filename
        print(
            f"\n[!] Folder '{target_folder}' not found. Saving profile to current root directory."
        )

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"[✓] Investigation profile successfully generated at: {filepath}\n")
    except Exception as e:
        print(f"[-] Critical Error writing the markdown file: {e}")


if __name__ == "__main__":
    main()
