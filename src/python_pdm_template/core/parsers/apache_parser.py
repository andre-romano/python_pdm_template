"""Parser de linhas de log Apache nos formatos Common e Combined."""
from __future__ import annotations

import re

from python_pdm_template.core.models import LogEntry


class ParseError(Exception):
    """Levantada quando uma linha nao casa com nenhum formato conhecido."""


class ApacheParser:
    """Parser para os formatos Common e Combined do Apache."""

    COMBINED_REGEX = re.compile(
        r'^(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\S+) '
        r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"$'
    )

    COMMON_REGEX = re.compile(
        r'^(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\S+)$'
    )

    def parse_line(self, line: str, line_number: int) -> LogEntry:
        """Parse a linha de log em LogEntry ou levanta ParseError."""
        line = line.rstrip()
        match = self.COMBINED_REGEX.match(line) or self.COMMON_REGEX.match(line)
        if not match:
            raise ParseError(f"Linha malformada na linha {line_number}")

        data = match.groupdict()
        size_str = data.get("size") or "-"
        size = 0 if size_str == "-" else int(size_str)

        return LogEntry(
            ip=data["ip"],
            timestamp=data["timestamp"],
            method=data["method"],
            path=data["url"],
            protocol=data["protocol"],
            status=int(data["status"]),
            bytes_sent=size,
            referer=data.get("referer"),
            user_agent=data.get("user_agent"),
        )