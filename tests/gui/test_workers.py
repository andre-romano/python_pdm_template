"""Testes do ParserWorker."""
from pathlib import Path

from python_pdm_template.gui.workers import ParserWorker


def test_parser_worker_processa_log(tmp_path: Path, qtbot) -> None:
    log_file = tmp_path / "access.log"
    log_file.write_text(
        '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] '
        '"GET /apache_pb.gif HTTP/1.0" 200 2326\n',
        encoding="utf-8",
    )

    worker = ParserWorker(str(log_file))
    results: list = []
    worker.finished.connect(results.extend)

    with qtbot.waitSignal(worker.finished, timeout=5000):
        worker.start()

    assert len(results) == 1
    assert results[0].ip == "127.0.0.1"
