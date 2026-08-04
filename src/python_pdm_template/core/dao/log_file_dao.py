"""DAO para leitura de arquivos de log em streaming com hash SHA-256 integrado."""
from __future__ import annotations

import hashlib
from collections.abc import Generator
from pathlib import Path


class LogFileDAO:
    """Le arquivos de log linha-a-linha e calcula SHA-256 no mesmo passo."""

    def __init__(self, file_path: str | Path) -> None:
        """Guarda o caminho e inicializa o digest vazio."""
        self.file_path = Path(file_path)
        self._digest = ""

    @property
    def digest(self) -> str:
        """Hash SHA-256 do arquivo, disponivel apos consumir read_lines."""
        return self._digest

    def read_lines(self) -> Generator[str, None, None]:
        """Le o arquivo em modo binario (para hash exato) e devolve linhas decodificadas."""
        sha256_hash = hashlib.sha256()
        with open(self.file_path, "rb") as f:
            for line_bytes in f:
                sha256_hash.update(line_bytes)
                yield line_bytes.decode("utf-8", errors="replace")
        self._digest = sha256_hash.hexdigest()