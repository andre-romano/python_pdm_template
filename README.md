# Log Sentinel

[![CI](https://github.com/202316360036/log-sentinel/actions/workflows/ci.yaml/badge.svg)](https://github.com/202316360036/log-sentinel/actions/workflows/ci.yaml)
[![Tests](https://github.com/202316360036/log-sentinel/actions/workflows/test.yaml/badge.svg)](https://github.com/202316360036/log-sentinel/actions/workflows/test.yaml)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=AryanAssis_ENGS2&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=AryanAssis_ENGS2)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=AryanAssis_ENGS2&metric=coverage)](https://sonarcloud.io/summary/new_code?id=AryanAssis_ENGS2)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Suite de auditoria e analise post-mortem de logs Apache. Detecta padroes de ataque (forca bruta, scanner de vulnerabilidades, picos de trafego) e gera relatorios consolidados via CLI e GUI.

Projeto desenvolvido na disciplina **Engenharia de Software II** — IFBA 2026.1.

## Requisitos

- Python 3.14 ou superior
- [PDM](https://pdm-project.org/) para gerenciamento de dependencias

## Instalacao

Clonar o repositorio e instalar as dependencias:

```bash
git clone https://github.com/202316360036/log-sentinel.git
cd log-sentinel
python -m pip install pdm
pdm install
```

## Uso

### CLI

Analisar um arquivo de log Apache:

```bash
pdm run python -m python_pdm_template analyze caminho/para/arquivo.log
```

O relatorio inclui numero de linhas processadas, linhas descartadas por erro de parse, hash SHA-256 do arquivo lido e a lista de deteccoes agrupadas por tipo.

### GUI

Abrir a interface grafica:

```bash
pdm run gui
```

A janela suporta selecao de arquivo por botao ou por arrastar e soltar, com filtros por IP e por status na tabela.

## Testes

```bash
pdm run pytest
```

O comando ja gera `coverage.xml` na raiz (consumido pelo SonarCloud) e o relatorio HTML em `htmlcov/`.

## Documentacao da disciplina

- [`docs/av2/`](docs/av2) — Testes de Software.
- [`docs/av3/`](docs/av3) — Falhas de Software.
- [`docs/av5/`](docs/av5) — Riscos e Qualidade (em andamento).

## Estrutura do projeto

- [`.github/workflows/`](.github/workflows) — pipelines de CI, testes e release.
- [`src/python_pdm_template/`](src/python_pdm_template) — codigo-fonte (Core, CLI e GUI).
- [`tests/`](tests) — testes unitarios e de integracao.
- [`pyproject.toml`](pyproject.toml) — dependencias, configuracao do pytest, Pyright e Ruff.
- [`sonar-project.properties`](sonar-project.properties) — configuracao do SonarCloud.

Repositorio inicialmente baseado no template [andre-romano/python_pdm_template](https://github.com/andre-romano/python_pdm_template).
