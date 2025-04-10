# warden_main.py
# Created: 2025-04-10
# Author: ChatGPT / Marty

# Description:
# This script is responsible for scanning the monitored files, checking for modifications or dangerous permissions,
# and generating reports for the janitor process.
#
# Path: C:\Users\ricar\Projects\Laptop\SysAdminTools\03_warden\warden_main.py

import os
import json
import hashlib
import logging
import yaml
import stat
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

CONFIG_PATH = "config.yaml"
WATCHLIST_PATH = "rules/watchlist.json"
BASELINE_PATH = "logs/baseline_hashes.json"
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'warden_log.txt')

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return yaml.safe_load(file) or {}
    return {}

def load_watchlist(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    logging.warning("Watchlist not found at %s", path)
    return []

def compute_file_hash(path):
    try:
        with open(path, 'rb') as f:
            sha256 = hashlib.sha256()
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
            return sha256.hexdigest()
    except Exception as e:
        logging.error("Error reading %s: %s", path, str(e))
        return None

def check_file_permissions(path):
    try:
        mode = os.stat(path).st_mode
        if os.name == 'posix':
            perms = oct(mode)[-3:]
            if perms == '777':
                logging.warning("Dangerous permission 777 detected: %s", path)
            return perms
        elif os.name == 'nt':
            if os.access(path, os.W_OK):
                logging.warning("Writable file detected: %s", path)
                return "writable"
            else:
                return "restricted"
    except Exception as e:
        logging.error("Error checking permissions for %s: %s", path, str(e))
        return "unknown"

def load_previous_hashes(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return {}

def save_current_hashes(path, hash_dict):
    with open(path, 'w') as file:
        json.dump(hash_dict, file, indent=2)

def export_scan_report(timestamp, results):
    ts_label = timestamp.strftime("%Y%m%d_%H%M")
    json_path = f"logs/scan_{ts_label}.json"
    md_path = f"logs/scan_{ts_label}.md"
    jb_path = f"logs/janitor_instructions_{ts_label}.json"

    # Export JSON
    with open(json_path, 'w', encoding='utf-8') as f_json:
        json.dump(results, f_json, indent=2)

    # Export Markdown
    with open(md_path, 'w', encoding='utf-8') as f_md:
        f_md.write(f"## Warden Scan Report - {timestamp}

")
        f_md.write("| File Path | Status | Previous Hash | Current Hash | Permissions |
")
        f_md.write("|-----------|--------|----------------|---------------|-------------|
")
        for path, data in results["files"].items():
            f_md.write(f"| {path} | {data['status']} | {data.get('previous_hash', '-')[:10]} | {data['current_hash'][:10]} | {data['permissions']} |
")

    # Save copy to Desktop/logs
    desktop_logs = os.path.join(os.path.expanduser("~"), "Desktop", "logs")
    os.makedirs(desktop_logs, exist_ok=True)
    dtstamp = timestamp.strftime("%d%m%y%H%M")
    desktop_report = os.path.join(desktop_logs, f"warden_log_{dtstamp}.md")
    with open(desktop_report, 'w', encoding='utf-8') as f:
        with open(md_path, 'r', encoding='utf-8') as original:
            f.write(original.read())

    # Generate janitor-boy instructions
    actions = []
    for path, data in results["files"].items():
        if data["permissions"] in ["777", "writable"]:
            actions.append({
                "path": path,
                "issue": "dangerous_permissions",
                "suggestion": "set to 644"
            })
        if data["status"] == "modified":
            actions.append({
                "path": path,
                "issue": "modified",
                "suggestion": "verify integrity"
            })
    janitor_payload = {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "actions": actions
    }
    with open(jb_path, 'w', encoding='utf-8') as f_jb:
        json.dump(janitor_payload, f_jb, indent=2)

def monitor_files(watchlist):
    previous_hashes = load_previous_hashes(BASELINE_PATH)
    current_hashes = {}
    scan_results = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "files": {}}
    changes_detected = False

    for filepath in watchlist:
        hash_value = compute_file_hash(filepath)
        current_hashes[filepath] = hash_value
        permissions = check_file_permissions(filepath)

        if hash_value is None:
            continue

        previous_hash = previous_hashes.get(filepath)
        status = "unchanged"

        if previous_hash and previous_hash != hash_value:
            logging.warning("File modified: %s", filepath)
            status = "modified"
            changes_detected = True
        elif not previous_hash:
            logging.info("New file monitored: %s", filepath)
            status = "new"

        scan_results["files"][filepath] = {
            "previous_hash": previous_hash,
            "current_hash": hash_value,
            "status": status,
            "permissions": permissions
        }

    save_current_hashes(BASELINE_PATH, current_hashes)
    export_scan_report(datetime.now(), scan_results)

    if not changes_detected:
        logging.info("No changes detected.")

def main():
    logging.info("WARDEN started.")
    config = load_config(CONFIG_PATH)
    watchlist = load_watchlist(WATCHLIST_PATH)
    monitor_files(watchlist)
    logging.info("WARDEN finished.")

    # Save a copy of the log file to Desktop/logs
    desktop_logs = os.path.join(os.path.expanduser("~"), "Desktop", "logs")
    os.makedirs(desktop_logs, exist_ok=True)
    dtstamp = datetime.now().strftime("%d%m%y%H%M")
    log_copy_path = os.path.join(desktop_logs, f"warden_log_{dtstamp}.txt")
    with open(LOG_FILE, 'r', encoding='utf-8') as original_log:
        with open(log_copy_path, 'w', encoding='utf-8') as backup:
            backup.write(original_log.read())

if __name__ == "__main__":
    main()
