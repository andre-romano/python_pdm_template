"""Modelo de tabela para exibir LogEntry na GUI."""
from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, Qt


class LogEntryTableModel(QAbstractTableModel):
      """Modelo de tabela que exibe LogEntry em 4 colunas."""

      def __init__(self, data: list | None = None) -> None:
          """Inicializa com dados opcionais e define os cabecalhos."""
          super().__init__()
          self._data = data or []
          self._headers = ["IP", "Timestamp", "Metodo", "Status"]

      def rowCount(self, parent=None) -> int:  # noqa: N802, ARG002
          """Devolve o numero de linhas atuais."""
          return len(self._data)

      def columnCount(self, parent=None) -> int:  # noqa: N802, ARG002
          """Devolve o numero de colunas fixo (4)."""
          return len(self._headers)

      def data(self, index, role=Qt.ItemDataRole.DisplayRole):
          """Devolve o texto da celula pedida pelo Qt."""
          if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
              return None
          entry = self._data[index.row()]
          column = index.column()
          if column == 0:
              return getattr(entry, "ip", "")
          if column == 1:
              return getattr(entry, "timestamp", "")
          if column == 2:  # noqa: PLR2004
              return getattr(entry, "method", "")
          if column == 3:  # noqa: PLR2004
              return str(getattr(entry, "status", ""))
          return None

      def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):  # noqa: N802
          """Devolve o nome da coluna quando pedido pelo Qt."""
          if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
              return self._headers[section]
          return None

      def set_data(self, data: list) -> None:
          """Substitui a lista inteira e notifica a view."""
          self.beginResetModel()
          self._data = data
          self.endResetModel()