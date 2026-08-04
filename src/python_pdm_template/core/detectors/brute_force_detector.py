"""Detector de forca bruta em janela de tempo deslizante."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Iterator

from datetime import datetime

from python_pdm_template.core.models import LogEntry, Detection

from typing import override
from python_pdm_template.core.detectors.base import BaseDetector



class BruteForceDetector(BaseDetector):
    """Detector de forca bruta baseado em janela deslizante."""

    def __init__(self, threshold: int = 10, window_seconds: int = 60) -> None:
        """Define limiar de tentativas e tamanho da janela em segundos."""
        self.threshold = threshold
        self.window_seconds = window_seconds
        
    @override                                                                
    def process(self, entries: Iterable[LogEntry]) -> Iterator[Detection]:
        """Consome LogEntries e emite Detection quando o limiar e atingido."""
        history: dict[str, list[datetime]] = defaultdict(list)

        for entry in entries:
            if entry.status not in (401, 403):
                continue
            try:
                time_str = entry.timestamp.split()[0]
                dt = datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S")
            except (ValueError, AttributeError):
                continue

            ip = entry.ip
            history[ip].append(dt)
            history[ip] = [
                t for t in history[ip]
                if (dt - t).total_seconds() <= self.window_seconds
            ]

            if len(history[ip]) >= self.threshold:
                yield Detection(
                    type="brute_force",
                    ip=ip,
                    count=len(history[ip]),
                    message=f"Brute-force: {len(history[ip])} tentativas do IP {ip}",
                )
                history[ip] = []