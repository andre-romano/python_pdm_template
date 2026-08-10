"""Pipeline Pipe-and-Filter integrando DAO, parser e detectores."""
from __future__ import annotations

from collections.abc import Iterator

from python_pdm_template.core.dao.log_file_dao import LogFileDAO
from python_pdm_template.core.models import Detection
from python_pdm_template.core.parsers.apache_parser import ApacheParser


class Pipeline:
    """Integra DAO, Parser e multiplos Detectores."""

    def __init__(
        self,
        dao: LogFileDAO,
        parser: ApacheParser,
        detectors: list,
    ) -> None:
        """Guarda as dependencias do pipeline."""
        self.dao = dao
        self.parser = parser
        self.detectors = detectors

    def run(self) -> Iterator[Detection]:
        """Le as linhas, faz parse e passa por todos os detectores."""
        entries = [
            self.parser.parse_line(line, i)
            for i, line in enumerate(self.dao.read_lines(), start=1)
        ]
        for detector in self.detectors:
            yield from detector.process(entries)