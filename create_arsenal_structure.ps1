
# PowerShell Script – Create Full Arsenal Digital Structure

$basePath = "C:\Users\ricar\Projects\Laptop\SysAdminTools"

$agents = @(
    "01_mirror", "02_janitor-boy", "03_warden", "04_kit-builder", "05_sentinel-watch",
    "06_logseer", "07_configsync", "08_cli-buddy", "09_ark", "10_atlas",
    "11_sandbox-me", "12_docuBot", "13_prompt-cli", "14_fleet-control", "15_failForge"
)

$mainFolders = @("00_common", "installer", "docs", "tests", "bin")

# Criar diretórios principais
foreach ($folder in $mainFolders) {
    $fullPath = Join-Path $basePath $folder
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath | Out-Null
        Write-Host "Created: $fullPath"
    }
}

# Criar estrutura para cada agente
foreach ($agent in $agents) {
    $agentPath = Join-Path $basePath $agent
    $subfolders = @("rules", "logs")
    $files = @("main.py", "config.yaml", "README.md")

    if (-not (Test-Path $agentPath)) {
        New-Item -ItemType Directory -Path $agentPath | Out-Null
        Write-Host "Created agent dir: $agentPath"
    }

    foreach ($sub in $subfolders) {
        $subPath = Join-Path $agentPath $sub
        if (-not (Test-Path $subPath)) {
            New-Item -ItemType Directory -Path $subPath | Out-Null
        }
    }

    # Gerar ficheiros com conteúdo base
    $readme = @"
# $agent

> Description: System Agent – $agent

## 🔧 Purpose

- Describe the purpose of the $agent agent here.

## 🚀 Usage

```bash
python main.py --config config.yaml
```

## 📁 Folder Structure

```
$agent/
├── main.py
├── config.yaml
├── rules/
├── logs/
└── README.md
```
"@

    $config = @"
# General Settings
verbose: true       # Show detailed execution info
dry_run: true       # Do not perform real deletions
log_level: "INFO"   # Options: DEBUG, INFO, WARNING, ERROR

# Paths
output_folder: "./logs"
rules_folder: "./rules"

# Execution profile
profile: "default"
"@

    $mainpy = @"
#!/usr/bin/env python3
"""
main.py – $agent
Created: 2025-04-09
Author: ChatGPT (Marty)

Description:
Entry point for the $agent agent.
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

    print("[$agent] Agent execution started...")

if __name__ == "__main__":
    main()
"@

    Set-Content -Path (Join-Path $agentPath "README.md") -Value $readme
    Set-Content -Path (Join-Path $agentPath "config.yaml") -Value $config
    Set-Content -Path (Join-Path $agentPath "main.py") -Value $mainpy
}

Write-Host "`n✅ Full Arsenal Digital structure created at: $basePath"
