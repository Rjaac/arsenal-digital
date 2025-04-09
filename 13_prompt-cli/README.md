# 13_prompt-cli

> Description: System Agent – 13_prompt-cli

## 🔧 Purpose

- Describe the purpose of the 13_prompt-cli agent here.

## 🚀 Usage

`ash
python main.py --config config.yaml
`

## 📁 Folder Structure

`
13_prompt-cli/
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
