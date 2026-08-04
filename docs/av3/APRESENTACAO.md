# Roteiro da Apresentação — AV3

> Engenharia de Software II (IFBA 2026.1) · Equipe Log Sentinel
> Duração-alvo: **25 min** (margem dentro da janela 20–30 min) + 5 min Q&A
> Avaliação individual e em grupo → **todos apresentam**.

---

## 1. Estrutura geral

| Bloco | Min | Apresentador | Conteúdo central |
|-------|----:|--------------|-------------------|
| 1. Abertura | 1 | Elder | Apresentar equipe, contexto da AV3 |
| 2. Visão do projeto | 2 | Rodrigo | Problema, solução, escopo (slide PROJETO) |
| 3. Propriedades emergentes | 3 | Helena | PEF e PENF do [doc 02](02_PROPRIEDADES_EMERGENTES.md) |
| 4. Dimensões de confiança | 3 | Elder | 7 dimensões do [doc 03](03_DIMENSOES_CONFIANCA.md) |
| 5. Barreiras, salvaguardas, condições latentes | 4 | Aryan | Modelo Swiss Cheese aplicado ([doc 01](01_BARREIRAS_SALVAGUARDAS.md)) |
| 6. Perigos, acidentes, danos | 3 | Rodrigo | Top-5 perigos críticos ([doc 04](04_PERIGOS_ACIDENTES_DANOS.md)) |
| 7. Ameaças e vulnerabilidades | 3 | Helena | STRIDE, ataques AT-01 a AT-05 ([doc 05](05_AMEACAS_VULNERABILIDADES.md)) |
| 8. Demonstração | 3 | Aryan + Rodrigo | Estado do app (vide [RELATORIO_AV3 §7](RELATORIO_AV3.md#7-demonstração-breve-do-app--estado-atual-2026-06-10)) |
| 9. Acompanhamento (commits, milestones, previsões) | 2 | Elder | Tabelas do [RELATORIO_AV3 §3-§6](RELATORIO_AV3.md) |
| 10. Próximos passos e fechamento | 1 | todos (1 frase cada) | Plano até AV4 |

**Total: 25 min**.

---

## 2. Roteiro detalhado — fala por fala

### Bloco 1 — Abertura (Elder, 1 min)
> "Boa-tarde, professor. Somos a equipe do Log Sentinel — eu sou o Elder, e estão comigo o Aryan, o Rodrigo e a Helena. Hoje vamos apresentar nossa entrega da AV3, que cobre falhas, ameaças e dimensões de confiança aplicadas ao nosso projeto."

Mostrar: slide com nomes + repo `https://github.com/202316360036/log-sentinel`.

### Bloco 2 — Visão do projeto (Rodrigo, 2 min)
- Problema: investigar incidentes em logs Apache é lento e propenso a erro.
- Solução: análise post-mortem, leve, com CLI + GUI.
- Escopo recortado para "fazer pouco e fazer bem". Citar 3 detectores: força bruta, scanner, picos.

Mostrar: slide PROJETO.md (resumo).

### Bloco 3 — Propriedades emergentes (Helena, 3 min)
- Conceito em 1 frase: "capacidade que só existe quando os componentes operam juntos".
- Mostrar diagrama do pipeline (DAO → Parser → Detector → Aggregator → DAO).
- 3 exemplos funcionais: PEF-01 (força bruta), PEF-04 (consolidação batch), PEF-05 (paridade CLI↔GUI).
- 3 exemplos não-funcionais: PENF-02 (RAM ≤ 200 MB), PENF-06 (GUI não congela), PENF-10 (offline by design).

### Bloco 4 — Dimensões de confiança (Elder, 3 min)
- 7 dimensões: safety, security, reliability, availability, maintainability, resilience, privacy.
- Para cada uma, **uma frase** dizendo como o Log Sentinel a sustenta.
- Destaque honesto: maturidade hoje varia (Maintainability ✅, Reliability 🔄, demais ⏳).
- Mostrar a tabela do [doc 03 §3](03_DIMENSOES_CONFIANCA.md#3-resumo-executivo).

### Bloco 5 — Barreiras, salvaguardas, condições latentes (Aryan, 4 min)
- Mostrar o diagrama de camadas defensivas (B0..B8, S0..S8).
- Explicar **uma barreira + uma salvaguarda + uma condição latente**:
  - **B2 (parser fail-fast por linha)** — preventiva.
  - **S6 (hash SHA-256 do log)** — cadeia de custódia.
  - **CL-01 (regex pode aceitar linha mal formada)** — vulnerabilidade dormente.
- Mostrar a matriz CL × B/S do [doc 01 §6](01_BARREIRAS_SALVAGUARDAS.md#6-matriz-barreira--condição-latente): cada condição é coberta por ≥ 2 defesas.

### Bloco 6 — Perigos, acidentes, danos (Rodrigo, 3 min)
- Diferença entre **perigo** (potencial), **acidente** (evento), **dano** (consequência).
- Top-3 perigos críticos: HZ-01 (falso negativo), HZ-02 (falso positivo), HZ-03 (OOM).
- Para um deles (HZ-02), contar a "história curta": "Imagine que o detector marca um crawler do Google como força bruta. Sysadmin bloqueia. SEO da empresa cai." → fecha com a mitigação (allowlist + threshold + contexto).
- Mostrar matriz severidade × probabilidade.

### Bloco 7 — Ameaças e vulnerabilidades (Helena, 3 min)
- Inventário rápido de ativos (A-01 a A-10).
- STRIDE em uma tabela.
- **Um ataque concreto**: AT-01 (log poisoning via User-Agent injetando script no relatório) — explicar o caminho do payload e a contramedida (B5).
- Citar exposição **supply-chain** (AT-04) e como Dependabot/lockfile mitigam.

### Bloco 8 — Demonstração (Aryan + Rodrigo, 3 min)
- Aryan: terminal — `pdm run pytest` (testes verdes); mostrar `git log --oneline -10` (ritmo).
- Rodrigo: `python -m python_pdm_template.cli.main --help` mostrando subcomandos.
- Se até 06/07 (sprint pré-AV3) houver `analyze` real, rodar sobre `tests/fixtures/sample_brute_force.log` e mostrar a saída.
- Mostrar GUI (esqueleto ou versão evoluída, depende do progresso da sprint pré-AV3).
- Aceitar abertamente: "documentação fechada no prazo original 16/06; GUI ainda em construção, evolução planejada para AV4 está no Gantt atualizado".

### Bloco 9 — Acompanhamento (Elder, 2 min)
- Tabela de commits por integrante.
- Milestones: AV1 100% ✅, Sprint 0 100% ✅, AV2 100% ✅, Sprint 1 (Core MVP) 17% ⚠️, AV3 docs 100% / demo em esqueleto.
- Atualização de previsões (gráfico Gantt redesenhado).
- **Reconhecer a lacuna** entre 13/05 e 16/06: "fechamos a documentação no prazo original; a prorrogação do professor (08/07) nos deu fôlego para entregar a demo funcional na sprint pré-AV3."

### Bloco 10 — Próximos passos (todos, ~15 s cada)
- Aryan: "Vou finalizar parser + detector de força bruta esta semana."
- Rodrigo: "Conecto a CLI ao Core e implemento `--anonymize-ips`."
- Helena: "Implemento o QThread worker e o painel de filtros."
- Elder: "Cuido do release v0.1.0 com PyInstaller e da branch protection. Obrigado, professor."

---

## 3. Slide deck sugerido (10 slides)

1. **Capa** — nome do projeto, equipe, data, link do repo.
2. **Visão** — problema, solução, escopo (1 imagem do GANTT).
3. **Pipeline & propriedades emergentes** — diagrama do pipeline com PEFs e PENFs anotadas.
4. **7 dimensões de confiança** — tabela colorida (status).
5. **Defesa em profundidade** — diagrama de camadas (B0..B8, S0..S8).
6. **Matriz CL × Defesas** — heatmap.
7. **Top perigos (HZ)** — matriz severidade × probabilidade com pontos numerados.
8. **STRIDE + 1 ataque ilustrado** — fluxo do AT-01 (log poisoning).
9. **Acompanhamento** — commits por pessoa, milestones, Gantt atualizado.
10. **Demo + próximos passos** — print da CLI/GUI funcionando, mini-roadmap.

Sugestão: gerar os slides em PDF a partir de Markdown (ex.: `marp` ou `pandoc`) para versão única. Coloca-se o PDF em `docs/av3/SLIDES.pdf` antes da apresentação.

---

## 4. Plano B — se a demo não estiver pronta

Se até 06/07 o Core não estiver fazendo análise real (cenário-base hoje, 16/06):
1. Cortar Bloco 8 para 1 min: mostra só os testes verdes + esqueletos.
2. Aumentar Bloco 9 (acompanhamento) para 3 min explicando a lacuna e o plano de recuperação.
3. **Não esconder.** A pauta da AV3 pede "demonstração breve do **estado atual**" — estado atual honesto é mais bem avaliado que demo fake.

---

## 5. Checklist de véspera (07/07)

- [ ] `git pull origin master` em todas as máquinas da equipe.
- [ ] `pdm install` rodando sem warnings.
- [ ] `pdm run pytest` verde.
- [ ] CI do GitHub Actions verde no master.
- [ ] [RELATORIO_AV3.md](RELATORIO_AV3.md) com **issues** e **% milestones** preenchidos (precisa `gh auth login`).
- [ ] Slides gerados em PDF e commitados.
- [ ] Cabo HDMI / adaptador / clicker conferidos.
- [ ] Ensaio cronometrado (≥ 1 vez).
- [ ] Cada um sabe o que o outro vai dizer (transições suaves).
