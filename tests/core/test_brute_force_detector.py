from pathlib import Path
from python_pdm_template.core.parsers.apache_parser import ApacheParser
from python_pdm_template.core.dao.log_file_dao import LogFileDAO
from python_pdm_template.core.detectors.brute_force_detector import BruteForceDetector

def test_brute_force_detector_positivo():
    parser = ApacheParser()
    dao = LogFileDAO(Path("tests/fixtures/sample_brute_force.log"))
    detector = BruteForceDetector(threshold=10, window_seconds=60)
    
    entries = (parser.parse_line(line, i) for i, line in enumerate(dao.read_lines()))
    detections = list(detector.process(entries))
    
    assert len(detections) >= 1
    assert detections[0].ip == "10.0.0.99"
    assert detections[0].type == "brute_force"

def test_brute_force_detector_negativo():
    parser = ApacheParser()
    dao = LogFileDAO(Path("tests/fixtures/sample.log"))
    detector = BruteForceDetector(threshold=10, window_seconds=60)
    
    entries = (parser.parse_line(line, i) for i, line in enumerate(dao.read_lines()))
    detections = list(detector.process(entries))
    
    assert len(detections) == 0