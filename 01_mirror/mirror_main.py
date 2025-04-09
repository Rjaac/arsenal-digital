#!/usr/bin/env python3
"""
main.py – 01_mirror
Created: 2025-04-09
Author: ChatGPT (Marty)

Description:
This agent collects system information (hardware, software, drivers, etc.)
and stores it in a timestamped snapshot folder, using configuration from config.yaml.
"""

import os
import sys
import json
import yaml
import platform
import socket
import psutil
import subprocess
from datetime import datetime

# Load config.yaml from same directory
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    if not os.path.exists(config_path):
        print("[ERROR] config.yaml not found.")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Create snapshot folder with timestamp
def create_snapshot_dir(base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    snapshot_name = f"snapshot_{timestamp}"
    snapshot_path = os.path.join(base_dir, snapshot_name)
    os.makedirs(snapshot_path, exist_ok=True)
    return snapshot_name, snapshot_path

# Collect list of installed software (Windows)
def get_installed_software():
    try:
        output = subprocess.check_output(['wmic', 'product', 'get', 'name,version'], stderr=subprocess.DEVNULL, text=True)
        lines = output.splitlines()[1:]  # skip header
        software = []
        for line in lines:
            parts = line.strip().rsplit("  ", 1)
            if len(parts) == 2:
                name, version = parts
                software.append({
                    "name": name.strip(),
                    "version": version.strip()
                })
        return software
    except Exception as e:
        print(f"[mirror] Failed to get installed software: {e}")
        return []

# Collect all system info for snapshot
def collect_system_info():
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu": platform.processor(),
        "ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "disk_total_gb": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        "installed_software": get_installed_software()
    }

# Save snapshot in various formats
def save_snapshot(data, snapshot_path):
    with open(os.path.join(snapshot_path, "system_info.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    with open(os.path.join(snapshot_path, "system_info.md"), "w", encoding="utf-8") as f:
        f.write("# System Snapshot (Markdown)\n\n")
        for k, v in data.items():
            if k != "installed_software":
                f.write(f"- **{k}**: {v}\n")
    with open(os.path.join(snapshot_path, "system_info.txt"), "w", encoding="utf-8") as f:
        for k, v in data.items():
            if k != "installed_software":
                f.write(f"{k}: {v}\n")
    with open(os.path.join(snapshot_path, "version.txt"), "w") as f:
        f.write("mirror.py v1.1")

# Update pointer to last snapshot
def update_last_snapshot_pointer(base_dir, snapshot_name):
    with open(os.path.join(base_dir, "last_snapshot.txt"), "w") as f:
        f.write(snapshot_name)

# Main execution
def main():
    config = load_config()
    verbose = config.get("verbose", False)
    base_dir = os.path.dirname(__file__)
    snapshot_root = os.path.join(base_dir, config.get("snapshot_output_dir", "mirror_snapshots"))
    os.makedirs(snapshot_root, exist_ok=True)

    snapshot_name, snapshot_path = create_snapshot_dir(snapshot_root)
    if verbose:
        print(f"[mirror] Saving snapshot to: {snapshot_path}")

    system_info = collect_system_info()
    save_snapshot(system_info, snapshot_path)
    update_last_snapshot_pointer(base_dir, snapshot_name)

    if verbose:
        print("[mirror] Snapshot complete.")

if __name__ == "__main__":
    main()
