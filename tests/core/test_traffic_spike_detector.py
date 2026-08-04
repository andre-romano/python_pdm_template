from python_pdm_template.core.detectors.traffic_spike_detector import TrafficSpikeDetector
from python_pdm_template.core.models import LogEntry


def test_traffic_spike_detector_iteracao_1():
    detector = TrafficSpikeDetector()
    entry = LogEntry(
        ip="127.0.0.1",
        timestamp="10/Oct/2000:13:00:00 -0700",
        method="GET",
        path="/",
        protocol="HTTP/1.0",
        status=200,
        bytes_sent=0,
        referer=None,
        user_agent=None,
    )
    entries = [entry for _ in range(101)]
    detections = list(detector.process(entries))
    assert len(detections) >= 1
    assert detections[0].type == "traffic_spike"