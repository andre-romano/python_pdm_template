"""Worker em QThread que le e parseia o log em segundo plano."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QThread, Signal

from python_pdm_template.core.dao.log_file_dao import LogFileDAO
from python_pdm_template.core.models import LogEntry
from python_pdm_template.core.parsers.apache_parser import ApacheParser, ParseError


class ParserWorker(QThread):
      """Roda o parser em thread separada para nao travar a UI."""

      progress = Signal(int)
      finished = Signal(list)

      def __init__(self, file_path: str) -> None:
          """Guarda o caminho do arquivo a ser processado."""
          super().__init__()
          self.file_path = Path(file_path)

      def run(self) -> None:
          """Le o arquivo, aplica o parser e emite a lista final."""
          dao = LogFileDAO(self.file_path)
          parser = ApacheParser()
          entries: list[LogEntry] = []
          for i, line in enumerate(dao.read_lines(), start=1):
              try:
                  entries.append(parser.parse_line(line, i))
              except ParseError:
                  continue
              if i % 50 == 0:
                  self.progress.emit(min(99, i % 100))
          self.progress.emit(100)
          self.finished.emit(entries)