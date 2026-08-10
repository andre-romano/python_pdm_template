"""Modelos de dados do Core."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class LogEntry:
    """Uma entrada parseada de log Apache."""

    ip: str
    timestamp: datetime
    method: str
    path: str
    protocol: str
    status: int
    bytes_sent: int
    referer: str | None = None
    user_agent: str | None = None

@dataclass
class Detection:
    """Registro de uma deteccao emitida por um detector."""

    type: str
    ip: str
    count: int
    message: str
