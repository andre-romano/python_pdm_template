# Estratégia de Testes (TDD)

## Filosofia

O Log Sentinel adota **Test-Driven Development (TDD)**: testes são escritos **antes** da implementação. Isto garante:

- Código testável por design
- Cobertura natural ≥ 80%
- Documentação executável do comportamento esperado
- Confiança para refatorar

## Ciclo TDD (Red-Green-Refactor)

```
1. RED    → Escrever teste que falha
2. GREEN  → Implementar o mínimo para passar
3. REFACTOR → Melhorar o código mantendo o teste verde
```

## Pirâmide de Testes

```
            /\
           /  \         Testes E2E
          /    \        (poucos, lentos, caros)
         /------\
        /        \      Testes de Integração
       /          \     (médios, validam interação entre módulos)
      /------------\
     /              \   Testes Unitários
    /                \  (muitos, rápidos, isolados)
   /__________________\
```

### Distribuição esperada

| Tipo | % do total | Onde |
|---|---|---|
| Unitários | ~70% | `tests/core/`, `tests/cli/`, `tests/gui/` |
| Integração | ~25% | `tests/integration/` |
| E2E | ~5% | `tests/e2e/` |

---

## Estrutura de Testes

```
tests/
├── conftest.py              # Fixtures globais
├── core/
│   ├── conftest.py          # Fixtures do core
│   ├── test_models.py
│   ├── test_parsers/
│   │   ├── test_apache_parser.py
│   │   └── test_parser_factory.py
│   ├── test_detectors/
│   │   ├── test_brute_force.py
│   │   ├── test_scanner.py
│   │   └── test_traffic_spike.py
│   ├── test_pipeline.py
│   ├── test_dao/
│   │   ├── test_log_file_dao.py
│   │   └── test_report_dao.py
│   ├── test_factories.py
│   └── test_analyzer.py
├── cli/
│   ├── test_analyze_command.py
│   ├── test_batch_command.py
│   └── test_detect_command.py
├── gui/
│   ├── test_workers.py
│   └── test_filters_panel.py
├── integration/
│   ├── test_full_analysis.py
│   └── test_cli_gui_parity.py
├── e2e/
│   └── test_real_log_files.py
└── fixtures/
    ├── sample_logs/
    │   ├── apache_common_valid.log
    │   ├── apache_combined_valid.log
    │   ├── apache_with_bruteforce.log
    │   ├── apache_with_scanner.log
    │   ├── empty.log
    │   ├── corrupted.log
    │   └── not_a_log.txt
    └── factories.py         # Factories para gerar dados de teste
```

---

## Fixtures Importantes

### `conftest.py` global

```python
import pytest
from pathlib import Path

@pytest.fixture
def fixtures_dir() -> Path:
    """Caminho da pasta de fixtures de teste."""
    return Path(__file__).parent / "fixtures"

@pytest.fixture
def sample_apache_log(fixtures_dir: Path) -> Path:
    return fixtures_dir / "sample_logs" / "apache_common_valid.log"
```

### Fixtures de dados

```python
# tests/fixtures/factories.py
from datetime import datetime
from log_sentinel.core.models import LogEntry

def make_log_entry(
    ip: str = "127.0.0.1",
    timestamp: datetime | None = None,
    method: str = "GET",
    path: str = "/",
    status: int = 200,
    bytes_sent: int = 1024,
) -> LogEntry:
    """Factory para criar LogEntry de teste."""
    return LogEntry(
        ip=ip,
        timestamp=timestamp or datetime(2026, 4, 15, 12, 0, 0),
        method=method,
        path=path,
        protocol="HTTP/1.1",
        status=status,
        bytes_sent=bytes_sent,
    )
```

---

## Padrões de Teste

### 1. Nomenclatura

```python
def test_<o_que_está_sendo_testado>_<contexto>_<resultado_esperado>():
    pass

# Exemplos
def test_parse_linha_valida_retorna_log_entry(): ...
def test_parse_linha_invalida_retorna_none(): ...
def test_brute_force_detector_threshold_100_identifica_ip_correto(): ...
```

### 2. Estrutura AAA (Arrange-Act-Assert)

```python
def test_analyzer_filtra_por_status_code():
    # Arrange
    parser = ApacheLogParser()
    analyzer = LogAnalyzer(parser=parser, file_dao=MockLogDAO([
        make_log_entry(status=200),
        make_log_entry(status=404),
        make_log_entry(status=500),
    ]))
    filters = AnalysisFilters(status_codes=[404, 500])

    # Act
    report = analyzer.analyze(Path("dummy"), filters=filters)

    # Assert
    assert report.metrics.total_requests == 2
```

### 3. Um conceito por teste

❌ Ruim — testa duas coisas:
```python
def test_parser():
    assert parser.parse(valid_line).status == 200
    assert parser.parse(invalid_line) is None
```

✅ Bom — separado:
```python
def test_parse_linha_valida_extrai_status_code():
    assert parser.parse(valid_line).status == 200

def test_parse_linha_invalida_retorna_none():
    assert parser.parse(invalid_line) is None
```

---

## Quando Usar Mocks

### ✅ Use mocks quando:

- O código depende de I/O (arquivos, rede, banco)
- O código depende de outro componente complexo
- Você quer isolar a unidade testada

### Exemplo: testando `LogAnalyzer` sem tocar disco

```python
from unittest.mock import MagicMock

def test_analyzer_chama_dao_para_ler_arquivo():
    # Arrange
    mock_dao = MagicMock(spec=LogFileDAO)
    mock_dao.read_lines.return_value = iter([
        '127.0.0.1 - - [10/Oct/2026:13:55:36 +0000] "GET / HTTP/1.1" 200 1024',
    ])
    mock_dao.get_size.return_value = 100

    analyzer = LogAnalyzer(
        parser=ApacheLogParser(),
        file_dao=mock_dao,
    )

    # Act
    report = analyzer.analyze(Path("fake.log"))

    # Assert
    mock_dao.read_lines.assert_called_once_with(Path("fake.log"))
    assert report.metrics.total_requests == 1
```

### ❌ Não use mocks quando:

- Está testando código puro (sem dependências externas)
- O componente real é simples e rápido (ex: dataclass)

---

## Testes de Defeitos (Edge Cases)

Para cada funcionalidade, escrever testes de defeitos:

### Categoria: Inputs inválidos
- Arquivo inexistente
- Arquivo vazio
- Arquivo binário (PDF, imagem)
- Arquivo com encoding errado
- Linha mal-formada no meio do arquivo
- Permissão negada

### Categoria: Limites
- Arquivo com 0 bytes
- Arquivo com 1 byte
- Arquivo gigante (> 1GB) — usar fixture sintética
- IP IPv6
- Status code não-padrão (ex: 999)

### Categoria: Concorrência (GUI)
- Cancelar análise no meio
- Iniciar análise enquanto outra está rodando
- Fechar janela durante análise

### Exemplo

```python
class TestAnalyzerDefeitos:

    def test_arquivo_inexistente_levanta_file_not_found(self, analyzer):
        with pytest.raises(FileNotFoundError):
            analyzer.analyze(Path("/inexistente.log"))

    def test_arquivo_binario_levanta_invalid_format_error(self, analyzer, fixtures_dir):
        binary_file = fixtures_dir / "sample.pdf"
        with pytest.raises(InvalidLogFormatError) as exc:
            analyzer.analyze(binary_file)
        assert "binário" in str(exc.value).lower() or "formato" in str(exc.value).lower()

    def test_arquivo_vazio_retorna_relatorio_vazio(self, analyzer, fixtures_dir):
        empty = fixtures_dir / "empty.log"
        report = analyzer.analyze(empty)
        assert report.metrics.total_requests == 0
        assert len(report.suspicious_ips) == 0
```

---

## Testes de Validação (Acceptance Tests)

Validam que o sistema atende aos casos de uso. Localização: `tests/integration/` e `tests/e2e/`.

```python
def test_cu_01_investigacao_de_ataque(fixtures_dir, tmp_path):
    """CU-01: detectar força bruta e exportar relatório."""
    # Arrange
    log_file = fixtures_dir / "apache_with_bruteforce.log"
    output_file = tmp_path / "suspeitos.json"

    # Act — simula o que o usuário faria via CLI
    from typer.testing import CliRunner
    from log_sentinel.cli.main import app

    runner = CliRunner()
    result = runner.invoke(app, [
        "detect", "brute-force", str(log_file),
        "--threshold", "100",
        "--window", "5m",
        "--output", str(output_file),
    ])

    # Assert
    assert result.exit_code == 0
    assert output_file.exists()

    import json
    data = json.loads(output_file.read_text())
    assert len(data["suspicious_ips"]) > 0
    assert any(ip["reason"] == "brute-force" for ip in data["suspicious_ips"])
```

---

## Cobertura

### Meta: 80% mínimo

```bash
python -m pdm run pytest --cov=src --cov-report=html --cov-report=term
```

### Verificar relatório

```bash
# Ver no navegador
open htmlcov/index.html

# Ver no terminal
coverage report --show-missing
```

### O que NÃO precisa ser testado

- Imports
- `__main__` blocks (`if __name__ == "__main__"`)
- Definições de tipo (Protocols, dataclasses)
- Código auto-gerado

Use `# pragma: no cover` quando justificado:
```python
if __name__ == "__main__":  # pragma: no cover
    main()
```

---

## Ordem de Implementação Recomendada (TDD)

Para cada módulo do Core:

1. **Models** — escrever testes de criação e validação
2. **Parsers** — escrever testes com linhas reais e inválidas
3. **DAO** — escrever testes com mocks de filesystem
4. **Detectors** — escrever testes com cenários conhecidos
5. **Pipeline** — escrever testes de integração entre os anteriores
6. **Analyzer (Facade)** — escrever testes de fluxo completo

Para cada teste:
1. Escreva o teste
2. Rode (`pytest tests/core/test_xxx.py -v`)
3. Veja falhar (RED)
4. Implemente o mínimo no Core
5. Rode novamente (GREEN)
6. Refatore se necessário

---

## Dicas para o Claude Code

Quando o Claude Code receber a tarefa de implementar uma nova funcionalidade:

1. Pedir para ele escrever os testes primeiro.
2. Rodar `pytest` para ver os testes falharem.
3. Pedir a implementação.
4. Rodar `pytest --cov` para verificar cobertura.
5. Refatorar se necessário.

Exemplo de prompt:
> "Implemente o `BruteForceDetector` seguindo TDD: primeiro escreva os testes em `tests/core/test_detectors/test_brute_force.py`, rode-os para confirmar que falham, depois implemente em `src/log_sentinel/core/detectors/brute_force.py`."
