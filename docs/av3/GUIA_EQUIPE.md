# Guia da Equipe — Apresentação AV3

> Engenharia de Software II (IFBA 2026.1) · Equipe Log Sentinel
> **Documentação AV3 entregue: 16/06/2026** (prazo original)
> **Apresentação: 08/07/2026** (prorrogada pelo professor; original era 17/06)
> Prazo interno de preparação da demo: **06/07/2026**
> Revisão: 2026-06-18

---

## 1. Para que serve este documento

Lista do que **cada integrante deve estudar** e **fazer até 06/07** para a apresentação da AV3.

Roteiro detalhado fala-por-fala está em [`APRESENTACAO.md`](APRESENTACAO.md). Relatório consolidado em [`RELATORIO_AV3.md`](RELATORIO_AV3.md).

---

## 2. Quem faz o quê na equipe

| Integrante | Papel | Bloco(s) da apresentação |
|------------|-------|--------------------------|
| **Elder** | CI/CD, releases, documentação | 1 (abertura), 4 (dimensões), 9 (acompanhamento), 10 |
| **Aryan** | Core (motor de análise) | 5 (barreiras/salvaguardas), 8 (demo), 10 |
| **Rodrigo** | CLI (Typer + Rich) | 2 (visão), 6 (perigos), 8 (demo), 10 |
| **Helena** | GUI (PySide6) | 3 (propriedades emergentes), 7 (ameaças), 10 |

---

## 3. O que TODOS devem fazer (até 05/07)

- [ ] `git checkout master && git pull origin master`
- [ ] `pdm install` rodando sem warnings
- [ ] `pdm run pytest -q` — tem que ficar **verde**
- [ ] Ler o roteiro: [`APRESENTACAO.md`](APRESENTACAO.md)
- [ ] Ler [`docs/PROJETO.md`](../PROJETO.md) para ter a visão geral
- [ ] Saber em que documento da AV3 sua fala está embasada (tabela seção 8)

---

## 4. Elder — estudar e fazer

### Estudar
- [ ] [`03_DIMENSOES_CONFIANCA.md`](03_DIMENSOES_CONFIANCA.md) — 7 dimensões (safety, security, reliability, availability, maintainability, resilience, privacy)
- [ ] [`RELATORIO_AV3.md`](RELATORIO_AV3.md) §3, §5, §6 — commits por integrante, milestones, replanejamento
- [ ] [`GANTT.md`](../GANTT.md) atualizado

### Fazer até 06/07
- [ ] Tentar `gh auth login` e atualizar §4 e §5 do relatório com dados reais de issues/milestones
- [ ] Confirmar HDMI/adaptador/clicker para o dia da apresentação
- [ ] Ensaiar a fala dos blocos 1, 4 e 9 (≈ 6 min no total)

---

## 5. Aryan — estudar e fazer

### Estudar
- [ ] [`01_BARREIRAS_SALVAGUARDAS.md`](01_BARREIRAS_SALVAGUARDAS.md) — modelo Swiss Cheese, B0–B8, S0–S8, condições latentes
- [ ] [`docs/architecture/CORE_API.md`](../architecture/CORE_API.md) — desenho do Core (caso o professor pergunte arquitetura)
- [ ] Saber explicar **uma barreira + uma salvaguarda + uma condição latente** (B2, S6, CL-01 — conforme roteiro)

### Fazer até 06/07
- [ ] **Sprint pré-AV3 — Core** (18/06 → 30/06). Commits esperados na branch `feat/core-parser-detector`:
  - [ ] `feat(core): ApacheParser (Common + Combined Log Format)` + testes (até 22/06)
  - [ ] `feat(core): LogFileDAO com streaming + hash SHA-256` (até 23/06)
  - [ ] `feat(core): BruteForceDetector + fixture sample_brute_force.log` + teste (até 25/06)
  - [ ] `feat(core): ScannerDetector` (até 28/06)
  - [ ] `feat(core): TrafficSpikeDetector` iteração 1 (até 30/06)
  - [ ] `feat(core): Pipeline + Aggregator` (até 03/07)
- [ ] Preparar terminal para a demo: deixar `pdm run pytest -v` e `git log --oneline -10` decorados
- [ ] Ensaiar a fala do bloco 5 e a parte da demo no bloco 8 (≈ 5 min)

---

## 6. Rodrigo — estudar e fazer

### Estudar
- [ ] [`docs/PROJETO.md`](../PROJETO.md) — visão geral do projeto (bloco 2)
- [ ] [`04_PERIGOS_ACIDENTES_DANOS.md`](04_PERIGOS_ACIDENTES_DANOS.md) — Top-3 perigos (HZ-01, HZ-02, HZ-03)
- [ ] Saber contar a "história curta" do HZ-02 (falso positivo virando bloqueio injustificado de crawler)

### Fazer até 06/07
- [ ] **Sprint pré-AV3 — CLI** (22/06 → 06/07). Branch sugerida: `feat/cli-integrated`:
  - [ ] `feat(cli): analyze chama ApacheParser real` (após Aryan subir parser, ~22/06)
  - [ ] `feat(cli): detect brute-force usando BruteForceDetector + saída Rich` (até 27/06)
  - [ ] `feat(cli): batch processa diretório com --output json` (até 02/07)
  - [ ] `feat(cli): --anonymize-ips e --max-lines` (até 05/07)
- [ ] Preparar para a demo: `python -m python_pdm_template.cli.main analyze tests/fixtures/sample_brute_force.log`
- [ ] Ensaiar a fala dos blocos 2 e 6 (≈ 5 min)

---

## 7. Helena — estudar e fazer

### Estudar
- [ ] [`02_PROPRIEDADES_EMERGENTES.md`](02_PROPRIEDADES_EMERGENTES.md) — PEFs (PEF-01, PEF-04, PEF-05) e PENFs (PENF-02, PENF-06, PENF-10)
- [ ] [`05_AMEACAS_VULNERABILIDADES.md`](05_AMEACAS_VULNERABILIDADES.md) — STRIDE + ataque AT-01 (log poisoning via User-Agent)
- [ ] Saber explicar o conceito de "propriedade emergente" em 1 frase

### Fazer até 06/07
- [ ] **Sprint pré-AV3 — GUI** (20/06 → 06/07). Branch sugerida: `feat/gui-worker`:
  - [ ] `feat(gui): entry point pdm run gui` no `pyproject.toml` (até 20/06) — evita o one-liner gigante na demo
  - [ ] `feat(gui): QThread worker chamando ApacheParser` (até 25/06)
  - [ ] `feat(gui): QTableView com colunas IP/timestamp/método/status` (até 26/06)
  - [ ] `feat(gui): drag&drop de arquivo .log` (até 30/06)
  - [ ] `feat(gui): filtros básicos por IP/status` (até 01/07)
- [ ] Ensaiar a fala dos blocos 3 e 7 (≈ 6 min)

---

## 8. Mapa rápido: qual documento embasa qual fala

| Bloco | Quem fala | Documento principal |
|-------|-----------|---------------------|
| 1. Abertura | Elder | — |
| 2. Visão do projeto | Rodrigo | [`docs/PROJETO.md`](../PROJETO.md) |
| 3. Propriedades emergentes | Helena | [`02_PROPRIEDADES_EMERGENTES.md`](02_PROPRIEDADES_EMERGENTES.md) |
| 4. Dimensões de confiança | Elder | [`03_DIMENSOES_CONFIANCA.md`](03_DIMENSOES_CONFIANCA.md) |
| 5. Barreiras e salvaguardas | Aryan | [`01_BARREIRAS_SALVAGUARDAS.md`](01_BARREIRAS_SALVAGUARDAS.md) |
| 6. Perigos, acidentes, danos | Rodrigo | [`04_PERIGOS_ACIDENTES_DANOS.md`](04_PERIGOS_ACIDENTES_DANOS.md) |
| 7. Ameaças e vulnerabilidades | Helena | [`05_AMEACAS_VULNERABILIDADES.md`](05_AMEACAS_VULNERABILIDADES.md) |
| 8. Demonstração | Aryan + Rodrigo | [`RELATORIO_AV3.md`](RELATORIO_AV3.md) §7 |
| 9. Acompanhamento | Elder | [`RELATORIO_AV3.md`](RELATORIO_AV3.md) §3–§6 + [`GANTT.md`](../GANTT.md) |
| 10. Próximos passos | Todos | — |

---

## 9. Ensaio geral — 07/07

- [ ] Reunião da equipe com cronômetro
- [ ] Rodar a apresentação inteira pelo menos 1x (alvo: 25 min)
- [ ] Revisar transições entre blocos (cada um sabe o que o próximo vai dizer)
- [ ] Conferir slides (se tiverem sido feitos) commitados em `docs/av3/SLIDES.pdf`
