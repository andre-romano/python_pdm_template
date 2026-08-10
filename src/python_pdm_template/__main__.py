"""Ponto de entrada do pacote. Delega para a CLI do Log Sentinel."""
from __future__ import annotations

import sys

from python_pdm_template.cli.main import main


if __name__ == "__main__":
    sys.exit(main())
