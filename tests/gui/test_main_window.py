"""Testes da MainWindow."""
from python_pdm_template.gui.main_window import MainWindow


def test_janela_abre(qtbot) -> None:
    janela = MainWindow()
    qtbot.addWidget(janela)
    assert janela.windowTitle() == "Log Sentinel"
