from python_pdm_template.core.detectors.scanner_detector import ScannerDetector
from python_pdm_template.core.models import LogEntry


def _entry(ip: str, timestamp: str, path: str) -> LogEntry:
    return LogEntry(
        ip=ip,
        timestamp=timestamp,
        method="GET",
        path=path,
        protocol="HTTP/1.0",
        status=404,
        bytes_sent=0,
        referer=None,
        user_agent=None,
    )


def test_scanner_detector_positivo():
    detector = ScannerDetector(threshold=2, window_seconds=60)
    entries = [
        _entry("10.0.0.1", "10/Oct/2000:13:55:01 -0700", "/.env"),
        _entry("10.0.0.1", "10/Oct/2000:13:55:05 -0700", "/wp-login"),
    ]
    detections = list(detector.process(entries))
    assert len(detections) == 1
    assert detections[0].type == "scanner"