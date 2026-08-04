# Contratos da API do Core

> Este documento define as **interfaces (contratos)** das classes do Core. Os testes TDD devem ser escritos com base nestes contratos antes da implementação.

## Modelos de Dados

### `LogEntry`
Representa uma linha de log parseada.

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class LogEntry:
    """Uma entrada parseada de log Apache."""
    ip: str
    timestamp: datetime
    method: str          # GET, POST, PUT, DELETE, ...
    path: str            # /index.html, /admin, ...
    protocol: str        # HTTP/1.1
    status: int          # 200, 404, 500, ...
    bytes_sent: int      # quantidade de bytes na resposta
    referer: str | None = None
    user_agent: str | None = None
```

### `Metrics`
Métricas agregadas de um conjunto de logs.

```python
@dataclass
class Metrics:
    """Métricas agregadas de uma análise."""
    total_requests: int
    requests_per_ip: dict[str, int]
    status_distribution: dict[int, int]    # {200: 1500, 404: 23, ...}
    top_endpoints: list[tuple[str, int]]   # [(path, count), ...]
    requests_per_hour: dict[int, int]      # {0: 50, 1: 30, ..., 23: 100}
    total_bytes: int
```

### `SuspiciousIP`
Resultado da detecção de anomalias.

```python
from enum import Enum

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass(frozen=True)
class SuspiciousIP:
    """IP identificado como suspeito por algum detector."""
    ip: str
    reason: str                       # "brute-force", "scanner", "traffic-spike"
    request_count: int
    time_window_seconds: int
    risk_level: RiskLevel
    sample_paths: list[str]           # exemplos de paths acessados
```

### `AnalysisReport`
Relatório consolidado.

```python
@dataclass
class AnalysisReport:
    """Relatório completo de uma análise."""
    files_analyzed: list[Path]
    metrics: Metrics
    suspicious_ips: list[SuspiciousIP]
    started_at: datetime
    finished_at: datetime
    errors: list[str]
```

---

## Interfaces (Protocols)

### `LogParserStrategy`
Interface para parsers de diferentes formatos de log.

```python
from typing import Protocol

class LogParserStrategy(Protocol):
    """Contrato para parsers de log de qualquer formato."""

    @property
    def format_name(self) -> str:
        """Nome do formato (ex: 'apache', 'nginx')."""
        ...

    def parse(self, line: str) -> LogEntry | None:
        """Parse uma única linha.

        :param line: Linha bruta do log.
        :return: LogEntry se parseável, None caso contrário.
        """
        ...

    def validate(self, sample_lines: list[str]) -> bool:
        """Valida se as linhas correspondem ao formato.

        :param sample_lines: Lista das primeiras linhas do arquivo.
        :return: True se ≥ 50% das linhas casarem com o formato.
        """
        ...
```

### `LogFileDAO`
Interface para leitura de arquivos de log.

```python
from typing import Iterator
from pathlib import Path

class LogFileDAO(Protocol):
    """Contrato para acesso a arquivos de log (somente leitura)."""

    def read_lines(self, path: Path) -> Iterator[str]:
        """Lê o arquivo linha por linha (generator).

        :param path: Caminho do arquivo.
        :return: Iterator de linhas (sem newline final).
        :raises FileNotFoundError: Se o arquivo não existir.
        :raises PermissionError: Se não houver permissão de leitura.
        """
        ...

    def get_size(self, path: Path) -> int:
        """Retorna o tamanho do arquivo em bytes."""
        ...

    def read_sample(self, path: Path, n_lines: int = 5) -> list[str]:
        """Lê as primeiras n_lines do arquivo (para validação)."""
        ...
```

### `ReportDAO`
Interface para exportação de relatórios.

```python
class ReportDAO(Protocol):
    """Contrato para exportar relatórios em diferentes formatos."""

    @property
    def format_name(self) -> str:
        """Nome do formato (ex: 'json', 'csv')."""
        ...

    def save(self, report: AnalysisReport, path: Path) -> None:
        """Salva o relatório no caminho indicado.

        :param report: Relatório a salvar.
        :param path: Caminho do arquivo de saída.
        """
        ...
```

### `AnomalyDetector`
Interface para detectores de anomalias.

```python
class AnomalyDetector(Protocol):
    """Contrato para detectores de comportamento anômalo."""

    @property
    def detector_name(self) -> str:
        """Nome do detector (ex: 'brute-force', 'scanner')."""
        ...

    def detect(self, entries: Iterator[LogEntry]) -> list[SuspiciousIP]:
        """Analisa as entradas e retorna IPs suspeitos.

        :param entries: Iterator de entradas de log.
        :return: Lista de IPs identificados como suspeitos.
        """
        ...
```

### `ProgressObserver`
Interface para observadores de progresso.

```python
class ProgressObserver(Protocol):
    """Contrato para observadores do progresso de processamento."""

    def on_file_start(self, path: Path, total_bytes: int) -> None: ...
    def on_progress(self, bytes_processed: int, total_bytes: int) -> None: ...
    def on_file_complete(self, path: Path, entries_parsed: int) -> None: ...
    def on_error(self, path: Path, error: Exception) -> None: ...
```

---

## Classes Concretas

### `LogAnalyzer` (Facade Principal)
Ponto de entrada principal do Core. Orquestra todo o processamento.

```python
class LogAnalyzer:
    """Facade principal do Core. Orquestra parsing, detecção e agregação."""

    def __init__(
        self,
        parser: LogParserStrategy,
        file_dao: LogFileDAO,
        detectors: list[AnomalyDetector] | None = None,
        observers: list[ProgressObserver] | None = None,
    ) -> None: ...

    def analyze(
        self,
        path: Path,
        filters: AnalysisFilters | None = None,
    ) -> AnalysisReport:
        """Analisa um único arquivo.

        :param path: Caminho do arquivo de log.
        :param filters: Filtros opcionais (IP, data, status).
        :raises InvalidLogFormatError: Se o arquivo não for válido.
        """
        ...

    def analyze_batch(
        self,
        paths: list[Path],
        filters: AnalysisFilters | None = None,
    ) -> AnalysisReport:
        """Analisa múltiplos arquivos e retorna relatório consolidado."""
        ...
```

### `AnalysisFilters`
Filtros aplicáveis durante a análise.

```python
@dataclass
class AnalysisFilters:
    """Filtros opcionais aplicados durante a análise."""
    ip: str | None = None
    status_codes: list[int] | None = None
    date_start: datetime | None = None
    date_end: datetime | None = None
    paths: list[str] | None = None
```

### `BruteForceDetector`

```python
class BruteForceDetector(AnomalyDetector):
    """Detecta IPs com requisições anormais em janela de tempo."""

    def __init__(
        self,
        threshold: int = 100,
        window_minutes: int = 5,
    ) -> None: ...

    def detect(self, entries: Iterator[LogEntry]) -> list[SuspiciousIP]: ...
```

### `ScannerDetector`

```python
class ScannerDetector(AnomalyDetector):
    """Detecta IPs varrendo URLs sensíveis."""

    DEFAULT_SUSPICIOUS_PATHS = [
        "/admin", "/wp-login", "/.env", "/phpmyadmin",
        "/.git", "/config", "/backup",
    ]

    def __init__(
        self,
        suspicious_paths: list[str] | None = None,
        min_distinct_paths: int = 5,
    ) -> None: ...

    def detect(self, entries: Iterator[LogEntry]) -> list[SuspiciousIP]: ...
```

### `LogParserFactory`

```python
class LogParserFactory:
    """Factory para criação de parsers de log."""

    @staticmethod
    def create(format_name: str) -> LogParserStrategy:
        """Cria um parser para o formato especificado.

        :param format_name: 'apache', 'nginx', etc.
        :raises ValueError: Se o formato não for suportado.
        """
        ...

    @staticmethod
    def list_supported() -> list[str]:
        """Retorna lista de formatos suportados."""
        ...
```

### `ReportFactory`

```python
class ReportFactory:
    """Factory para criação de DAOs de relatório."""

    @staticmethod
    def create(format_name: str) -> ReportDAO:
        """Cria um DAO de relatório para o formato especificado.

        :param format_name: 'json', 'csv', etc.
        """
        ...
```

---

## Exceções

```python
class LogSentinelError(Exception):
    """Exceção base do sistema."""

class InvalidLogFormatError(LogSentinelError):
    """Levantada quando o arquivo não corresponde ao formato esperado."""

class FileTooLargeError(LogSentinelError):
    """Levantada quando o arquivo excede o limite de processamento."""

class UnsupportedFormatError(LogSentinelError):
    """Levantada quando o formato solicitado não é suportado."""
```

---

## Exemplo de Uso (referência para testes)

```python
from pathlib import Path
from log_sentinel.core import (
    LogAnalyzer, LogParserFactory, ReportFactory,
    BruteForceDetector, AnalysisFilters,
)
from log_sentinel.core.dao import LocalFileLogDAO

# Setup
parser = LogParserFactory.create("apache")
file_dao = LocalFileLogDAO()
detectors = [BruteForceDetector(threshold=100, window_minutes=5)]

analyzer = LogAnalyzer(parser=parser, file_dao=file_dao, detectors=detectors)

# Análise
report = analyzer.analyze(
    path=Path("access.log"),
    filters=AnalysisFilters(status_codes=[404, 500]),
)

# Saída
print(f"Total de requisições: {report.metrics.total_requests}")
print(f"IPs suspeitos: {len(report.suspicious_ips)}")

# Exportação
report_dao = ReportFactory.create("json")
report_dao.save(report, Path("relatorio.json"))
```
