import pytest
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




def test_cli_analyze_help_exit_zero():
  
    with pytest.raises(SystemExit) as exc:
        main(["analyze", "--help"])
    assert exc.value.code == 0


def test_cli_analyze_arquivo_vazio(tmp_path, capsys):
    arquivo_vazio = tmp_path / "vazio.log"
    arquivo_vazio.touch()

    exit_code = main(["analyze", str(arquivo_vazio)])
    saida = capsys.readouterr().out
    
    assert exit_code == 0
    assert "Nenhuma anomalia" in saida


def test_cli_analyze_conta_descartadas(tmp_path, capsys):
    arquivo_misto = tmp_path / "misto.log"
    conteudo = (
        '192.168.1.1 - - [10/Oct/2000:13:55:36 -0700] "GET / HTTP/1.0" 200 2326\n'
        'aaa\n'
        'bbb\n'
    )
    arquivo_misto.write_text(conteudo)

    exit_code = main(["analyze", str(arquivo_misto)])
    saida = capsys.readouterr().out
    
    assert exit_code == 0
    assert "Linhas descartadas: 2" in saida