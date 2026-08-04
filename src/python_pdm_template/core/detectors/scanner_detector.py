"""Detector de varredura a URLs sensiveis (scanners)."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Iterator
from datetime import datetime

from typing import override
from python_pdm_template.core.detectors.base import BaseDetector

from python_pdm_template.core.models import LogEntry, Detection


class ScannerDetector(BaseDetector):
    """Detecta acessos repetidos a URLs sensiveis em janela de tempo."""

    def __init__(self, threshold: int = 3, window_seconds: int = 60) -> None:
        """Define limiar de acessos e tamanho da janela em segundos."""
        self.threshold = threshold
        self.window_seconds = window_seconds
        self.sensitive_urls = ["/admin", "/.env", "/wp-login", "/.git"]
    
    @override
    def process(self, entries: Iterable[LogEntry]) -> Iterator[Detection]:
        """Consome LogEntries e emite Detection ao atingir o limiar."""
        history: dict[str, list[datetime]] = defaultdict(list)

        for entry in entries:
            if not any(s in entry.path for s in self.sensitive_urls):
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
                    type="scanner",
                    ip=ip,
                    count=len(history[ip]),
                    message=f"Scanner: {len(history[ip])} acessos sensiveis do IP {ip}",
                )
                history[ip] = []