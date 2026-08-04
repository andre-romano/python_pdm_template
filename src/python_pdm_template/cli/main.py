"""Interface de linha de comando do Log Sentinel."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from python_pdm_template.core.aggregator import Aggregator
from python_pdm_template.core.dao.log_file_dao import LogFileDAO
from python_pdm_template.core.detectors.brute_force_detector import BruteForceDetector
from python_pdm_template.core.detectors.scanner_detector import ScannerDetector
from python_pdm_template.core.detectors.traffic_spike_detector import TrafficSpikeDetector
from python_pdm_template.core.parsers.apache_parser import ApacheParser, ParseError


def analyze(arquivo: Path) -> int:
    """Analise um arquivo de log e imprima as deteccoes encontradas."""
    if not arquivo.exists():
        print(f"Arquivo nao encontrado: {arquivo}", file=sys.stderr)
        return 2

    dao = LogFileDAO(arquivo)
    parser = ApacheParser()
    entries = []
    descartadas = 0
    for i, linha in enumerate(dao.read_lines(), start=1):
        try:
            entries.append(parser.parse_line(linha, i))
        except ParseError:
            descartadas += 1

    detectors = [
        BruteForceDetector(threshold=10, window_seconds=60),
        ScannerDetector(threshold=2, window_seconds=60),
        TrafficSpikeDetector(),
    ]

    deteccoes = []
    for det in detectors:
        deteccoes.extend(det.process(entries))

    relatorio = Aggregator().aggregate(deteccoes)

    print("=" * 60)
    print(f"Log Sentinel - relatorio de {arquivo}")
    print("=" * 60)
    print(f"Linhas processadas: {len(entries)}")
    if descartadas:
        print(f"Linhas descartadas: {descartadas}")
    print(f"Hash SHA-256:       {dao.digest}")
    print(f"Total de deteccoes: {relatorio.total_detections}")
    print()

    if relatorio.total_detections == 0:
        print("Nenhuma anomalia identificada.")
        return 0

    for tipo, itens in relatorio.detections_by_type.items():
        print(f"[{tipo}] {len(itens)} deteccao(oes):")
        for det in itens:
            print(f"  - {det.message}")
        print()
    return 1


def main(argv: list[str] | None = None) -> int:
    """Sirva como ponto de entrada da CLI."""
    argp = argparse.ArgumentParser(
        prog="log-sentinel",
        description="Analise post-mortem de logs Apache",
    )
    sub = argp.add_subparsers(dest="cmd", required=True)

    p_analyze = sub.add_parser("analyze", help="Analisa um arquivo de log")
    p_analyze.add_argument("arquivo", type=Path, help="Caminho para o arquivo de log")

    args = argp.parse_args(argv)

    if args.cmd == "analyze":
        return analyze(args.arquivo)
    argp.error(f"Comando desconhecido: {args.cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
