"""Ponto de entrada da GUI do Log Sentinel."""
import sys

from PySide6.QtWidgets import QApplication

from python_pdm_template.gui.main_window import MainWindow


def main() -> None:
      """Sobe a QApplication e mostra a janela principal."""
      app = QApplication(sys.argv)
      window = MainWindow()
      window.show()
      sys.exit(app.exec())


if __name__ == "__main__":
      main()
