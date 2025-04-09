# 03_warden

> Description: System Agent – 03_warden

## 🔧 Purpose

- Describe the purpose of the 03_warden agent here.

## 🚀 Usage

`ash
python main.py --config config.yaml
`

## 📁 Folder Structure

`
03_warden/
├── main.py
├── config.yaml
├── rules/
├── logs/
└── README.md
`
"@

     = @"
# General Settings
verbose: true       # Show detailed execution info
dry_run: true       # Do not perform real deletions
log_level: "INFO"   # Options: DEBUG, INFO, WARNING, ERROR

# Paths
output_folder: "./logs"
rules_folder: "./rules"

# Execution profile
profile: "default"
