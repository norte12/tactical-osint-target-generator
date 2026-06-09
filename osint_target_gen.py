import os
import sys
from datetime import datetime
import requests
import time
import random


def check_platform(url, name, alias, headers):
    try:
        # User agents y headers específicos para evadir bloqueos WAF y SPA
        googlebot_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }
        mobile_safari_headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }

        # Ajustes de endpoints estratégicos
        if name == "Reddit":
            url = f"https://old.reddit.com/user/{alias}"
        elif name == "Twitter_X":
            url = f"https://publish.twitter.com/oembed?url=https://twitter.com/{alias}"
        elif name == "Pinterest":
            url = f"https://www.pinterest.com/oembed.json?url=https://www.pinterest.com/{alias}/"
        elif name == "Medium":
            url = f"https://medium.com/feed/@{alias}"

        # Usar headers de Googlebot para Instagram y Spotify, y Mobile Safari para Facebook
        active_headers = headers
        if name in ["Instagram", "Spotify"]:
            active_headers = googlebot_headers
            if name == "Instagram":
                active_headers["Accept-Language"] = "en-US,en;q=0.9"
        elif name == "Facebook":
            active_headers = mobile_safari_headers

        if name in ["Facebook", "Instagram"] and not url.endswith("/"):
            url += "/"

        response = requests.get(url, headers=active_headers, timeout=8, allow_redirects=True)
        final_url = response.url.lower()
        content = response.text.lower()

        # Lógicas específicas de detección
        if name == "Instagram":
            # Lógica robusta e independiente de idioma basada en metadatos og:description
            has_og_desc = ('property="og:description"' in content or 
                           "property='og:description'" in content or 
                           'property=og:description' in content)
            if has_og_desc:
                return "Found (200)"
            else:
                return "Not Found (404)"

        if name == "Facebook":
            # Redirección determinista: si no existe, m.facebook.com atiende; si existe, www.facebook.com mantiene
            if "m.facebook.com" in final_url:
                return "Not Found (404)"
            elif "www.facebook.com" in final_url:
                return "Found (200)"
            elif response.status_code == 404:
                return "Not Found (404)"
            elif response.status_code in [403, 429, 999]:
                return f"Blocked ({response.status_code} - Protection Wall)"
            return f"Status {response.status_code}"

        if name == "Reddit":
            if response.status_code == 404 or "página no encontrada" in content or "page not found" in content:
                return "Not Found (404)"
            if response.status_code == 200:
                return "Found (200)"
            if response.status_code in [403, 429]:
                return f"Blocked ({response.status_code} - Protection Wall)"
            return f"Status {response.status_code}"

        if name == "Twitter_X":
            if response.status_code == 200:
                return "Found (200)"
            if response.status_code == 404:
                return "Not Found (404)"
            if response.status_code in [403, 429]:
                return f"Blocked ({response.status_code} - Protection Wall)"
            return f"Status {response.status_code}"

        if name == "Pinterest":
            if response.status_code == 200:
                return "Found (200)"
            if response.status_code in [400, 404] or "does not support this url" in content:
                return "Not Found (404)"
            if response.status_code in [403, 429]:
                return f"Blocked ({response.status_code} - Protection Wall)"
            return f"Status {response.status_code}"

        if name == "Medium":
            if response.status_code == 404 or "<body" in content:
                return "Not Found (404)"
            return "Found (200)"

        if name == "Spotify":
            if response.status_code == 404 or "page not found" in content or "página no encontrada" in content:
                return "Not Found (404)"
            if response.status_code == 200:
                return "Found (200)"
            if response.status_code in [403, 429]:
                return f"Blocked ({response.status_code} - Protection Wall)"
            return f"Status {response.status_code}"

        if name == "Twitch":
            # Si el alias está disponible para registro o el contenido no existe en la estructura interna
            if (
                'isavailable":true' in content
                or "unless you have a time machine" in content
                or "máquina del tiempo" in content
                or "twitch is the world&#39;s leading video platform" in content
                or "twitch is the world's leading video platform" in content
            ):
                return "Not Found (404)"
            if response.status_code == 404:
                return "Not Found (404)"
            return "Found (200)"

        if name == "GitLab":
            if response.status_code == 404 or "users/sign_in" in final_url or "sign_in" in final_url:
                return "Not Found (404)"
            return "Found (200)"

        # Fallbacks genéricos para plataformas estables
        if response.status_code == 200:
            if name == "Telegram" and (
                "tgme_page_extra" not in response.text
                or "view in telegram" not in content
            ):
                return "Not Found (404)"
            if name == "TikTok" and (
                '"statuscode":10221' in content or "user-not-found" in final_url
            ):
                return "Not Found (404)"
            return "Found (200)"
        elif response.status_code == 404:
            return "Not Found (404)"
        elif response.status_code in [403, 429, 999]:
            return f"Blocked ({response.status_code} - Protection Wall)"
        else:
            return f"Status {response.status_code}"

    except requests.exceptions.RequestException:
        return "Error/Timeout"


def main():
    print("=" * 65)
    print(" === TACTICAL OSINT TARGET GENERATOR v1.6 (Structural Engine) ===")
    print("=" * 65)

    alias = input("[?] Enter target alias/username: ").strip()
    if not alias:
        print("[-] Alias cannot be empty.")
        sys.exit(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    platforms = {
        "GitHub": f"https://github.com/{alias}",
        "GitLab": f"https://gitlab.com/{alias}",
        "Reddit": f"https://www.reddit.com/user/{alias}",
        "Twitter_X": f"https://x.com/{alias}",
        "Instagram": f"https://www.instagram.com/{alias}",
        "Facebook": f"https://www.facebook.com/{alias}",
        "TikTok": f"https://www.tiktok.com/@{alias}",
        "LinkedIn": f"https://www.linkedin.com/in/{alias}",
        "Telegram": f"https://t.me/{alias}",
        "Spotify": f"https://open.spotify.com/user/{alias}",
        "Linktree": f"https://linktr.ee/{alias}",
        "DockerHub": f"https://hub.docker.com/u/{alias}",
        "YouTube": f"https://www.youtube.com/@{alias}",
        "Twitch": f"https://www.twitch.tv/{alias}",
        "Medium": f"https://medium.com/@{alias}",
        "Pinterest": f"https://www.pinterest.com/{alias}",
    }

    results = {}
    print(f"\n[*] Launching structural footprinting for: {alias}...\n")

    for name, url in platforms.items():
        # Introducir retardo aleatorio para mantener un perfil bajo ante WAFs
        time.sleep(random.uniform(1.2, 2.5))
        results[name] = check_platform(url, name, alias, headers)
        status_flag = "[+]" if results[name].startswith("Found") else "[-]"
        print(f" {status_flag} {name}: {results[name]}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    yaml_properties = f"alias: {alias}\ntype: target\ncategory: reconnaissance\nstatus: active\ncreated_at: {now}\n"

    for name, url in platforms.items():
        clean_key = name.lower()
        val = url if results[name].startswith("Found") else "N/A"
        yaml_properties += f'{clean_key}: "{val}"\n'

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
- Fingerprint matrix verified via Structural Node & API Validation Engine on {now}.
"""

    filename = f"{alias}_target.md"
    target_folder = "02_Targets"

    if os.path.exists(target_folder) and os.path.isdir(target_folder):
        filepath = os.path.join(target_folder, filename)
    else:
        filepath = filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(
            f"\n[v] Reporte real purgado de falsos positivos generado en: {filepath}\n"
        )
    except Exception as e:
        print(f"[-] Error: {e}")


if __name__ == "__main__":
    main()
