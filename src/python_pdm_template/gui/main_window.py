"""Janela principal da GUI do Log Sentinel."""
from __future__ import annotations

# Adicionamos o QLineEdit (caixa de texto), QHBoxLayout (organização de lado) e QLabel (texto)
from PySide6.QtWidgets import (QMainWindow, QTableView, QPushButton, 
                               QVBoxLayout, QHBoxLayout, QWidget, 
                               QFileDialog, QProgressBar, QLineEdit, QLabel)
# Adicionamos o QSortFilterProxyModel (a nossa peneira de detetive) e o Qt
from PySide6.QtCore import QSortFilterProxyModel, Qt
from python_pdm_template.gui.models import LogEntryTableModel
from python_pdm_template.gui.workers import ParserWorker


class MainWindow(QMainWindow):
    """Janela principal do Log Sentinel."""

    def __init__(self) -> None:
        """Inicializa a janela principal com filtros, tabela e drag-and-drop."""
        super().__init__()
        self.setWindowTitle("Log Sentinel")
        self.resize(1024, 768)

        # --- [COMMIT 4] Ativa o Drag and Drop ---
        # Diz para a janela: "Pode aceitar arquivos arrastados para cá!"
        self.setAcceptDrops(True)

        # 1. O "Cérebro" da Tabela (Model original)
        self.model = LogEntryTableModel()
        
        # --- [COMMIT 5] Criando a Peneira (Proxy Model) ---
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        # Diz para ignorar se a letra é maiúscula ou minúscula (tanto faz!)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        # 2. O desenho da Tabela (View)
        # MUDANÇA: Agora a tabela mostra o modelo com a PENEIRA, não o original puro
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)

        # 3. O Botão e a Barrinha de Progresso
        self.btn_open = QPushButton("Abrir arquivo de log...")
        self.btn_open.clicked.connect(self.start_parsing)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # --- [COMMIT 5] Criando as Caixinhas de Texto dos Filtros ---
        self.txt_filter_ip = QLineEdit()
        self.txt_filter_ip.setPlaceholderText("Digite para filtrar por IP...")
        self.txt_filter_ip.textChanged.connect(self.filter_ip_changed)

        self.txt_filter_status = QLineEdit()
        self.txt_filter_status.setPlaceholderText("Digite para filtrar por Status...")
        self.txt_filter_status.textChanged.connect(self.filter_status_changed)

        # Colocando os filtros um do lado do outro
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar IP:"))
        filter_layout.addWidget(self.txt_filter_ip)
        filter_layout.addWidget(QLabel("Filtrar Status:"))
        filter_layout.addWidget(self.txt_filter_status)

        # 4. Organizando tudo um embaixo do outro (como blocos de Lego)
        layout = QVBoxLayout()
        layout.addLayout(filter_layout) # Filtros no topo!
        layout.addWidget(self.btn_open)
        layout.addWidget(self.table_view)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        
        # Coloca o nosso container cheio de coisas na janela!
        self.setCentralWidget(container)

    def start_parsing(self) -> None:
        """Abre o buscador de arquivos tradicional."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Escolha o Log", "", "Logs (*.log);;Todos (*.*)")
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path: str) -> None:
        """Liga o operário invisível para processar o arquivo (usado pelo botão e pelo drag and drop)."""
        # Criando o nosso operário invisível do Commit 2
        self.worker = ParserWorker(file_path)
        
        # Conectando os rádio-comunicadores (Signals)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_finished)
        
        # Mandando ele trabalhar!
        self.worker.start()
        self.btn_open.setEnabled(False) # Desliga o botão para não clicar duas vezes

    def on_finished(self, log_entries: list) -> None:
        """Recebe os dados do operário quando ele termina e joga na tabela."""
        self.model.set_data(log_entries)
        self.btn_open.setEnabled(True) # Ativa o botão de novo
        self.progress_bar.setValue(100) # Deixa a barra cheia

    # --- [COMMIT 5] Funções dos Filtros ---
    def filter_ip_changed(self, text: str) -> None:
        """Olha para a coluna 0 (IP) e filtra o que o usuário digitou."""
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setFilterFixedString(text)

    def filter_status_changed(self, text: str) -> None:
        """Olha para a coluna 3 (Status) e filtra o que o usuário digitou."""
        self.proxy_model.setFilterKeyColumn(3)
        self.proxy_model.setFilterFixedString(text)

    # --- [COMMIT 4] Funções de Arrastar e Soltar (Drag and Drop) ---
    def dragEnterEvent(self, event) -> None:  # noqa: N802
        """Verifica se o brinquedo que jogaram na janela é mesmo um arquivo."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction() # A janela diz: "Gostei, pode soltar!"

    def dropEvent(self, event) -> None:  # noqa: N802
        """Pega o caminho do arquivo que foi solto e manda ler."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            # Só vale se for um arquivo de Log que termina com .log!
            if file_path.endswith(".log"):
                self.process_file(file_path)
