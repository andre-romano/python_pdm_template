"""Agregador de deteccoes em relatorio consolidado."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from python_pdm_template.core.models import Detection


@dataclass
class Report:
    """Relatorio consolidado de deteccoes."""

    total_detections: int = 0
    detections_by_type: dict[str, list[Detection]] = field(default_factory=dict)


class Aggregator:
    """Agrega um stream de deteccoes em um Report."""

    def aggregate(self, detections: Iterable[Detection]) -> Report:
        """Consome as deteccoes e devolve um Report consolidado por tipo."""
        report = Report()
        for detection in detections:
            report.total_detections += 1
            report.detections_by_type.setdefault(detection.type, []).append(detection)
        return report