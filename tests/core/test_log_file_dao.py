import hashlib
from pathlib import Path
from python_pdm_template.core.dao.log_file_dao import LogFileDAO

def test_log_file_dao_streaming_and_hash():
    # Aponta para a fixture de 3 linhas
    fixture_path = Path("tests/fixtures/sample.log")
    
    # Calcula o hash SHA-256 esperado manualmente para conferência
    with open(fixture_path, 'rb') as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()
        
    # Inicializa o DAO e consome as linhas
    dao = LogFileDAO(fixture_path)
    linhas = list(dao.read_lines())
    
    # As asserções exigidas pelo documento
    assert len(linhas) == 3
    assert dao.digest == expected_hash