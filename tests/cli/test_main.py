from python_pdm_template.cli.main import main


def test_cli_analyze_sem_deteccao(capsys):
    exit_code = main(["analyze", "tests/fixtures/sample.log"])
    saida = capsys.readouterr().out
    assert exit_code == 0
    assert "Nenhuma anomalia identificada" in saida


def test_cli_analyze_detecta_brute_force(capsys):
    exit_code = main(["analyze", "tests/fixtures/sample_brute_force.log"])
    saida = capsys.readouterr().out
    assert exit_code == 1
    assert "brute_force" in saida
    assert "10.0.0.99" in saida


def test_cli_analyze_arquivo_inexistente(capsys):
    exit_code = main(["analyze", "arquivo/inexistente.log"])
    err = capsys.readouterr().err
    assert exit_code == 2
    assert "nao encontrado" in err.lower()
