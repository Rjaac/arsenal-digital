# janitor-boy_main.py
# Created: 2025-04-10
# Author: ChatGPT / Marty

# Description:
# This script is responsible for monitoring installed software, checking for dangerous permissions,
# applying cleanup rules, and generating reports for the janitor process.
#
# Path: C:\Users\ricar\Projects\Laptop\SysAdminTools\02_janitor-boy\janitor-boy_main.py

import os
import sys
import yaml
import json
import glob
import stat
from datetime import datetime

def load_yaml(path):
    if not os.path.exists(path):
        print(f"[ERROR] YAML file not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(path):
    if not os.path.exists(path):
        print(f"[ERROR] JSON file not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_last_snapshot_path(mirror_dir):
    pointer_path = os.path.join(mirror_dir, "last_snapshot.txt")
    if not os.path.exists(pointer_path):
        print("[ERROR] last_snapshot.txt not found.")
        sys.exit(1)
    with open(pointer_path, "r") as f:
        snapshot_folder = f.read().strip()
    return os.path.join(mirror_dir, "mirror_snapshots", snapshot_folder, "system_info.json")

def load_latest_warden_instructions(logs_dir):
    files = sorted(
        glob.glob(os.path.join(logs_dir, "janitor_instructions_*.json")),
        reverse=True
    )
    if not files:
        return []
    with open(files[0], "r", encoding="utf-8") as f:
        return json.load(f).get("actions", [])

def apply_uninstall_rules(software_list, rules):
    suggestions = []
    blacklist = rules.get("blacklist", [])
    keywords = rules.get("keyword_match", [])

    for app in software_list:
        name = app.get("name", "").lower()
        matched = False
        reason = ""

        for item in blacklist:
            if item.lower() in name:
                matched = True
                reason = f"blacklist match: {item}"
                break

        if not matched:
            for kw in keywords:
                if kw.lower() in name:
                    matched = True
                    reason = f"keyword match: {kw}"
                    break

        if matched:
            suggestions.append({
                "name": app.get("name", "Unknown"),
                "version": app.get("version", "N/A"),
                "reason": reason
            })

    return suggestions

def act_on_warden_actions(actions):
    for act in actions:
        path = act.get("path")
        issue = act.get("issue")
        if issue == "dangerous_permissions":
            try:
                if os.name == "posix":
                    os.chmod(path, 0o644)
                    print(f"[ACTION] Permissions corrected for {path} → 644")
                elif os.name == "nt":
                    os.chmod(path, stat.S_IREAD)
                    print(f"[ACTION] Permissions set to read-only for {path}")
            except Exception as e:
                print(f"[ERROR] Could not change permissions for {path}: {e}")
        elif issue == "modified":
            print(f"[NOTICE] File modified: {path} (please verify integrity)")

def write_report(software_suggestions, warden_actions, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        f.write(f"# janitor-boy Report – {timestamp}

")

        if not software_suggestions:
            f.write("✅ No redundant software detected.

")
        else:
            f.write("## Suggested Uninstalls:
")
            for s in software_suggestions:
                f.write(f"- **{s['name']}** ({s['version']}) – {s['reason']}
")

        if warden_actions:
            f.write("
## Actions from WARDEN:
")
            for act in warden_actions:
                f.write(f"- **{act['path']}** → *{act['issue']}* → {act['suggestion']}
")

    # Save copy to Desktop/logs
    desktop_logs = os.path.join(os.path.expanduser("~"), "Desktop", "logs")
    os.makedirs(desktop_logs, exist_ok=True)
    dtstamp = datetime.now().strftime("%d%m%y%H%M")
    desktop_report = os.path.join(desktop_logs, f"janitor-boy_{dtstamp}.md")
    with open(desktop_report, "w", encoding="utf-8") as f:
        with open(output_path, "r", encoding="utf-8") as original:
            f.write(original.read())

def main():
    base_dir = os.path.dirname(__file__)
    profile_path = os.path.join(base_dir, "profiles", "deep_clean.yaml")
    mirror_dir = os.path.join(os.path.dirname(base_dir), "01_mirror")
    logs_dir = os.path.join(base_dir, "logs")

    profile = load_yaml(profile_path)
    snapshot_path = find_last_snapshot_path(mirror_dir)
    snapshot = load_json(snapshot_path)

    software_list = snapshot.get("installed_software", [])
    uninstall_rules = profile.get("uninstall_rules", {})

    software_suggestions = apply_uninstall_rules(software_list, uninstall_rules)
    warden_actions = load_latest_warden_instructions(logs_dir)

    if warden_actions:
        act_on_warden_actions(warden_actions)

    report_path = os.path.join(logs_dir, f"janitor_suggestions_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
    write_report(software_suggestions, warden_actions, report_path)

    print(f"[janitor-boy] Analysis complete. Report written to: {report_path}")

if __name__ == "__main__":
    main()
