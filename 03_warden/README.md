# 🛡️ WARDEN – System Integrity Watchdog

**Versão:** 0.2  
**Autor:** ChatGPT / Marty  
**Data de criação:** 2025-04-10  
**Projeto:** DONA_LAPTOP_ONE → SysAdminTools → 03_warden

---

## 📌 Objetivo

O `warden` é um agente de monitorização da integridade do sistema. Atua como sentinela, vigiando ficheiros e diretórios críticos. O seu papel é detetar alterações inesperadas — como modificações, eliminações ou criações — e gerar alertas para o utilizador ou para outros módulos da suite SysAdminTools.

---

## 🧱 Estrutura do Projeto

```
03_warden/
├── main.py              # Script principal de execução
├── config.yaml          # Parâmetros de configuração (intervalos, opções)
├── rules/               # Regras e listas de vigilância (ex: watchlist.json)
├── logs/                # Registos de execução, alertas e relatórios
└── README.md            # Documento descritivo do agente
```

---

## 🔧 Funcionalidades (v0.2)

- Leitura de configurações gerais a partir de `config.yaml`
- Leitura de ficheiros de regras personalizados (ex: `watchlist.json`)
- Cálculo do hash SHA256 de cada ficheiro monitorizado
- Comparação com valores anteriores (baseline)
- Geração de alertas simples via log (`logs/warden_log.txt`)
- Exportação dos resultados do scan para `.json` e `.md`

---

## 📌 Caminho Futuro (v0.3+)

- Integração com `mirror.py` como baseline de referência
- Geração de relatórios semanais de integridade
- Detecção de permissões perigosas
- Notificações em tempo real (sistema / email)
- "Modo Paranoico" com alertas verbosos e reação automática

---

## 🔐 Nota

Este agente **não modifica** ficheiros — apenas observa. É o observador silencioso que toma nota de tudo… e reporta.

> “Quem vigia os vigilantes? Neste caso, tu. Mas com ajuda.” – Marty

