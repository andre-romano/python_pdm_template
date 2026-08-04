from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from python_pdm_template.core.models import LogEntry, Detection

class BaseDetector(ABC):
    @abstractmethod
    def process(self, entries: Iterable[LogEntry]) -> Iterator[Detection]:
        ...