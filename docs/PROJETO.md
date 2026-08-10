# Log Sentinel — Visão Geral do Projeto

## O Problema

Servidores web geram diariamente arquivos de log com milhões de linhas. Quando ocorre um incidente de segurança ou anomalia de tráfego, o administrador precisa investigar esses logs manualmente — uma tarefa lenta, propensa a erro e que muitas vezes envolve abrir arquivos de vários gigabytes.

Ferramentas existentes têm limitações:
- **Grafana, Prometheus**: focam em monitoramento em tempo real, não em análise post-mortem.
- **GoAccess, AWStats**: oferecem métricas gerais, mas pouco focadas em segurança.
- **Elastic SIEM**: poderoso, mas complexo e pesado para uso pontual.

## A Solução

O **Log Sentinel** preenche essa lacuna oferecendo:

- Análise **post-mortem** (sobre arquivos já existentes).
- Foco em **segurança**: detecção de força bruta, port scanning, picos anormais.
- **Leve e portátil**: roda em qualquer máquina sem dependências externas pesadas.
- Duas formas de uso:
  - **CLI** para integração em pipelines de auditoria.
  - **GUI** para investigação visual interativa.

## Público-alvo

- Administradores de servidor (sysadmins)
- Analistas de infraestrutura
- Analistas de segurança da informação
- Estudantes aprendendo análise de logs e segurança defensiva

## Diferenciais

| Característica | Log Sentinel | GoAccess | Grafana | Elastic SIEM |
|---|---|---|---|---|
| Análise post-mortem | ✅ | ✅ | ❌ | ✅ |
| Foco em segurança | ✅ | ❌ | ⚠️ | ✅ |
| GUI nativa | ✅ | ⚠️ (web) | ✅ | ✅ |
| CLI rica | ✅ | ✅ | ❌ | ⚠️ |
| Leve / portátil | ✅ | ✅ | ❌ | ❌ |
| Sem dependências externas | ✅ | ✅ | ❌ | ❌ |

## Casos de Uso Prioritários

### 1. Investigação de incidente
> Um sysadmin recebe alerta de invasão. Abre o Log Sentinel, seleciona o `access.log` da semana passada, aplica filtro de detecção de força bruta e exporta o relatório com IPs suspeitos.

### 2. Auditoria mensal automatizada
> Um analista executa via cron: `log-sentinel analyze /var/log/apache/ --output relatorio.json` e usa o JSON em outro script.

### 3. Análise visual rápida
> Um estagiário abre a GUI, arrasta vários arquivos de log e visualiza na tabela quais IPs fizeram mais requisições.

## Tecnologias

- **Python 3.12+** — linguagem principal
- **PDM** — gerenciamento de dependências
- **Typer + Rich** — CLI
- **PySide6** — GUI
- **pytest + pytest-cov** — testes
- **ruff + pyright** — qualidade de código
- **PyInstaller** — empacotamento
- **GitHub Actions** — CI/CD
- **SonarCloud** — qualidade contínua

## Métricas de Sucesso do Projeto

- ✅ 100% dos requisitos funcionais e não funcionais implementados
- ✅ Cobertura de testes ≥ 80%
- ✅ CLI e GUI com paridade de funcionalidades
- ✅ Capaz de processar arquivos de 1GB+ sem travar
- ✅ Empacotado em executável standalone para Linux e Windows
