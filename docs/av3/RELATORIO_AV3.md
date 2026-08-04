# Relatório Consolidado — AV3

> Engenharia de Software II (IFBA 2026.1) · Equipe Log Sentinel
> Data de elaboração: 2026-06-10 · **Entrega congelada: 2026-06-16** (prazo original do professor)
> Última revisão: 2026-06-18 (consolidação pós-entrega)
> **Apresentação:** 2026-07-08 (prorrogada pelo professor; o pacote documental abaixo permanece fechado em 16/06)

---

## 1. Identificação do projeto

- **Nome:** Log Sentinel
- **Repositório:** https://github.com/202316360036/log-sentinel
- **Branch principal:** `master`
- **Branch desta entrega (AV3):** `docs/av3-especificacao`
- **CI status:** verde (lint, tests, build) — ver badges no [README](../../README.md)
- **Documentação geral:** [docs/PROJETO.md](../PROJETO.md)
- **Arquitetura:** [docs/architecture/ARQUITETURA.md](../architecture/ARQUITETURA.md)

---

## 2. Entregáveis AV3 (mapeamento)

| Entregável solicitado | Documento | Estado |
|------------------------|-----------|--------|
| Barreiras, salvaguardas e condições latentes | [01_BARREIRAS_SALVAGUARDAS.md](01_BARREIRAS_SALVAGUARDAS.md) | ✅ entregue |
| Propriedades emergentes funcionais e não-funcionais | [02_PROPRIEDADES_EMERGENTES.md](02_PROPRIEDADES_EMERGENTES.md) | ✅ entregue |
| Dimensões de confiança do sistema | [03_DIMENSOES_CONFIANCA.md](03_DIMENSOES_CONFIANCA.md) | ✅ entregue |
| Perigos, acidentes e danos | [04_PERIGOS_ACIDENTES_DANOS.md](04_PERIGOS_ACIDENTES_DANOS.md) | ✅ entregue |
| Ativos, vulnerabilidades, ataques, ameaças, exposições | [05_AMEACAS_VULNERABILIDADES.md](05_AMEACAS_VULNERABILIDADES.md) | ✅ entregue |
| Link do GitHub | seção 1 deste doc | ✅ |
| Quantidade de commits por integrante | seção 3 deste doc | ✅ |
| Issues finalizados | seção 4 deste doc | ✅ |
| Percentuais dos milestones | seção 5 deste doc | ✅ |
| Atualização das previsões | seção 6 deste doc + [GANTT.md](../GANTT.md) | ✅ |
| Demonstração breve do app | seção 7 deste doc | ⚠️ esqueletos CLI+GUI (assumido honestamente) |
| Roteiro da apresentação | [APRESENTACAO.md](APRESENTACAO.md) · [SLIDES.md](SLIDES.md) | ✅ |

---

## 3. Commits por integrante

> Fonte: `git shortlog -sn --all --no-merges --since=2026-04-01 --until=2026-06-17`
> Corte: 2026-06-16 (entrega original). Reexecutado em 2026-06-18 para conferência.

| Integrante | Papel principal | Commits | Observação |
|------------|------------------|--------:|------------|
| **Elder** (`202316360036`) | CI/CD, releases, documentação | **9** | inclui setup do PyInstaller, SonarCloud opcional, fix de ruff/pyright, docs AV2 |
| **Aryan Souza Assis** | Core (parsers, modelos) | **9** | inclui commit inicial e setup de SonarCloud; primeiro `LogEntry` + TDD (8 commits + 1 com config local diferente "Aryan Assis") |
| **Rodrigo Cruz** | CLI (Typer) | **4** | pacote CLI + esqueleto `analyze`/`batch` |
| **Helena Santos Freitas** | GUI (PySide6) | **2** | pacote GUI + esqueleto `MainWindow` |

Notas:
- `Andre` (1 commit) é o autor do **template** original (`andre-romano/python_pdm_template`); **não conta** como integrante da equipe.
- `Aryan Assis` (1 commit "Add as coisas") é a mesma pessoa que `Aryan Souza Assis` — autoria duplicada por config local de git diferente. Total real do Aryan: **9 commits**.

**Total da equipe (sem o template): 24 commits** entre 08/04/2026 e 12/05/2026.

> ⚠️ Lacuna evidente: **nenhum commit de código entre 13/05 e 16/06**. O grupo precisa retomar trabalho de Core/CLI/GUI; o replanejamento (Sprint pré-AV3) está na seção 6, viabilizado pela prorrogação do professor.

Detalhe individual por commit em [APENDICE_COMMITS.md](APENDICE_COMMITS.md).

---

## 4. Issues finalizadas

> Fonte: `gh issue list --repo 202316360036/log-sentinel --state all --limit 200 --json number,title,state,assignees,milestone,closedAt,labels`
> Corte: 2026-06-16T23:59:59Z (entrega original da AV3).

**Síntese até 16/06/2026:**

| Métrica | Valor |
|---------|------:|
| Issues abertas no período (08/04 → 16/06) | **25** |
| Issues fechadas até 16/06 | **12** |
| Issues ainda abertas em 16/06 | **13** |

**Issues fechadas por integrante (assignees em 16/06):**

| Integrante | Fechadas | Issues |
|------------|---------:|--------|
| **Elder** | 8 | #8 fork template, #9 badges CI, #10 PyInstaller workflow, #11 SonarCloud opcional, #12 ruff D104, #13 página HTML estudo, #14 migrar conteúdo, #18 SonarCloud config |
| **Rodrigo Cruz** | 2 | #6 pacote CLI, #7 Typer `analyze`/`batch` |
| **Aryan Souza Assis** | 0 | — (todas Core ainda abertas: #19-#23) |
| **Helena Santos Freitas** | 0 | — (#15 MainWindow e #17 drag&drop abertas) |
| Marcos AV (sem assignee) | 2 | #1 AV1, #2 AV2 |

**Issues abertas em 16/06 (compromisso pós-entrega):**

- **Core (Aryan):** #19 `LogEntry`, #20 `ApacheLogParser`, #21 `BruteForceDetector`, #22 `ScannerDetector`, #23 `LogFileDAO`/`ReportDAO`.
- **CLI (Rodrigo):** #16 `analyze` real com filtros.
- **GUI (Helena):** #15 esqueleto `MainWindow` (entregue como esqueleto, marcador segue aberto até integração), #17 drag&drop.
- **Marcos:** #3 AV3 (será fechada após apresentação 08/07), #4 AV4, #5 AV5.

> Comparativo de produtividade declarada x entregue está em [APENDICE_COMMITS.md](APENDICE_COMMITS.md). A discrepância Aryan (9 commits / 0 issues fechadas) indica trabalho não rastreado por issue — boa prática a corrigir na sprint pré-AV3.

---

## 5. Percentuais dos milestones

> Fonte: `gh api 'repos/202316360036/log-sentinel/milestones?state=all' --jq '.[] | {title, state, open_issues, closed_issues, due_on}'`
> Corte: 2026-06-16.

| # | Milestone | Due | Closed | Open | % real | Estado |
|---|-----------|-----|-------:|-----:|-------:|--------|
| 1 | **AV1 - AMBIENTE** | 14/04/2026 | 1 | 0 | **100%** | ✅ fechada |
| 6 | **Sprint 0 - Setup & Documentação** | 11/05/2026 | 9 | 0 | **100%** | ✅ fechada |
| 2 | **AV2** | 12/05/2026 | 1 | 0 | **100%** | ✅ entregue (issue ainda aberta) |
| 7 | **Sprint 1 - Core MVP** | 08/06/2026 | 1 | 5 | **17%** | ⚠️ atrasada |
| 3 | **AV3 - FALHAS DE SOFTWARE** | 16/06/2026 | 0 | 1 | **0%** (issue rastreadora) → docs 100% entregues | 🟡 entregue (docs); demo na sprint pré-AV3 |
| 8 | **Sprint 2 - CLI & GUI** | 30/06/2026 | 0 | 3 | **0%** | ⏳ no prazo |
| 4 | **AV4 - SEMINÁRIO** | 22/07/2026 (sem due no GH) | 0 | 1 | **0%** | ⏳ no prazo |
| 5 | **AV5 - RISCOS E QUALIDADE** | 11/08/2026 | 0 | 1 | **0%** | ⏳ no prazo |
| 9 | **Sprint 3 - Polimento & Release** | 12/08/2026 | 0 | 0 | — | ⏳ a planejar |

**Leitura crítica:**
- Marcos **acadêmicos** (AV1, AV2, Sprint 0) estão 100%.
- Sprint 1 (Core MVP) com **17%** explica a demo em esqueleto — corrigida pela sprint pré-AV3 (§6.2).
- A milestone AV3 do GitHub ficará aberta até a apresentação (08/07); a entrega documental, no entanto, foi congelada em 16/06.

---

## 6. Atualização das previsões de entrega

### 6.1 Diagnóstico (corte 16/06, validado em 18/06)
- AV1, AV2 e Sprint 0 fechadas em 100%. ✅
- AV3 (este documento): **docs 100% entregues no prazo original (16/06)**; demo permanece em esqueleto.
- **Sprint 1 (Core MVP) em 17%**: 1 de 6 issues fechada — só `LogEntry` + teste TDD.
- **Sprint 1.5 de recuperação (11–14/06) NÃO foi cumprida**: zero commits de código entre 13/05 e 16/06.
- **Prorrogação:** o professor adiou a apresentação de 17/06 para **08/07/2026**. A equipe ganhou 21 dias para fechar a demo, mas a entrega documental abaixo permanece no prazo original.

### 6.2 Replanejamento para chegar à AV3 (Sprint pré-AV3 — 18/06 → 06/07)

| Período | Foco | Responsável |
|---------|------|-------------|
| **18/06 (hoje)** | Atualizar GANTT + relatório com novo prazo; abrir 1 issue por integrante | Elder |
| **18/06 → 22/06** | `ApacheParser` (Common + Combined) + testes unitários | Aryan |
| **19/06 → 23/06** | `LogFileDAO` streaming linha-a-linha + hash SHA-256 | Aryan |
| **20/06** | Criar entry point `pdm run gui` no `pyproject.toml` | Helena |
| **22/06** | `BruteForceDetector` (janela de tempo + threshold) + teste com `tests/fixtures/sample_brute_force.log` | Aryan |
| **22/06 → 25/06** | CLI `analyze` real (substitui stub) chamando ApacheParser | Rodrigo |
| **23/06 → 26/06** | GUI: QThread worker + QTableView com resultados do parser | Helena |
| **25/06 → 27/06** | CLI `detect brute-force` + saída Rich | Rodrigo |
| **26/06 → 30/06** | `ScannerDetector` + 1ª iteração de `TrafficSpikeDetector` | Aryan |
| **27/06 → 01/07** | GUI: drag&drop de `.log` + filtros básicos | Helena |
| **27/06 → 02/07** | CLI `batch` + `--output json` | Rodrigo |
| **01/07 → 03/07** | `Pipeline` + `Aggregator` consolidando detectores | Aryan |
| **02/07 → 05/07** | Flags hardening CLI (`--anonymize-ips`, `--max-lines`) | Rodrigo |
| **05/07** | Branch protection no `master` + atualizar `APENDICE_COMMITS.md` | Elder |
| **06/07** | Smoke test E2E (CLI + GUI sobre fixtures) + gravar demo curta (3 min) | todos |
| **07/07** | Ensaio da apresentação cronometrado (alvo 25 min); revisar slides | todos |
| **08/07** | **Apresentação AV3** 🎯 | todos |

### 6.3 Replanejamento para AV4 / AV5 (após 08/07)

| Período | Entrega | Responsável |
|---------|---------|-------------|
| 09/07 → 22/07 | Detectores complementares + Aggregator final | Aryan |
| 09/07 → 22/07 | CLI completa (`--format`, paginação Rich) | Rodrigo |
| 09/07 → 22/07 | GUI: exportar JSON + barra de progresso | Helena |
| 15/07 → 29/07 | PyInstaller release v0.1.0 (Linux + Windows) | Elder |
| 15/07 → 22/07 | Preparar AV4 (Seminário) | todos |
| 22/07 → 12/08 | Hardening (B4/B5/S1/S5/S6/anonymize) + cobertura ≥ 80% para AV5 | Aryan + Elder |

---

## 7. Demonstração breve do app — estado em 2026-06-16

### O que **roda** hoje
```bash
# CLI (esqueleto Typer)
pdm run python -m python_pdm_template --help                # ainda printa "Hello"
pdm run python -m python_pdm_template.cli.main --help       # mostra subcomandos analyze e batch
pdm run python -m python_pdm_template.cli.main analyze access.log
# Saída: "Analisando access.log... (nao implementado ainda)"

# GUI (esqueleto PySide6)
pdm run python -c "from python_pdm_template.gui.main_window import MainWindow; from PySide6.QtWidgets import QApplication; import sys; a=QApplication(sys.argv); w=MainWindow(); w.show(); a.exec()"
# Abre janela 1024x768 com texto "Em construcao"

# Testes
pdm run pytest -q
# 1 teste verde: test_log_entry_armazena_campos_obrigatorios
```

### Roteiro de demo (3 min) — versão mínima honesta
1. **Abrir terminal** e mostrar `git log --oneline -10` (ritmo do projeto).
2. **CLI:** rodar `--help` mostrando os 2 subcomandos planejados.
3. **GUI:** abrir a janela vazia e dizer "esqueleto pronto, próxima sprint conecta ao Core".
4. **Testes:** rodar `pytest` e mostrar a saída verde + `--cov`.
5. **Pipeline CI:** abrir a aba Actions no GitHub mostrando build verde.
6. **Docs AV3:** abrir os 5 documentos novos no GitHub.

### Se até 06/07 o Core estiver pronto (sprint pré-AV3, §6.2), substituir os passos 2 e 3 por:
1. Mostrar análise real de `tests/fixtures/sample_brute_force.log` na CLI.
2. Reproduzir a mesma análise na GUI (paridade — propriedade emergente PEF-05).
3. Exportar JSON e mostrar hash + versão (cadeia de custódia).

---

## 8. Onde está cada documento

```
docs/
├── PROJETO.md              ← visão geral
├── ESCOPO.md               ← in/out scope
├── REQUISITOS.md           ← RF/RNF
├── CASOS_DE_USO.md
├── GANTT.md                ← cronograma (atualizado)
├── architecture/
│   ├── ARQUITETURA.md
│   ├── CORE_API.md
│   ├── CLI_DESIGN.md
│   └── GUI_DESIGN.md
├── testing/
│   ├── ESTRATEGIA_TESTES.md
│   └── CRITERIOS_ACEITACAO.md
├── team/
│   ├── PAPEIS.md
│   └── CONVENCOES.md
└── av3/                    ← ENTREGA DESTA AVALIAÇÃO
    ├── 01_BARREIRAS_SALVAGUARDAS.md
    ├── 02_PROPRIEDADES_EMERGENTES.md
    ├── 03_DIMENSOES_CONFIANCA.md
    ├── 04_PERIGOS_ACIDENTES_DANOS.md
    ├── 05_AMEACAS_VULNERABILIDADES.md
    ├── APRESENTACAO.md
    ├── APENDICE_COMMITS.md
    └── RELATORIO_AV3.md    ← (este arquivo)
```
