#!/usr/bin/env python3
"""
main.py – 03_warden
Created: 2025-04-09
Author: ChatGPT (Marty)

Description:
Entry point for the 03_warden agent.
Loads config, applies logic, and handles output.
"""

import yaml
import os
import sys

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        print("[ERROR] config.yaml not found.")
        sys.exit(1)

    config = load_config(config_path)
    if config.get("verbose", False):
        print("[INFO] Config loaded successfully.")
        print(config)

    print("[03_warden] Agent execution started...")

if __name__ == "__main__":
    main()
