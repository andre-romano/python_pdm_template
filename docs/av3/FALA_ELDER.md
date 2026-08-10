# Fala — Elder Lopes (AV3)

> Rascunho das falas dos blocos sob minha responsabilidade.
> Blocos: **1 (abertura)**, **4 (dimensões de confiança)**, **9 (acompanhamento)**, **10 (fechamento)**.
> Tempo total dos meus blocos: ≈ **6 min 15 s** dos 25 min totais.

---

## Bloco 1 — Abertura (≈ 1 min)

> "Boa tarde, professor. Somos a equipe do **Log Sentinel** — eu sou o Elder Lopes, responsável pelo CI/CD e pela documentação, e estão comigo o Aryan, que cuida do Core, o Rodrigo, responsável pela CLI, e a Helena, responsável pela GUI.
>
> O Log Sentinel é uma ferramenta de análise *post-mortem* de logs do Apache, com foco em segurança defensiva — detecta padrões como força bruta, port scanning e picos de tráfego. Hoje vamos apresentar nossa entrega da AV3, que cobre **falhas, ameaças e dimensões de confiança** aplicadas ao nosso projeto.
>
> Toda a documentação está em `github.com/202316360036/log-sentinel`, na pasta `docs/av3/`. A apresentação está dividida em 10 blocos curtos, e cada um da equipe vai apresentar a parte que conduziu. Vamos começar com o Rodrigo apresentando a visão geral."

**Apoio visual:** slide de capa com nomes, papéis e link do repositório.

---

## Bloco 4 — Dimensões de confiança (≈ 3 min)

> "Quando a gente desenvolve um software que vai ser usado para **tomar decisões com consequência real** — como bloquear um IP suspeito ou registrar uma evidência em processo — não basta dizer que ele funciona. Precisamos mostrar que ele é **confiável**. A literatura clássica, especialmente o Avizienis e o Laprie em 2004, decompõe confiança em **sete dimensões**, e o Log Sentinel se posiciona em cada uma delas."

> "**Primeira, Safety** — segurança operacional. O Log Sentinel opera em modo **read-only** sobre o arquivo de log: nunca escreve, renomeia ou remove a entrada. E o pipeline é **idempotente** — rodar duas vezes no mesmo log produz o mesmo relatório."

> "**Segunda, Security** — proteção contra ações maliciosas. A análise é **100% offline**: nenhum dado de log sai da máquina, nenhum módulo de rede é importado no Core. Além disso, sanitizamos a saída para evitar que um payload injetado em `User-Agent` execute script no visualizador do relatório, e geramos um hash SHA-256 do log original para garantir cadeia de custódia."

> "**Terceira, Reliability** — confiabilidade. Aplicamos isolamento por arquivo no modo batch, ou seja, exceção em um arquivo não derruba os outros, e mantemos meta de **80% de cobertura de testes** com TDD desde o primeiro commit funcional."

> "**Quarta, Availability** — disponibilidade. Como é uma aplicação local de invocação imediata, não há servidor que possa cair. E vamos empacotar com **PyInstaller**, então roda mesmo sem Python instalado."

> "**Quinta, Maintainability** — manutenibilidade. Essa hoje é a dimensão mais madura no projeto: arquitetura em camadas com o Core 100% isolado, padrões de projeto explícitos como Strategy, Factory, Observer, e o CI roda `ruff` e `pyright` em todo PR."

> "**Sexta, Resilience** — resiliência. O parser é **fail-fast por linha**: linha inválida vira um `ParseError` registrado, mas o processamento continua. Se o usuário der `Ctrl+C` no meio, ele recebe um **relatório parcial**, não tudo-ou-nada."

> "**Sétima, Privacy** — privacidade. **Zero telemetria**, logs nunca saem da máquina, e vamos ter uma flag `--anonymize-ips` para mascarar IPs quando o relatório precisar ser compartilhado com terceiros."

> "Para ser honesto sobre maturidade: hoje a Maintainability já está pronta, Availability está com o pipeline montado, Reliability está em construção, e as outras quatro estão planejadas e documentadas, mas serão implementadas até a AV5. Essa tabela com o status de cada dimensão está no documento 03 da nossa entrega."

**Apoio visual:** tabela colorida do §3 do doc 03 — uma linha por dimensão, coluna de mecanismos, coluna de status (✅ / 🔄 / ⏳).

---

## Bloco 9 — Acompanhamento (≈ 2 min)

> "Sobre o acompanhamento do projeto. Em termos de **commits**, no período de 08 de abril até 12 de maio acumulamos cerca de **24 commits** úteis: 9 do Aryan no Core e na configuração, 9 meus em CI e documentação, 4 do Rodrigo na CLI, e 2 da Helena na GUI. O nome `Andre` que aparece no `git log` é o autor do **template original** que usamos como base — não conta como integrante."

> "Sobre **milestones**: a **AV1 (Ambiente)** está fechada em 100%, a **AV2 (Testes e documentação inicial)** também em 100%, e a **AV3 (esta entrega)** está em torno de **80%** — os cinco documentos estão completos, e a parte que falta é a demo funcional, que o Aryan e o Rodrigo vão mostrar daqui a pouco."

> "Precisamos ser **transparentes sobre uma lacuna**: entre 13 de maio e 10 de junho, praticamente não tivemos commits no repositório. Foi um período em que outras disciplinas demandaram atenção. Reconhecemos isso abertamente. A partir do dia 10 retomamos o ritmo, fechamos a documentação completa da AV3 e replanejamos os próximos passos."

> "O Gantt foi **atualizado** para refletir essa realidade: a entrega do Core MVP foi remanejada para a janela de 16 a 30 de junho, junto com a CLI completa e os widgets principais da GUI. Os marcos finais — release v0.1.0, AV4 e AV5 — continuam dentro do prazo original. Toda essa tabela está no `RELATORIO_AV3.md`, seções 3 a 6."

**Apoio visual:** slide com (1) tabela de commits por integrante; (2) tabela de milestones com %; (3) trecho do Gantt atualizado.

---

## Bloco 10 — Próximos passos e fechamento (≈ 15 s da minha parte)

> "Da minha parte, vou cuidar do **release v0.1.0** com PyInstaller para Linux e Windows e configurar a **branch protection** definitiva no repositório.
>
> Professor, era isso. Estamos abertos para perguntas. Obrigado."

---

## Anotações pessoais (não falar)

- **Tom geral:** firme, sem desculpa-rodeio. A frase chave é "reconhecemos abertamente" — assumir lacuna é mais bem avaliado que esconder.
- **Não decorar palavra por palavra**; saber a sequência de **ideias** é mais importante.
- **Olhar pro professor**, não pro slide.
- **Cronometrar em casa**: se passar de 3 min no bloco 4, cortar exemplos de verificação (só citar mecanismos).
- **Se travar:** voltar à tabela do slide e ler a linha onde parei — é um caminho seguro de retomada.

## Estudo extra (caso ele pergunte algo das dimensões)

- **Por que 7 e não 5?** Avizienis/Laprie (2004) consolidaram safety, reliability, availability, maintainability, integrity, confidentiality como sub-atributos de dependability+security. Resilience entrou depois com NIST SP 800-160 Vol.2. Privacy foi destacada com LGPD/GDPR. Adotamos as 7 porque cada uma muda o que verificamos.
- **Maintainability x Reliability — não é a mesma coisa?** Não: manutenibilidade é facilidade de evoluir o código; confiabilidade é probabilidade de operar correto. Um código bem mantido pode ter bugs intermitentes.
- **Como medir Availability se não tem servidor?** Para app local, availability vira tempo de cold-start e ausência de dependência de runtime — por isso o teste de smoke no binário PyInstaller numa VM limpa.
