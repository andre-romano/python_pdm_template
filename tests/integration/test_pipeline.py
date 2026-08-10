from pathlib import Path
from python_pdm_template.core.dao.log_file_dao import LogFileDAO
from python_pdm_template.core.parsers.apache_parser import ApacheParser
from python_pdm_template.core.detectors.brute_force_detector import BruteForceDetector
from python_pdm_template.core.detectors.scanner_detector import ScannerDetector
from python_pdm_template.core.detectors.traffic_spike_detector import TrafficSpikeDetector
from python_pdm_template.core.pipeline import Pipeline
from python_pdm_template.core.aggregator import Aggregator

def test_pipeline_completo():
    # Setup dos componentes
    dao = LogFileDAO(Path("tests/fixtures/sample_brute_force.log"))
    parser = ApacheParser()
    detectors = [
        BruteForceDetector(threshold=10, window_seconds=60),
        ScannerDetector(threshold=2, window_seconds=60),
        TrafficSpikeDetector()
    ]
    
    # Executa o pipeline
    pipeline = Pipeline(dao, parser, detectors)
    detections = list(pipeline.run())
    
    # Agrega os resultados
    aggregator = Aggregator()
    report = aggregator.aggregate(detections)
    
    # Baseado no sample_brute_force.log, esperamos pelo menos a detecção de brute_force
    assert report.total_detections >= 1
    assert "brute_force" in report.detections_by_type
    assert report.detections_by_type["brute_force"][0].ip == "10.0.0.99"