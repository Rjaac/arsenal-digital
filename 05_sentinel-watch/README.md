# 05_sentinel-watch

> Description: System Agent – 05_sentinel-watch

## 🔧 Purpose

- Describe the purpose of the 05_sentinel-watch agent here.

## 🚀 Usage

`ash
python main.py --config config.yaml
`

## 📁 Folder Structure

`
05_sentinel-watch/
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
