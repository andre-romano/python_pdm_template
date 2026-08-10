"""Interface abstrata para detectores do Core."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator

from python_pdm_template.core.models import Detection, LogEntry


class BaseDetector(ABC):
    """Contrato comum para todos os detectores do pipeline."""

    @abstractmethod
    def process(self, entries: Iterable[LogEntry]) -> Iterator[Detection]:
        """Consome LogEntries e emite Detection quando o criterio e atingido."""
