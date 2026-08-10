# Dimensões de Confiança (Trustworthiness)

> Documento AV3 — Engenharia de Software II (IFBA 2026.1)
> Projeto: **Log Sentinel**
> Base teórica: Avizienis, Laprie, Randell & Landwehr (2004) — *Basic Concepts and Taxonomy of Dependable and Secure Computing* — e ISO/IEC 25010.

---

## 1. Por que falamos de "confiança" e não só de "qualidade"

Um software que processa **logs de produção e ajuda a investigar incidentes de segurança** será usado para tomar decisões com consequências reais — bloquear um IP, abrir um chamado, registrar evidência num processo. O usuário não precisa apenas de um software *que funciona*; precisa de um software **em que pode confiar**.

A literatura clássica decompõe "confiança" em sete dimensões interligadas. Este documento define **cada dimensão**, **como o Log Sentinel a sustenta** e **como ela é verificável** (assim a confiança não fica como discurso).

---

## 2. As sete dimensões aplicadas ao Log Sentinel

### 2.1 **Safety** (segurança operacional / ausência de dano não intencional)

**Definição:** propriedade de não causar dano físico ou material por mau funcionamento.

**Como o Log Sentinel a sustenta:**
- Modo **read-only** sobre os arquivos de log: jamais escreve, renomeia ou remove o log analisado.
- Pipeline **idempotente**: rodar 2× sobre o mesmo log produz o mesmo relatório.
- Saída sempre em arquivo novo (com confirmação se já existir — salvaguarda **S5** do [doc 01](01_BARREIRAS_SALVAGUARDAS.md)).

**Como verificamos:**
- Teste que confere `mtime`/`hash` do log de entrada antes e depois da execução.
- Análise estática: nenhum `open(..., 'w')`/`'a'` sobre o caminho do log de entrada (lint customizado).

---

### 2.2 **Security** (proteção contra ações maliciosas)

**Definição:** integridade, confidencialidade e disponibilidade frente a adversários.

**Como sustenta:**
- **Análise offline**: nenhum dado de log sai da máquina (sem telemetria, sem chamadas de rede).
- **Sanitização da saída** (barreira B5): payloads em `User-Agent` ou `Referer` não conseguem executar script ao serem renderizados em visualizadores.
- **Limite de input** (B4): protege contra log envenenado de tamanho extremo.
- **Cadeia de custódia** (S6): hash SHA-256 do log no relatório.
- Documento [05 — Ameaças e vulnerabilidades](05_AMEACAS_VULNERABILIDADES.md) detalha o modelo de ameaça completo.

**Como verificamos:**
- Linter falha CI se algum módulo de rede (`requests`, `urllib`, `socket`, ...) for importado em `core/`.
- Teste de fuzzing leve no parser com linhas malformadas e payloads injetados.
- Scans de dependências (Dependabot/SonarCloud).

---

### 2.3 **Reliability** (confiabilidade — continuidade de serviço correto)

**Definição:** probabilidade de operação correta durante um intervalo de tempo.

**Como sustenta:**
- **Isolamento por arquivo** no batch (B3): exceção num arquivo não derruba os outros.
- **Determinismo**: ordenação estável + saída canonicalizada → mesmo input ⇒ mesmo output.
- **Cobertura ≥ 80%** com testes unitários, de integração e snapshot.
- **TDD** desde o início (commit `bfeafd7` adiciona o primeiro teste antes do MVP).

**Como verificamos:**
- `pytest --cov` no CI bloqueia merge se cobertura cair.
- Snapshot tests detectam regressão de saída.
- Build em matrix (Linux + Windows) confirma comportamento idêntico.

---

### 2.4 **Availability** (disponibilidade)

**Definição:** prontidão para uso quando solicitado.

**Como sustenta:**
- **Aplicação local de invocação imediata** (CLI single-shot ou GUI desktop) — não há servidor que possa cair.
- **Sem dependências externas em tempo de execução**: PDM resolve deps na instalação, mas a execução é offline.
- **Empacotamento standalone (PyInstaller)**: usuário pode rodar mesmo sem Python instalado.

**Como verificamos:**
- Smoke test que executa o binário PyInstaller numa VM limpa (sem Python global) e confere exit code 0.
- Tempo de cold-start medido em CI: deve abrir GUI em < 3 s.

---

### 2.5 **Maintainability** (manutenibilidade)

**Definição:** facilidade de evoluir, corrigir e adaptar.

**Como sustenta:**
- **Arquitetura em camadas** com Core 100% isolado (RNF-01) — ver [ARQUITETURA.md](../architecture/ARQUITETURA.md).
- **Padrões de projeto** explícitos: Strategy (parsers), Factory (parser/DAO), Pipe-and-Filter (pipeline), Facade (`LogAnalyzer`), Observer (eventos de progresso).
- **Convenções** documentadas em [team/CONVENCOES.md](../team/CONVENCOES.md).
- **CI** com `ruff` + `pyright` impede entrada de código não conforme.
- **Documentação por pasta** (`README.md` em cada subdiretório).

**Como verificamos:**
- Métrica do SonarCloud: dívida técnica, code smells, complexidade ciclomática.
- Time-to-add-new-detector medido manualmente em retros: meta < 1 dia.

---

### 2.6 **Resilience** (resiliência — recuperação após perturbação)

**Definição:** capacidade de degradar com graça e recuperar-se de eventos inesperados.

**Como sustenta:**
- **Parser fail-fast por linha** (B2): linha inválida vira `ParseError` registrada (S4), processamento continua.
- **Pipeline encerra com relatório parcial** se interrompido — não tudo-ou-nada.
- **Mensagens de erro humanizadas** (S1) orientam o operador a corrigir e refazer.
- Modo `--continue-from <offset>` (planejado pós-MVP) para retomar processamento longo.

**Como verificamos:**
- Teste de injeção de falhas (`pyfaultinjection`/manual): corrompe trecho do log e confere relatório parcial.
- Teste de `Ctrl+C` no meio do batch: arquivos já processados aparecem no relatório.

---

### 2.7 **Privacy** (privacidade)

**Definição:** controle do que é coletado, retido e exposto sobre indivíduos.

**Como sustenta:**
- **Zero telemetria.** Nenhuma informação é enviada a servidores remotos.
- **Logs nunca saem da máquina do operador**, mesmo em caso de erro (sem relatório automático de crash).
- **Mascaramento opcional de IPs** no relatório exportado (flag `--anonymize-ips` planejada) — útil quando o relatório será compartilhado com terceiros.
- Mensagens de erro **não embutem caminho absoluto do home do usuário** quando rodando em modo `--anonymize`.

**Como verificamos:**
- Inspeção das saídas do app com `strings`/`grep` em busca de hostnames/usernames quando flag de anonimização ativa.
- Revisão manual periódica do README e relatórios para evitar exposição.

---

## 3. Resumo executivo

| # | Dimensão | Mecanismos principais | Estado da implementação |
|---|----------|------------------------|---------------------------|
| 1 | Safety | Read-only, idempotência, S5 | ⏳ parcial — a finalizar com batch |
| 2 | Security | Offline, B4, B5, S6, threat model dedicado | ⏳ parcial |
| 3 | Reliability | B3, determinismo, cobertura ≥ 80% | 🔄 em construção |
| 4 | Availability | App local, PyInstaller, sem deps de runtime | ✅ pipeline pronto |
| 5 | Maintainability | Camadas, padrões, ruff/pyright/Sonar | ✅ infra pronta, MVP em construção |
| 6 | Resilience | B2, S4, mensagens humanizadas | ⏳ planejado |
| 7 | Privacy | Offline by design, `--anonymize-ips` | ⏳ flag a implementar |

Legenda: ✅ pronto · 🔄 parcial em uso · ⏳ planejado / a implementar.

---

## 4. Trade-offs assumidos conscientemente

Confiança não vem de graça — sempre há tensão entre dimensões. Documentamos as escolhas:

| Trade-off | Escolhemos por | A custo de |
|---|---|---|
| Streaming (gera-uma-linha-por-vez) vs carregamento total | Memória baixa (PENF-02) e tolerância a logs gigantes | Algumas métricas exigem segunda passada — custo aceitável |
| Determinismo (snapshot tests) vs flexibilidade de output | Confiabilidade auditável | Tornar mudanças de formato mais cerimoniosas |
| Offline (sem rede) vs enriquecimento (GeoIP via API) | Privacy e security por padrão | Quem quiser geolocalização precisará de plugin opcional |
| Fail-fast por linha vs aborto total na primeira falha | Resilience (relatório parcial vale mais que zero) | Operador precisa olhar a lista de descartes (S4) |
| Read-only sobre o log vs ferramentas que reescrevem | Safety e cadeia de custódia | Não rotacionamos, nem deduplicamos linhas no próprio log |

---

## 5. Relação com as outras pautas da AV3

- As **propriedades emergentes** ([doc 02](02_PROPRIEDADES_EMERGENTES.md)) são a *evidência observável* destas dimensões. Ex.: PENF-02 (RAM ≤ 200 MB) é evidência de **availability** e **resilience**.
- As **barreiras e salvaguardas** ([doc 01](01_BARREIRAS_SALVAGUARDAS.md)) são os *mecanismos concretos* que sustentam cada dimensão.
- O documento [04 — Perigos, Acidentes e Danos](04_PERIGOS_ACIDENTES_DANOS.md) descreve **o que perdemos** quando uma dimensão falha.
- O documento [05 — Ameaças e Vulnerabilidades](05_AMEACAS_VULNERABILIDADES.md) foca em **security**, expandindo a dimensão 2.2.

## 6. Referências

- Avizienis, A.; Laprie, J.-C.; Randell, B.; Landwehr, C. (2004). *Basic Concepts and Taxonomy of Dependable and Secure Computing.* IEEE TDSC, 1(1), 11–33.
- ISO/IEC 25010:2011 — Systems and software Quality Requirements and Evaluation (SQuaRE).
- NIST SP 800-160 Vol.2 — *Developing Cyber-Resilient Systems.*
- LGPD (Lei 13.709/2018) — base para a dimensão de privacidade.
