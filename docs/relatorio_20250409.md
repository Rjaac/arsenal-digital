# 🗓️ Relatório de Atividade – 2025-04-09

## 🧱 Estrutura de Projeto Criada
**Pasta principal:** `SysAdminTools`

**Subpastas modulares para 15 agentes:**
- `01_mirror` → Inventário e snapshots
- `02_janitor-boy` → Limpeza e auditoria de software
- `03_warden` a `15_failForge` → Estrutura base com `main.py`, `config.yaml`, `README.md`

---

## 🔧 Agentes Ativos

### ✅ 01_mirror
- Recolhe dados do sistema (RAM, disco, CPU)
- Implementada recolha de software instalado via `wmic`
- Geração de ficheiros: `.json`, `.md`, `.txt`, `version.txt`
- Escreve `last_snapshot.txt` para integração com outros agentes

### ✅ 02_janitor-boy
- Lê o snapshot mais recente do `mirror`
- Carrega regras de perfil YAML (`deep_clean.yaml`)
- Aplica filtros de blacklist e palavras-chave
- Gera relatório `.md` com sugestões de desinstalação

---

## 📁 Perfis e Regras
**Criado perfil `deep_clean.yaml` com:**
- Blacklist de software
- Palavras-chave
- Placeholder para ficheiros temporários e atualizações futuras

---

## 🔃 Integração GitHub
- **Repositório criado:** [github.com/Rjaac/arsenal-digital](https://github.com/Rjaac/arsenal-digital)
- `git init`, `commit` e `push` realizados com sucesso
- `.git` ativo, histórico limpo, estrutura sincronizada

---

## 📝 Documentação
**`README.md` criado na raiz com:**
- Visão geral
- Tabela de agentes
- Instruções de uso
- Filosofia do projeto

**`.gitignore` recomendado com pastas e ficheiros a excluir**

---

## 🧠 Estado do Projeto

| **Componente**       | **Estado**       |
|-----------------------|------------------|
| Estrutura Git         | ✅ Completa      |
| `mirror.py`           | ✅ Funcional     |
| `janitor-boy.py`      | ✅ Funcional     |
| Regras YAML           | ✅ Ativo         |
| Documentação          | ✅ Base criada   |
| Testes                | 🔲 A iniciar     |
| Agentes restantes     | 🔲 Em branco (só estrutura) |
