# Prompt para gerar SLIDES.pdf via Gemini

> Para uso no Google Slides com Gemini ativado (botão *Help me create* /
> *Ajude-me a criar*). Conteúdo autoritativo está em
> [`SLIDES.md`](SLIDES.md) — este prompt é uma transcrição
> compacta para a IA gerar a versão visual.

## Como usar (5 passos)

1. Abra `slides.google.com` → **Blank presentation**.
2. Clique no botão do **Gemini** ("Help me create" / "Ajude-me a criar").
3. Cole **tudo** que está entre `===INÍCIO DO PROMPT===` e
   `===FIM DO PROMPT===` abaixo.
4. Aguarde a geração. Confira contra o **checklist** no final
   deste arquivo. Se algo divergir, peça refinamento (ver
   *Troubleshooting*).
5. **File → Download → PDF Document (.pdf)** → salve em
   `docs/av3/SLIDES.pdf` e commite.

---

## Prompt

===INÍCIO DO PROMPT===

Crie uma apresentação acadêmica de exatamente **12 slides**
intitulada "Log Sentinel — AV3" para a disciplina **Engenharia
de Software II** do IFBA, semestre 2026.1. Equipe: Elder, Aryan,
Rodrigo, Helena. Data: 17 de junho de 2026. Repositório:
`github.com/202316360036/log-sentinel`.

### Regras visuais obrigatórias

- **Estilo:** acadêmico sóbrio, NÃO comercial, NÃO "tech deck".
  O resultado deve parecer trabalho universitário sério, não
  apresentação de startup.
- **Fundo:** branco off `#FAFAFA`. **Texto principal:** `#0F172A`.
  **Texto secundário:** `#475569`.
- **Cor de destaque única:** azul acadêmico `#1E40AF` (títulos,
  números de slide, linhas de cabeçalho de tabela).
- **Vermelho:** `#B91C1C` apenas para a palavra "Crítico" e
  para alertas de severidade alta. Nunca como cor de fundo.
- **Âmbar:** `#A16207` apenas para a palavra "Parcial".
- **Verde:** `#15803D` apenas para a palavra "Ativo".
- **Tipografia:** Inter ou Source Sans Pro. Títulos de slide
  36–40pt em peso 600. Corpo 24–26pt. Tabelas 20–22pt com
  cabeçalho em negrito. Código em JetBrains Mono ou Source
  Code Pro 18–20pt. **Nada abaixo de 20pt em nenhum lugar.**
- **Numeração:** "X / 12" no canto inferior direito (cinza
  14pt), exceto na capa (slide 1), no "Obrigado" (slide 11) e
  nas Referências (slide 12).
- **Rodapé esquerdo:** "Log Sentinel — AV3 — IFBA 2026.1"
  (cinza 14pt), nos mesmos slides que têm numeração.

### Proibido (a IA tem tendência a fazer; não faça)

- **Nenhum emoji** ou pictograma colorido decorativo. Sem
  checkmark verde, ampulheta, lupa, alerta vermelho, escudo,
  cadeado, raio, foguete, etc. Use **palavras**.
- **Nenhum gradiente, glow, sombra colorida ou efeito 3D.**
- **Nenhuma stock photo** de hacker encapuzado, datacenter
  abstrato, "código matrix", cérebro digital, pessoas
  apertando mãos, mundo conectado, etc.
- **Nenhum ícone arredondado** decorativo. Apenas ícones
  funcionais discretos (caso necessário), monocromáticos.
- **Nenhuma palavra de marketing:** "inovador", "revolucionário",
  "next-gen", "potencializa", "empodera", "sinergia",
  "ecossistema", "de ponta", "transformador", "disruptivo".
- **Não invente features.** O Log Sentinel é uma ferramenta
  **offline, post-mortem**, de análise de logs Apache locais.
  NÃO mencione: TLS, mTLS, latência inferior a 100ms, ingestão
  distribuída, tempo real, 99.9% de precisão, coletores
  redundantes, microsserviços, machine learning. Nada disso
  existe no escopo.
- **Não use mais de 2 cores em um mesmo slide.**
- **Não use bordas arredondadas grandes.** Raio máximo 4px.

### Marcadores de status (substituem emojis)

Em todos os slides onde houver estado de implementação, use a
palavra em texto colorido (sem ícone, sem círculo, sem badge):

- **Ativo** — em verde `#15803D`
- **Parcial** — em âmbar `#A16207`
- **Planejado** — em cinza `#475569`
- **Crítico** — em vermelho `#B91C1C`
- **Alto** — em vermelho `#B91C1C`
- **Médio** — em âmbar `#A16207`
- **Baixo** — em cinza `#475569`

---

### CONTEÚDO DOS 12 SLIDES

#### Slide 1 — Capa (sem numeração, sem rodapé)

Centralizado verticalmente. Título grande "**Log Sentinel**" em
64pt. Subtítulo em 28pt cinza: "Análise post-mortem de logs
Apache". Três linhas em 22pt:

- "Equipe: Elder · Aryan · Rodrigo · Helena"
- "Engenharia de Software II — IFBA 2026.1"
- "Apresentação AV3 — 17 de junho de 2026"

Rodapé centralizado em 18pt: `github.com/202316360036/log-sentinel`.

Sem imagem, sem decoração.

#### Slide 2 — Visão do projeto

Título: "**Visão do projeto**".

Três parágrafos curtos:

- **Problema.** Investigar incidentes em logs Apache é lento,
  propenso a erro e exige conhecimento de regex e CLI que o
  sysadmin médio não tem tempo de manter.
- **Solução.** Suíte offline (CLI + GUI) para análise
  post-mortem. Lê logs locais, detecta padrões, exporta
  relatório JSON reproduzível com hash SHA-256 do log.
- **Escopo MVP** — fazer pouco e fazer bem:
  - Três detectores: força bruta, scanner de vulnerabilidade,
    pico de tráfego.
  - Zero requisições de rede em runtime (privacidade por design).
  - Cadeia de custódia via hash embutido no relatório.

#### Slide 3 — Pipeline e propriedades emergentes

Título: "**Pipeline e propriedades emergentes**".

À esquerda, **diagrama horizontal** em 5 caixas retangulares
de bordas finas, ligadas por setas pretas simples:

`LogFileDAO` → `ApacheParser` → `Detectores` → `Aggregator` → `ReportDAO`

Sob cada caixa, uma linha de 16pt descrevendo a função.

À direita, duas listas:

**Funcionais (PEF):**
- PEF-01 — Detecção de força bruta a partir de log bruto.
- PEF-04 — Auditoria batch consolidada (um JSON por diretório).
- PEF-05 — Paridade CLI e GUI sobre o mesmo Core.

**Não-funcionais (PENF):**
- PENF-02 — Uso de RAM até 200 MB independente do tamanho do log.
- PENF-06 — GUI não congela durante processamento (QThread).
- PENF-10 — Análise totalmente offline (validado por linter).

#### Slide 4 — Sete dimensões de confiança

Título: "**Sete dimensões de confiança**".
Subtítulo em 16pt cinza: "Avizienis, Laprie, Randell e Landwehr
(2004); ISO/IEC 25010".

Tabela com 3 colunas (Dimensão / Mecanismo principal / Estado)
e 7 linhas. Use as palavras de status coloridas conforme regra:

| Dimensão | Mecanismo principal | Estado |
|---|---|---|
| Safety | Read-only sobre o log, idempotência, S5 | Planejado |
| Security | Offline by design, B4, B5, S6, modelo de ameaças | Planejado |
| Reliability | Isolamento por arquivo, determinismo, cobertura alvo 80% | Parcial |
| Availability | App local, PyInstaller, sem deps em runtime | **Ativo** |
| Maintainability | Camadas, Strategy/Factory, ruff + pyright + Sonar | **Ativo** |
| Resilience | Parser fail-fast por linha (B2), S4, mensagens humanizadas | Planejado |
| Privacy | Offline, `--anonymize-ips`, sem telemetria | Planejado |

#### Slide 5 — Defesa em profundidade

Título: "**Defesa em profundidade — barreiras e salvaguardas**".

Duas colunas lado a lado.

**Coluna esquerda — "Barreiras (preventivas)":** lista vertical
de B0 a B8, cada uma em uma linha com identificador em negrito,
descrição curta e status à direita. Apenas **B0** marcado como
**Ativo**; B1 a B8 marcados como **Planejado**.

- B0 — Lint e type-check na CI — **Ativo**
- B1 — Validação de caminho de arquivo — Planejado
- B2 — Parser fail-fast por linha — Planejado
- B3 — Isolamento por arquivo no batch — Planejado
- B4 — Limite `--max-lines` / `--max-bytes` — Planejado
- B5 — Sanitização da saída JSON — Planejado
- B6 — GUI em QThread — Planejado
- B7 — Lint cross-layer (core → cli/gui) — Planejado
- B8 — Streaming + hash incremental — Planejado

**Coluna direita — "Salvaguardas (detecção e contenção)":**
lista de S0 a S8.

- S0 — Cobertura de testes — Parcial
- S1 — Mensagens humanizadas — Planejado
- S2 — Logging estruturado — Planejado
- S3 — Barra de progresso com aborto — Planejado
- S4 — Lista de linhas rejeitadas — Planejado
- S5 — Confirmação antes de sobrescrever — Planejado
- S6 — Hash SHA-256 do log — Planejado
- S7 — Versão do app no JSON — Planejado
- S8 — SonarCloud / SAST — **Ativo**

Rodapé do slide em itálico 16pt cinza: "Hoje só B0 e S8 estão
ativos; S0 parcial. Demais defesas mapeadas para sprints até AV5."

#### Slide 6 — Matriz Condição Latente × Defesas

Título: "**Matriz Condição Latente × Defesas**".

Tabela com 3 colunas (ID / Descrição resumida / Defesas que cobrem)
e 7 linhas:

| ID | Descrição resumida | Defesas |
|---|---|---|
| CL-01 | Regex aceita silenciosamente linha mal formada | B2 · S0 · S4 |
| CL-02 | DoS por log envenenado gigante | B1 · B4 · S3 |
| CL-03 | `.read()` causa MemoryError em log grande | B4 · B8 · S0 |
| CL-04 | GUI congela em batch longo | B6 · S1 · S3 |
| CL-05 | Script no JSON executa em visualizador web | B5 · S0 |
| CL-06 | Acoplamento core → cli/gui (regressão) | B0 · B7 · S0 |
| CL-09 | Cron sobrescreve relatório anterior | S1 · S5 · S7 |

Rodapé em itálico 16pt cinza: "Princípio: cada condição latente
é coberta por pelo menos duas defesas. Catálogo completo CL-01
a CL-10 no documento 01."

#### Slide 7 — Perigos prioritários

Título: "**Perigos prioritários**".
Subtítulo em 16pt cinza: "Leveson (2011) — STAMP/STPA; IEC 61508;
NIST SP 800-30".

Tabela com 5 colunas (ID / Perigo / Severidade / Probabilidade /
Risco) e 3 linhas. A coluna "Risco" deve estar **vermelha**
em todas as 3 linhas (todos são Crítico):

| ID | Perigo | Severidade | Probabilidade | Risco |
|---|---|---|---|---|
| **HZ-01** | Falso negativo — ataque real não detectado | Catastrófica | Ocasional | **Crítico** |
| **HZ-02** | Falso positivo — cliente legítimo acusado | Crítica | Provável | **Crítico** |
| **HZ-03** | Estouro de memória em log grande | Crítica | Provável | **Crítico** |

Abaixo da tabela, parágrafo em 20pt:

> **História breve do HZ-02.** Detector marca o crawler do
> Google como força bruta. Sysadmin bloqueia o IP. SEO da
> empresa cai por 48 horas. Mitigação: threshold configurável,
> allowlist de User-Agents, contexto do match no relatório.

#### Slide 8 — STRIDE e ataque AT-01

Título: "**Modelo de ameaças — STRIDE e ataque AT-01**".

Tabela com 3 colunas (Categoria / Onde ocorre no Log Sentinel /
Defesa principal) e 6 linhas. Destaque a linha de **Information
Disclosure** em fundo cinza claro (`#F1F5F9`):

| Categoria | Onde ocorre | Defesa principal |
|---|---|---|
| Spoofing | Substituição do binário PyInstaller publicado | Checksum em release notes |
| Tampering | Troca do log entre leitura e hash (TOCTOU) | Hash em streaming junto da leitura |
| Repudiation | Operador nega ter rodado a análise | Versão + parâmetros + timestamp (S7) |
| **Information Disclosure** | JSON com `<script>` aberto no browser | **B5 — sanitização da saída** |
| Denial of Service | Log envenenado / ReDoS no parser | B4 + regex sem backtracking |
| Elevation of Privilege | Dependência transitiva maliciosa | Dependabot + `permissions:` mínimas |

Abaixo da tabela, bloco com **borda cinza fina** (sem fundo
preenchido) descrevendo o **AT-01 Log Poisoning** em 4 passos
numerados:

1. Atacante envia requisição com User-Agent malicioso.
2. Linha é gravada no log Apache.
3. Operador abre relatório JSON em visualizador web.
4. Script executa na máquina do operador.

Linha final em negrito: "**Contramedida:** B5 — escape de `<`,
`>` e aspas na serialização JSON."

#### Slide 9 — Acompanhamento

Título: "**Acompanhamento — commits, marcos, previsões**".

Duas tabelas lado a lado.

**Esquerda — "Commits por integrante (abr–jun 2026)":**

| Integrante | Papel | Commits |
|---|---|---:|
| Elder | CI/CD, releases, docs | 9 |
| Aryan | Core (parsers, modelos) | 9 |
| Rodrigo | CLI (Typer) | 4 |
| Helena | GUI (PySide6) | 2 |

Abaixo da tabela: "**Total: 24 commits.**"

**Direita — "Marcos em 16/06/2026":**

| Marco | Data | Status |
|---|---|---|
| AV1 Ambiente | 15/04 | **Ativo** (100%) |
| AV2 Testes | 13/05 | **Ativo** (100%) |
| AV3 Documentos | 17/06 | **Ativo** (100%) |
| AV3 Demonstração | 17/06 | Parcial (30%) |
| Sprint 1 Core MVP | 13/05→08/06 | Parcial (15%) |
| AV4 Seminário | 22/07 | Planejado |
| AV5 Riscos e Qualidade | 12/08 | Planejado |

Rodapé em itálico 16pt cinza: "Reconhecemos lacuna entre 13/05
e 16/06. Plano de recuperação no GANTT atualizado."

#### Slide 10 — Demonstração e roadmap

Título: "**Demonstração e próximos passos**".

Duas colunas.

**Esquerda — "Demonstrável hoje":**

- Um teste TDD verde: `test_log_entry_armazena_campos_obrigatorios`.
- CLI esqueleto com subcomandos `analyze` e `batch`.
- GUI esqueleto `MainWindow` em PySide6.
- CI verde em `master`.
- Cinco documentos AV3 entregues em `docs/av3/`.

**Direita — "Roadmap até AV5":**

| Janela | Entrega |
|---|---|
| 16/06–30/06 | Parser + BruteForceDetector + DAO streaming + CLI real + GUI QThread |
| 01/07–15/07 | Release v0.1.0 PyInstaller (Linux + Windows) |
| 22/07 | **AV4 — Seminário** |
| 23/07–12/08 | Hardening B4/B5/B8 + S1/S5/S6; cobertura 80% |
| 12/08 | **AV5 — Riscos e Qualidade** |

Reserve no final do slide um **espaço retangular de ~400×200px**
com borda cinza tracejada e texto "Mockup de interface — a
inserir manualmente". Imagens serão coladas depois.

#### Slide 11 — Obrigado (sem numeração, sem rodapé)

Centralizado verticalmente. Apenas texto:

- Em 60pt: "**Obrigado.**"
- Em 36pt cinza, abaixo: "Perguntas?"
- Em 20pt no rodapé:
  - `github.com/202316360036/log-sentinel`
  - Branch: `docs/av3-especificacao`
  - Documentos AV3: `docs/av3/`

#### Slide 12 — Referências (sem numeração, sem rodapé)

Título: "**Referências**".

Lista numerada, fonte 20pt:

1. Reason, J. (1990). *Human Error.* Cambridge University Press.
2. Avizienis, A.; Laprie, J.-C.; Randell, B.; Landwehr, C. (2004).
   *Basic Concepts and Taxonomy of Dependable and Secure
   Computing.* IEEE TDSC, 1(1), 11–33.
3. Leveson, N. (2011). *Engineering a Safer World.* MIT Press.
4. Microsoft (1999). *STRIDE Threat Modeling.*
5. NIST SP 800-30 Rev. 1. *Guide for Conducting Risk Assessments.*
6. OWASP Top 10 (2021).
7. ISO/IEC 25010:2011 — *Software Quality Requirements and
   Evaluation.*
8. LGPD — Lei 13.709/2018.

===FIM DO PROMPT===

---

## Checklist pós-geração (antes de exportar PDF)

Confira **cada item** no deck gerado. Se algo divergir, peça
refinamento ao Gemini (ver próximo bloco).

- [ ] 12 slides exatos (nem 10, nem 14).
- [ ] **Zero emoji** em qualquer slide. Nenhum checkmark, ampulheta,
      lupa, raio, escudo, cadeado, alerta, etc.
- [ ] Status sempre em palavra colorida: "Ativo" (verde),
      "Parcial" (âmbar), "Planejado" (cinza), "Crítico" (vermelho).
- [ ] **Slide 1** (capa) e **slides 11–12** (Obrigado, Referências)
      sem numeração e sem rodapé.
- [ ] Demais slides com "X / 12" no canto inferior direito e
      rodapé "Log Sentinel — AV3 — IFBA 2026.1" à esquerda.
- [ ] **Slide 4:** só **Availability** e **Maintainability** marcadas
      como "Ativo". Reliability como "Parcial". Outras 4 como "Planejado".
- [ ] **Slide 5:** só **B0** e **S8** marcados como "Ativo". S0
      como "Parcial". Demais como "Planejado".
- [ ] **Slide 7:** **HZ-01**, **HZ-02**, **HZ-03** todos com risco
      "Crítico" em vermelho.
- [ ] **Slide 8:** linha de **Information Disclosure** destacada
      (fundo cinza claro) e contramedida "B5".
- [ ] **Slide 9:** commits **9 / 9 / 4 / 2** (total 24). Sprint 1
      marcado como "Parcial (15%)". AV4 em 22/07; AV5 em 12/08.
- [ ] **Slide 10:** placeholder retangular tracejado para a imagem
      do mockup.
- [ ] Sem stock photo de hacker, datacenter, "matrix code".
- [ ] Sem palavra "inovador", "revolucionário", "next-gen",
      "potencializa", "sinergia", "ecossistema", "transformador".
- [ ] Sem TLS, sem mTLS, sem "latência <100ms", sem "99.9% de
      precisão", sem "ingestão distribuída".
- [ ] Tipografia consistente (Inter ou Source Sans Pro) em todos
      os slides. Nada abaixo de 20pt.

Quando todos os itens estiverem OK: **File → Download → PDF
Document (.pdf)** → salvar em `docs/av3/SLIDES.pdf`.

---

## Troubleshooting — pedindo refinamento ao Gemini

Se o resultado divergir do esperado, use frases curtas e
diretas no chat do Gemini. Não reescreva o prompt inteiro.

| Problema | O que pedir |
|----------|-------------|
| Apareceu emoji em alguma tabela | "Remova todos os emojis e pictogramas de todos os slides. Use apenas texto colorido para indicar status: Ativo (verde), Parcial (âmbar), Planejado (cinza), Crítico (vermelho)." |
| Apareceu stock photo | "Remova todas as imagens de fundo, stock photos e ícones decorativos. Mantenha apenas texto e diagramas simples de caixas e setas." |
| Texto muito pequeno | "Aumente a fonte do corpo para 24pt mínimo e a fonte das tabelas para 20pt mínimo." |
| Apareceu "inovador" / "next-gen" | "Reescreva sem usar palavras de marketing como inovador, revolucionário, next-gen, potencializa, sinergia. Use linguagem técnica acadêmica." |
| Marcou tudo como Ativo no slide 5 | "No slide 5, apenas B0 e S8 devem estar marcados como Ativo. S0 como Parcial. B1 a B8 (exceto B0) e S1 a S7 todos como Planejado." |
| Inverteu HZ-01/02/03 | "No slide 7, HZ-01 é falso negativo (Catastrófica, Ocasional). HZ-02 é falso positivo (Crítica, Provável). HZ-03 é estouro de memória (Crítica, Provável). Os três têm risco Crítico." |
| Mudou números de commits | "No slide 9, os commits são: Elder 9, Aryan 9, Rodrigo 4, Helena 2. Total 24. Não invente outros números." |
| Adicionou TLS/latência | "Remova qualquer menção a TLS, mTLS, latência abaixo de 100ms, ingestão distribuída, tempo real, machine learning. O Log Sentinel é uma ferramenta offline post-mortem de logs Apache locais." |
| Bordas e gradientes coloridos | "Remova todos os gradientes, sombras coloridas e bordas arredondadas grandes. Use bordas finas pretas/cinzas com raio máximo de 4px." |

## Fonte de verdade

Se o Gemini insistir em divergir, abandone a iteração com IA
e use o markdown direto em [`SLIDES.md`](SLIDES.md) — contém o
mesmo conteúdo e pode ser convertido em PDF via Marp em um comando:

```powershell
npx @marp-team/marp-cli docs/av3/SLIDES.md --pdf `
  --allow-local-files -o docs/av3/SLIDES.pdf
```
