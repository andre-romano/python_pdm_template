# Arquitetura do Sistema

## Visão Geral

O Log Sentinel segue uma arquitetura em camadas, com o **Core** completamente isolado das interfaces de apresentação (CLI e GUI). Esta separação garante que:

- O Core pode ser usado standalone (como biblioteca).
- CLI e GUI compartilham 100% da lógica de negócio.
- Testes do Core não dependem de UI.

```
┌─────────────────────────────────────────────────────────────┐
│                       USUÁRIO FINAL                          │
└──────────────────┬──────────────────────┬───────────────────┘
                   │                      │
        ┌──────────▼──────────┐  ┌────────▼──────────┐
        │       CLI           │  │       GUI          │
        │  (Typer + Rich)     │  │    (PySide6)       │
        │                     │  │                    │
        │  Controllers        │  │  MainWindow +      │
        │  Subcomandos        │  │  Workers (QThread) │
        └──────────┬──────────┘  └────────┬───────────┘
                   │                      │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼──────────────────────────────┐
                   │              CORE                        │
                   │                                          │
                   │  ┌───────────────────────────────────┐  │
                   │  │      LogAnalyzer (Facade)         │  │
                   │  └─────┬─────────────┬───────────────┘  │
                   │        │             │                   │
                   │  ┌─────▼─────┐ ┌────▼──────────┐       │
                   │  │ Pipeline  │ │   Factory     │       │
                   │  │ (Pipe &   │ │ (Parsers,     │       │
                   │  │  Filter)  │ │   DAOs)       │       │
                   │  └─────┬─────┘ └───────────────┘       │
                   │        │                                │
                   │  ┌─────▼──────────────────────────┐    │
                   │  │  Strategies (Parsers)          │    │
                   │  │  Detectors                     │    │
                   │  │  DAO (LogFileDAO, ReportDAO)   │    │
                   │  └────────────────────────────────┘    │
                   │                                          │
                   │           Eventos de Progresso          │
                   └──────────────────────────────────────────┘
                              │
                   ┌──────────▼──────────┐
                   │  Sistema de         │
                   │  arquivos (logs)    │
                   └─────────────────────┘
```

---

## Padrões de Projeto Aplicados

### 1. MVC (Model-View-Controller)

| Camada | Onde está | Responsabilidade |
|---|---|---|
| **Model** | `core/models.py` | Dataclasses: `LogEntry`, `AnalysisReport`, `Metrics` |
| **View** | `cli/`, `gui/` | Apresentar resultados ao usuário |
| **Controller** | `cli/commands/`, `gui/main_window.py` | Receber input, chamar Core, atualizar View |

### 2. Pipe & Filter

O processamento de logs é um pipeline de filtros encadeados:

```
Arquivo de Log
    │
    ▼
[ Reader ] ──► [ Validator ] ──► [ Parser ] ──► [ Filter ] ──► [ Aggregator ] ──► Relatório
   (DAO)        (Fail-Fast)     (Strategy)     (opcional)     (Métricas)
```

Cada etapa é independente e pode ser substituída ou estendida.

### 3. Strategy

Permite trocar o parser conforme o formato:

```python
class LogParserStrategy(Protocol):
    def parse(self, line: str) -> LogEntry | None: ...
    def validate(self, lines: list[str]) -> bool: ...

class ApacheLogParser(LogParserStrategy): ...
class NginxLogParser(LogParserStrategy): ...  # futuro
```

### 4. DAO (Data Access Object)

Isola toda I/O do sistema:

```python
class LogFileDAO(Protocol):
    def read_lines(self, path: Path) -> Iterator[str]: ...
    def get_size(self, path: Path) -> int: ...

class LocalFileLogDAO(LogFileDAO): ...
class MockLogDAO(LogFileDAO): ...  # para testes

class ReportDAO(Protocol):
    def save(self, report: AnalysisReport, path: Path) -> None: ...

class JsonReportDAO(ReportDAO): ...
```

### 5. Factory

Centraliza a criação de objetos:

```python
class LogParserFactory:
    @staticmethod
    def create(format_name: str) -> LogParserStrategy:
        match format_name:
            case "apache": return ApacheLogParser()
            case "nginx": return NginxLogParser()
            case _: raise ValueError(f"Formato desconhecido: {format_name}")
```

---

## Fluxo de Dados (Sequência)

### Cenário: usuário analisa um arquivo via CLI

```
Usuário                CLI               Factory          Pipeline         DAO            Parser
   │                    │                   │                │              │               │
   │  log-sentinel ──── │                   │                │              │               │
   │  analyze a.log     │                   │                │              │               │
   │                    │                   │                │              │               │
   │                    │── create("apache")─►                │              │               │
   │                    │                   │                │              │               │
   │                    │◄──── ApacheParser ─                │              │               │
   │                    │                   │                │              │               │
   │                    │── analyze(file) ──────────────────►                │               │
   │                    │                   │                │              │               │
   │                    │                   │                │── read() ────►               │
   │                    │                   │                │              │               │
   │                    │                   │                │◄── lines ────                │
   │                    │                   │                │              │               │
   │                    │                   │                │── parse() ───────────────────►
   │                    │                   │                │              │               │
   │                    │                   │                │◄── entries ──────────────────
   │                    │                   │                │              │               │
   │                    │                   │                │ [aggregate metrics]          │
   │                    │                   │                │              │               │
   │                    │◄──── report ──────────────────────                │               │
   │                    │                   │                │              │               │
   │                    │ [render table]    │                │              │               │
   │                    │                   │                │              │               │
   │◄── output ─────────                    │                │              │               │
```

---

## Estrutura de Diretórios

```
log-sentinel/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline CI/CD
├── .vscode/
│   └── settings.json
├── docs/                       # Documentação do projeto
│   ├── PROJETO.md
│   ├── REQUISITOS.md
│   ├── ESCOPO.md
│   ├── CASOS_DE_USO.md
│   ├── architecture/
│   │   ├── ARQUITETURA.md
│   │   ├── CORE_API.md
│   │   ├── CLI_DESIGN.md
│   │   └── GUI_DESIGN.md
│   ├── testing/
│   │   ├── ESTRATEGIA_TESTES.md
│   │   └── CRITERIOS_ACEITACAO.md
│   └── team/
│       ├── PAPEIS.md
│       └── CONVENCOES.md
├── src/
│   └── log_sentinel/
│       ├── __init__.py
│       ├── __main__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── parsers/
│       │   ├── detectors/
│       │   ├── pipeline.py
│       │   ├── dao/
│       │   ├── factories.py
│       │   └── events.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   └── commands/
│       └── gui/
│           ├── __init__.py
│           ├── main_window.py
│           ├── workers.py
│           └── widgets/
├── tests/
│   ├── core/
│   ├── cli/
│   ├── gui/
│   └── fixtures/
├── pyproject.toml
├── pdm.lock
├── README.md
├── CLAUDE.md                   # Contexto para Claude Code
└── .claude/
    └── AGENT_GUIDE.md
```

---

## Princípios SOLID Aplicados

- **S** (Single Responsibility): cada classe tem uma única responsabilidade. Ex: `ApacheLogParser` só faz parsing, `BruteForceDetector` só detecta força bruta.
- **O** (Open/Closed): para adicionar um novo formato, basta criar uma nova `Strategy`. Nenhum código existente é alterado.
- **L** (Liskov Substitution): qualquer `LogParserStrategy` pode ser usado onde a interface é esperada.
- **I** (Interface Segregation): interfaces (Protocols) são pequenas e focadas.
- **D** (Dependency Inversion): o Core depende de abstrações (Protocols), não de implementações concretas.

---

## Sistema de Eventos (Observer)

O Core emite eventos durante o processamento, consumidos por CLI e GUI:

```python
class ProgressObserver(Protocol):
    def on_file_start(self, path: Path, total_bytes: int) -> None: ...
    def on_progress(self, bytes_processed: int, total_bytes: int) -> None: ...
    def on_file_complete(self, path: Path, entries_parsed: int) -> None: ...
    def on_error(self, path: Path, error: Exception) -> None: ...

# CLI implementa com Rich
class RichProgressObserver(ProgressObserver): ...

# GUI implementa com QSignal
class QtProgressObserver(QObject, ProgressObserver):
    progress_signal = Signal(int, int)
    ...
```
