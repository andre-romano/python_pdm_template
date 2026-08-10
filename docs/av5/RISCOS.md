# Especificacao de Riscos - Log Sentinel

Este documento descreve os riscos identificados pela equipe para o desenvolvimento
e operacao do Log Sentinel. Ele integra o pacote da AV5 (Riscos e Qualidade) da
disciplina de Engenharia de Software II.

## Metodo

Para cada risco descrevemos, na ordem: uma descricao breve, a avaliacao em termos
de probabilidade e impacto, uma analise de causa-raiz e a declaracao de
aceitabilidade que a equipe assumiu. A avaliacao segue a escala qualitativa
descrita a seguir, apoiada em uma matriz simples.

### Escala de probabilidade

| Nivel | Descricao |
|-------|-----------|
| Baixa | Ocorrencia improvavel dentro do horizonte do projeto. |
| Media | Ocorrencia plausivel em uma minoria dos cenarios de uso. |
| Alta  | Ocorrencia esperada em uso normal se nao houver mitigacao. |

### Escala de impacto

| Nivel | Descricao |
|-------|-----------|
| Baixo | Perda de tempo pontual, sem comprometer o resultado da analise. |
| Medio | Perda de confianca em uma parte do relatorio; requer reexecucao. |
| Alto  | Comprometimento do resultado ou da integridade do arquivo analisado. |

### Matriz probabilidade x impacto

|                | Impacto Baixo | Impacto Medio | Impacto Alto |
|----------------|---------------|---------------|--------------|
| Prob. Alta     | Moderado      | Alto          | Critico      |
| Prob. Media    | Baixo         | Moderado      | Alto         |
| Prob. Baixa    | Baixo         | Baixo         | Moderado     |

## Catalogo de riscos

### R1 - Log de entrada corrompido ou truncado

- Descricao: o arquivo `.log` recebido pelo Log Sentinel pode ter linhas
  incompletas, encoding inesperado ou truncamento parcial resultante de rotacao.
- Avaliacao: probabilidade media, impacto medio, nivel geral moderado.
- Causa-raiz: logs Apache reais sofrem rotacao e coleta manual; parte das
  linhas pode chegar sem os campos esperados pelo `ApacheParser`.
- Mitigacao adotada: o parser levanta `ParseError` por linha invalida e a CLI
  contabiliza descartadas em vez de abortar a analise inteira.
- Aceitabilidade: TODO Elder - confirmar ate 05/08 se a equipe aceita perder
  ate X% de linhas descartadas ou se e preciso emitir alerta.

### R2 - Falha de deteccao (falso negativo) em cenarios reais

- Descricao: os tres detectores implementados (BruteForceDetector,
  ScannerDetector, TrafficSpikeDetector) trabalham com thresholds fixos e
  janelas de tempo curtas; ataques mais lentos, distribuidos entre varios IPs
  ou com pausas superiores a janela nao sao identificados.
- Avaliacao: probabilidade alta, impacto medio, nivel alto.
- Causa-raiz: o Log Sentinel foi projetado como ferramenta de analise
  post-mortem sobre um unico arquivo, sem correlacao entre IPs nem persistencia
  de estado entre execucoes; essa e uma limitacao consciente do escopo, nao um
  defeito.
- Mitigacao adotada: os thresholds e o tamanho da janela sao parametros do
  construtor de cada detector, permitindo calibracao por caso; a suite de
  testes inclui casos de fronteira (threshold-1, threshold exato, threshold+1)
  documentando o comportamento esperado.
- Aceitabilidade: aceitavel. A ferramenta declara no relatorio final o total
  de linhas processadas e o hash do arquivo, permitindo que o analista humano
  reprocesse o mesmo log com outros thresholds se suspeitar de subestimacao.

### R3 - Ambiente Windows do professor sem Python instalado

- Descricao: a demo da AV5 ocorre na maquina do professor, que nao aceita
  Docker; se o binario nao trouxer todas as dependencias, a apresentacao trava.
- Avaliacao: probabilidade alta, impacto alto, nivel critico.
- Causa-raiz: PySide6 costuma exigir `--collect-all` no PyInstaller; ausencia
  desse flag no build inicial gerou binario incompleto em outros projetos.
- Mitigacao adotada: `release.yaml` gera dois executaveis (`log-sentinel.exe` e
  `log-sentinel-gui.exe`) via PyInstaller, com smoke test rodando o `.exe` da
  CLI contra fixture antes de publicar o artefato.
- Aceitabilidade: aceitavel apenas se o smoke test do binario passar em
  `windows-latest`. Se falhar, bloqueia a apresentacao.

### R4 - Cobertura de testes abaixo de 80% no dia da entrega

- Descricao: a rubrica exige cobertura minima de 80% no SonarCloud; parte do
  codigo da GUI ainda nao possui testes automatizados.
- Avaliacao: probabilidade media, impacto alto, nivel alto.
- Causa-raiz: `pytest-qt` nao estava no grupo `dev`; testes de GUI so entram
  nesta AV.
- Mitigacao adotada: distribuicao de testes por integrante nas issues #35, #36
  e #37, com deadline interno em 05/08.
- Aceitabilidade: aceitavel entregar com cobertura entre 80% e 85% desde que
  os modulos criticos (parser, detectores, DAO) fiquem acima de 90%.

### R5 - Divergencia entre versao apresentada e versao publicada no GitHub

- Descricao: a demo pode acabar sendo executada com um build local diferente
  do que esta no master, especialmente se algum integrante rebuilds o binario
  no proprio notebook horas antes da apresentacao.
- Avaliacao: probabilidade media, impacto medio, nivel moderado.
- Causa-raiz: fluxo humano. Sob pressao a equipe costuma preferir "compilar
  aqui rapido" a esperar o workflow terminar; isso quebra a rastreabilidade
  entre o commit avaliado no SonarCloud e o binario apresentado.
- Mitigacao adotada: antes da apresentacao a equipe cria a tag `v0.5.0` no
  commit revisado, o `release.yaml` gera os binarios em runners limpos e
  publica como GitHub Release; a apresentacao usa o `.exe` baixado dessa
  release, nao um build local.
- Aceitabilidade: aceitavel apenas se a tag existir e o artefato tiver sido
  gerado pelo workflow. Rebuild local so em caso de emergencia, e ainda assim
  a partir da tag.

### R6 - Ausencia de um integrante no dia da apresentacao

- Descricao: a AV3 ja aconteceu com a equipe reduzida em relacao ao numero
  planejado; a avaliacao e individual e em grupo, entao a falta de alguem
  penaliza a nota coletiva.
- Avaliacao: probabilidade media, impacto medio, nivel moderado.
- Causa-raiz: fatores externos ao projeto (saude, deslocamento, conflitos com
  outras disciplinas). Nao ha o que a equipe possa fazer para eliminar a
  causa; so podemos mitigar o impacto.
- Mitigacao adotada: cada bloco da apresentacao tem um responsavel principal
  e um substituto explicitamente designado no roteiro; o material de apoio
  fica em uma pasta compartilhada acessivel a todos ate a vespera; a demo
  do binario e ensaiada por pelo menos dois integrantes.
- Aceitabilidade: aceitavel enquanto pelo menos tres dos quatro integrantes
  estiverem presentes. Se cair para dois, a equipe reagenda com o professor
  se possivel, ou executa o roteiro reduzido cobrindo apenas os blocos
  criticos (visao geral, demo, encerramento).

## Declaracao geral de aceitabilidade

Dos seis riscos catalogados, tres estao plenamente mitigados pela mecanica
tecnica do projeto: R1 (log corrompido) e absorvido pelo tratamento de
`ParseError` do parser combinado com o contador de linhas descartadas na CLI;
R3 (ambiente Windows do professor) e coberto pela geracao de dois binarios
autocontidos via PyInstaller no `release.yaml` com smoke test no proprio
runner Windows; R4 (cobertura abaixo de 80%) e endereçado pela distribuicao
explicita das tarefas de teste entre os integrantes com deadline interno em
2026-08-05, uma semana antes da entrega.

Dois riscos permanecem parcialmente aceitos: R2 (falso negativo) e uma
limitacao consciente do escopo, com mitigacao pela parametrizacao dos
thresholds e pela publicacao do hash do arquivo no relatorio, permitindo
reprocessamento; R5 (divergencia entre versao apresentada e publicada) depende
de disciplina operacional da equipe no dia da apresentacao, e por isso ficou
protocolada a exigencia de que o binario apresentado venha do GitHub Release
gerado a partir da tag `v0.5.0`.

Um risco (R6, ausencia de integrante) nao admite mitigacao tecnica, so
compensacao organizacional pela designacao de substitutos por bloco de
apresentacao.

Nenhum risco identificado justifica adiar a entrega ou reduzir escopo alem do
que ja foi acordado (nada de detector novo, foco em endurecer o que existe).
O projeto entra na AV5 com aceitabilidade geral favoravel.
