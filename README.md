# Tactical OSINT Target Generator ⚡

A lightweight, fast, and passive OSINT footprinting script designed to automate initial target reconnaissance and export profiles natively into Markdown for Obsidian.

This script queries public platforms to verify the existence of a specific alias/username, avoiding active infrastructure interaction to maintain a low-profile investigation footprint.

## 🚀 Features

- **Passive Enumeration:** Fast checks across core platforms (GitHub, Twitter/X, Reddit, Linktree) without alerting the target.
- **Obsidian Native Integration:** Automatically generates a clean `.md` file with strict YAML Frontmatter/Properties syntax.
- **Zero Configuration:** Designed to feed directly into structured investigative environments.

## 🛠️ Installation & Usage

1. Clone this repository:
```bash
git clone https://github.com/norte12/tactical-osint-target-generator.git
cd tactical-osint-target-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python osint_target_gen.py
```

4. Enter the target's alias when prompted. The script will output a file named `[alias]_target.md`.

---

## 🎯 Level Up Your Investigation Workflow

This script is a standalone reconnaissance tool, but it was engineered to act as a module for a complete intelligence workflow.

If you need a professional, dark-mode optimized mission control center to link these targets, track infrastructure shifts, map relationship networks (Graph View), and keep your digital evidence secure and local, check out the full environment:

📦 **[Download the Tactical OSINT Vault on Gumroad](https://norte12.gumroad.com/l/pnnfl)** *(Available under a 'Name Your Price' model, including lifetime updates).*

```text
 🟢 1. RUN SCRIPT ───> 🔵 2. DRAG TO VAULT ───> 🟡 3. LINK NODES ───> 🔴 4. REPORT
   Execute Python       Drop the generated .md      Map relations via    Export pristine
    recon module         file inside /Targets        Canvas & Graphs      evidence logs
```

## 🔒 OpSec Notice

Operating entirely on local Markdown files ensures your intelligence data never touches third-party cloud servers. Keep your workspace local, keep your data private.

Developed by Azrael © 2026. Built for threat intel analysts, OSINT investigators, and red teamers.
