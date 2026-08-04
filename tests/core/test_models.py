"""Testes do modulo de modelos (TDD - RED phase)."""
from datetime import datetime
import pytest

def test_log_entry_armazena_campos_obrigatorios():
    from python_pdm_template.core.models import LogEntry
    entry = LogEntry(
        ip="127.0.0.1",
        timestamp=datetime(2026, 5, 11, 12, 0, 0),
        method="GET",
        path="/",
        protocol="HTTP/1.1",
        status=200,
        bytes_sent=1024,
    )
    assert entry.ip == "127.0.0.1"
    assert entry.status == 200
