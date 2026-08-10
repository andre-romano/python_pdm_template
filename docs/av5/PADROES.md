# Padroes de Projeto e Arquitetura - Log Sentinel

Este documento reune os padroes de projeto e arquitetura utilizados na
implementacao do Log Sentinel. Cada secao identifica o padrao, aponta onde ele
aparece no codigo, explica a motivacao e traz um trecho ilustrativo. Integra o
pacote da AV5 (Riscos e Qualidade).

## Visao geral

Do ponto de vista arquitetural o Log Sentinel e uma aplicacao em camadas com
tres frentes independentes que compartilham o mesmo Core: uma camada de acesso
a dados (`core/dao`), uma camada de dominio (`core/parsers`, `core/detectors`,
`core/aggregator`) e duas interfaces (`cli/` e `gui/`). O fluxo de execucao
dentro do Core segue o padrao Pipe-and-Filter, e cada detector e uma variante
polimorfica do padrao Strategy. A GUI segue MVC com o mecanismo de sinais e
slots do Qt no papel de Observer.

## Pipe-and-Filter (Pipeline do Core)

- Onde: `src/python_pdm_template/core/pipeline.py`, classe `Pipeline`.
- Motivacao: manter cada estagio da analise (leitura, parse, deteccao)
  independente e substituivel; permite trocar o DAO ou adicionar um detector
  sem reescrever os demais.
- Trecho:

  ```python
  class Pipeline:
      def __init__(self, dao: LogFileDAO, parser: ApacheParser, detectors: list) -> None:
          ...
      def run(self) -> Iterator[Detection]:
          entries = [self.parser.parse_line(line, i)
                     for i, line in enumerate(self.dao.read_lines(), start=1)]
          for detector in self.detectors:
              yield from detector.process(entries)
  ```

## Strategy (Detectores)

- Onde: `src/python_pdm_template/core/detectors/`.
- Motivacao: cada tipo de anomalia (`brute_force`, `scanner`, `traffic_spike`)
  aplica um algoritmo diferente sobre a mesma sequencia de `LogEntry`. O
  Pipeline os trata pela mesma interface, escolhendo qual conjunto de
  estrategias executar por injecao no construtor.
- Estado atual: TODO Aryan - fechar a issue #35 introduzindo `BaseDetector(ABC)`
  em `core/detectors/base.py` com `process(entries) -> Iterator[Detection]` e
  migrar as tres classes existentes para herdar dele. Depois, colar aqui o
  diagrama de heranca resultante.

## DAO (Data Access Object)

- Onde: `src/python_pdm_template/core/dao/log_file_dao.py`, classe `LogFileDAO`.
- Motivacao: isolar o acesso ao arquivo `.log` do restante do sistema. Alem de
  ler as linhas em streaming (evitando carregar arquivos grandes inteiros na
  memoria), o DAO calcula e expoe o hash SHA-256 do arquivo em um unico passe,
  usado na sessao de integridade dos requisitos de seguranca.
- Trecho:

  ```python
  class LogFileDAO:
      def __init__(self, file_path: str | Path) -> None:
          self.file_path = Path(file_path)
          self._digest = ""

      @property
      def digest(self) -> str:
          """Hash SHA-256 do arquivo, disponivel apos consumir read_lines."""
          return self._digest

      def read_lines(self) -> Generator[str, None, None]:
          sha256_hash = hashlib.sha256()
          with open(self.file_path, "rb") as f:
              for line_bytes in f:
                  sha256_hash.update(line_bytes)
                  yield line_bytes.decode("utf-8", errors="replace")
          self._digest = sha256_hash.hexdigest()
  ```

- Consequencia arquitetural: o hash so fica disponivel apos consumir o
  generator ate o fim. Quem quiser publicar o digest (a CLI ao final do
  relatorio, por exemplo) precisa iterar toda a sequencia antes. O parser e
  os detectores nao precisam saber que o arquivo foi lido em binario nem que
  o hash esta sendo calculado no meio do caminho.

## MVC + Observer (GUI)

- Onde: `src/python_pdm_template/gui/`.
- Motivacao: separar o dado exibido (`LogEntryTableModel`, um `QAbstractTableModel`)
  da apresentacao (`MainWindow` e a `QTableView`), com o parse rodando em uma
  `QThread` (`LogParserWorker`) que emite sinais para atualizar a interface
  sem bloquear o event loop.
- Estado atual: TODO Helena - fechar a issue #37 e entregar para o Elder o
  paragrafo final desta secao, citando explicitamente:
  - Model: `LogEntryTableModel` estende `QAbstractTableModel`.
  - View: `QTableView` na `MainWindow`.
  - Controller: a propria `MainWindow`, que responde a acoes do usuario
    (drag-and-drop, filtros, botoes) e coordena o worker.
  - Observer: os sinais `progress`, `finished`, `error` do `LogParserWorker`
    ligados a slots da `MainWindow`.

## Referencias cruzadas

- Cobertura das estrategias e do DAO por testes: ver secao correspondente em
  `docs/av5/AFIRMACOES.md` (a ser produzida por Rodrigo).
- Riscos associados a essas escolhas de padrao: R2, R3 e R4 em
  `docs/av5/RISCOS.md`.
