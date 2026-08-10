# Design da GUI

> Responsável: **Helena** — Engenheira de GUI

## Tecnologia

- **PySide6** (Qt for Python) — framework de GUI nativa multiplataforma

## Princípios de UX

1. **Não travar a tela**: toda operação pesada em `QThread` (RNF-02).
2. **Feedback constante**: barra de progresso visível durante processamento.
3. **Drag & drop**: suporte para arrastar arquivos para a janela.
4. **Filtros laterais**: aplicáveis sem reprocessar o arquivo.
5. **Atalhos de teclado**: Ctrl+O (abrir), Ctrl+E (exportar), F5 (atualizar).

## Estrutura de Telas

### Tela Principal (MainWindow)

```
┌────────────────────────────────────────────────────────────────────┐
│  Log Sentinel                                          [_] [□] [X] │
├────────────────────────────────────────────────────────────────────┤
│  📁 Arquivo  ⚙️ Análise  📊 Relatório  ❓ Ajuda                    │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─ FILTROS ──────────────┐ ┌─ RESULTADOS ────────────────────┐   │
│  │                        │ │ ┌────────────────────────────┐ │   │
│  │ Formato:               │ │ │ Métricas Gerais            │ │   │
│  │  [Apache         ▼]    │ │ │ Requests: 15.234           │ │   │
│  │                        │ │ │ IPs únicos: 892            │ │   │
│  │ Filtrar por IP:        │ │ └────────────────────────────┘ │   │
│  │  [_______________]     │ │                                │   │
│  │                        │ │ ┌─ Top IPs ─────────────────┐ │   │
│  │ Status codes:          │ │ │ IP            Requests    │ │   │
│  │  [✓] 2xx               │ │ │ 192.168.1.100   3.421     │ │   │
│  │  [✓] 3xx               │ │ │ 10.0.0.5        1.892     │ │   │
│  │  [✓] 4xx               │ │ │ ...                        │ │   │
│  │  [ ] 5xx               │ │ └────────────────────────────┘ │   │
│  │                        │ │                                │   │
│  │ Período:               │ │ ┌─ Suspeitos ───────────────┐ │   │
│  │  De: [____]            │ │ │ IP        Motivo   Risco  │ │   │
│  │  Até: [____]           │ │ │ 203...    bf       ALTO   │ │   │
│  │                        │ │ └────────────────────────────┘ │   │
│  │ Detecções:             │ │                                │   │
│  │  [✓] Força bruta       │ │                                │   │
│  │  [✓] Scanner           │ │                                │   │
│  │  [ ] Picos de tráfego  │ │                                │   │
│  │                        │ │                                │   │
│  │ [Aplicar filtros]      │ │                                │   │
│  │                        │ │                                │   │
│  └────────────────────────┘ └────────────────────────────────┘   │
│                                                                    │
│  [Selecionar arquivo...] [Analisar] [Exportar JSON]                │
│                                                                    │
│  Progresso: [████████░░░░] 67% • Processando: access.log           │
└────────────────────────────────────────────────────────────────────┘
```

---

## Componentes (Widgets)

### `MainWindow`
Janela principal. Orquestra os outros widgets e gerencia threads.

```python
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log Sentinel")
        self.setAcceptDrops(True)  # Para drag & drop
        self._setup_ui()
        self._setup_workers()

    def _setup_ui(self) -> None: ...
    def _setup_workers(self) -> None: ...

    # Drag & drop
    def dragEnterEvent(self, event) -> None: ...
    def dropEvent(self, event) -> None: ...
```

### `FiltersPanel`
Painel lateral com filtros aplicáveis.

```python
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

class FiltersPanel(QWidget):
    filters_changed = Signal(object)  # emite AnalysisFilters

    def __init__(self): ...

    def get_filters(self) -> AnalysisFilters: ...
    def reset(self) -> None: ...
```

### `ResultsTable`
Tabela de resultados (usa `QTableWidget` ou `QTableView`).

```python
class ResultsTable(QWidget):
    def __init__(self): ...

    def set_report(self, report: AnalysisReport) -> None: ...
    def clear(self) -> None: ...
```

### `ProgressBar`
Barra de progresso com label de status.

```python
class ProgressBar(QWidget):
    def __init__(self): ...

    def set_progress(self, current: int, total: int) -> None: ...
    def set_status(self, text: str) -> None: ...
```

---

## Sistema de Workers (Threads)

### Por que threads?

A janela do Qt roda na **main thread**. Se o processamento de log rodar nessa thread, a janela congela (RNF-02 violado).

### Worker para análise

```python
from PySide6.QtCore import QObject, Signal, QThread

class AnalysisWorker(QObject):
    progress = Signal(int, int)         # bytes_processed, total_bytes
    finished = Signal(object)           # AnalysisReport
    error = Signal(str)                 # mensagem de erro
    file_started = Signal(str, int)     # path, size
    file_completed = Signal(str, int)   # path, entries

    def __init__(
        self,
        analyzer: LogAnalyzer,
        path: Path,
        filters: AnalysisFilters | None = None,
    ):
        super().__init__()
        self.analyzer = analyzer
        self.path = path
        self.filters = filters

    def run(self) -> None:
        """Rodado em thread separada. NÃO toca em widgets diretamente."""
        try:
            report = self.analyzer.analyze(self.path, filters=self.filters)
            self.finished.emit(report)
        except Exception as e:
            self.error.emit(str(e))
```

### Uso no MainWindow

```python
def _start_analysis(self, path: Path) -> None:
    self.thread = QThread()
    self.worker = AnalysisWorker(self.analyzer, path, self.filters)
    self.worker.moveToThread(self.thread)

    # Conectar sinais
    self.thread.started.connect(self.worker.run)
    self.worker.finished.connect(self._on_analysis_finished)
    self.worker.error.connect(self._on_analysis_error)
    self.worker.progress.connect(self.progress_bar.set_progress)
    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)

    self.thread.start()
```

---

## Observer para Progresso (Adapter para Qt)

```python
from PySide6.QtCore import QObject, Signal
from log_sentinel.core import ProgressObserver

class QtProgressObserver(QObject):
    """Adapta o ProgressObserver do Core para Qt Signals."""

    progress_signal = Signal(int, int)
    file_start_signal = Signal(str, int)
    file_complete_signal = Signal(str, int)
    error_signal = Signal(str, str)

    def on_file_start(self, path: Path, total_bytes: int) -> None:
        self.file_start_signal.emit(str(path), total_bytes)

    def on_progress(self, bytes_processed: int, total_bytes: int) -> None:
        self.progress_signal.emit(bytes_processed, total_bytes)

    def on_file_complete(self, path: Path, entries_parsed: int) -> None:
        self.file_complete_signal.emit(str(path), entries_parsed)

    def on_error(self, path: Path, error: Exception) -> None:
        self.error_signal.emit(str(path), str(error))
```

---

## Estrutura do Código

```
src/log_sentinel/gui/
├── __init__.py
├── __main__.py              # Ponto de entrada (python -m log_sentinel.gui)
├── app.py                   # QApplication setup
├── main_window.py           # MainWindow
├── workers.py               # AnalysisWorker, BatchWorker
├── observers.py             # QtProgressObserver
├── widgets/
│   ├── __init__.py
│   ├── file_picker.py       # Botão e área de drag & drop
│   ├── filters_panel.py     # Painel lateral
│   ├── results_table.py     # Tabela de resultados
│   ├── metrics_card.py      # Card de métricas gerais
│   └── progress_bar.py      # Barra de progresso
├── dialogs/
│   ├── __init__.py
│   ├── error_dialog.py      # Diálogos de erro
│   └── export_dialog.py     # Diálogo de exportação
└── resources/
    ├── icons/
    └── styles.qss           # Estilo Qt (CSS-like)
```

---

## Regras Importantes

⚠️ **NUNCA** importar nada do Core que faça I/O dentro da main thread.
⚠️ **NUNCA** modificar widgets de uma thread que não seja a main thread.
⚠️ **NUNCA** colocar regex ou regra de negócio dentro de `gui/`.

✅ A GUI **apenas**:
1. Captura input do usuário (cliques, drag & drop).
2. Configura filtros baseados na UI.
3. Dispara workers para o Core.
4. Recebe sinais e atualiza widgets.

✅ Comunicação entre Worker e UI **sempre** via `Signal`/`Slot`.

---

## Paridade com CLI (RN-03)

Toda funcionalidade da GUI deve ter equivalente na CLI:

| GUI | CLI |
|---|---|
| Botão "Selecionar arquivo" | `analyze ARQUIVO` |
| Botão "Adicionar diretório" | `batch DIRETORIO` |
| Campo "Filtrar por IP" | `--ip` |
| Checkbox "Status 5xx" | `--status-code 500` |
| Checkbox "Detectar força bruta" | `detect brute-force` |
| Botão "Exportar JSON" | `--output FILE` |

Sempre que adicionar um campo na GUI, adicione a flag equivalente na CLI (e vice-versa).
