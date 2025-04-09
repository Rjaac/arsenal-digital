# mirror – v1.5

## 📌 Overview
`mirror` is a compact Python utility that captures a snapshot of your Windows system's key characteristics. It is designed to support lightweight system inventory, diagnostics, and integration with future agents like `janitor-bot`.

## 🧰 Features
- Collects:
  - System info (OS, CPU, RAM, hostname, architecture)
  - Disk usage and partition details
  - Installed software via Windows Registry
  - Active Windows services
  - Hardware drivers and devices (via WMI)
- Outputs a timestamped folder with:
  - `snapshot.md` – human-readable report
  - `snapshot.json` – structured data for parsing
  - `version.txt` – version and creation metadata
- Portable: can be run from any directory

## 🛠️ Usage
From any directory, run:
```bash
python mirror.py
```
This will create a folder like:
```
snapshot_20250407_1500/
├── snapshot.md
├── snapshot.json
└── version.txt
```

## 📦 Requirements
Make sure you have the following Python packages installed:
```bash
pip install psutil wmi pywin32
```

## 🔍 Output Example (snapshot.md)
```
## System Info
- os: Windows
- hostname: DONA_LAPTOP_ONE
- cpu_count: 4
- ram_total_gb: 5.95
...
```

## 🧭 Version History
- **v1.5 – 2025-04-07**
  - Simplified structure
  - Outputs snapshot directly in its own folder
  - Clean and modular for reuse

## 👥 Authors
- Ricardo Jorge Cardoso
- Marty (ChatGPT)

## 🔐 License
For personal use. Core tool for DONA_LAPTOP_ONE project.

