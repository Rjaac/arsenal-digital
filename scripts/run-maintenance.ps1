# run-maintenance.ps1
# Executa Warden e Janitor-Boy com nomes de ficheiro atualizados

Write-Host "=== Início da Manutenção ===" -ForegroundColor Cyan

# Caminhos relativos ao local onde está o script
$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$wardenPath = Join-Path $baseDir "..\\03_warden\\warden_main.py"
$janitorPath = Join-Path $baseDir "..\\02_janitor-boy\\janitor-boy_main.py"

# Executar Warden
Write-Host "`n[Warden]" -ForegroundColor Yellow
python $wardenPath

Start-Sleep -Seconds 2

# Executar Janitor-Boy
Write-Host "`n[Janitor-Boy]" -ForegroundColor Green
python $janitorPath

Write-Host "`n=== Fim da Manutenção ===" -ForegroundColor Cyan
