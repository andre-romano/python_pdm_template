# Design da CLI

> Responsável: **Rodrigo** — Engenheiro de CLI

## Tecnologias

- **Typer** — framework de CLI baseado em type hints
- **Rich** — formatação rica no terminal (tabelas, cores, barras de progresso)

## Estrutura de Comandos

```
log-sentinel                          # mostra ajuda geral
log-sentinel --version                # mostra versão
log-sentinel --help                   # ajuda detalhada

log-sentinel analyze <arquivo>        # analisa um único arquivo
log-sentinel batch <diretório>        # analisa múltiplos arquivos
log-sentinel detect <tipo> <arquivo>  # detecção específica
log-sentinel formats                  # lista formatos suportados
```

## Subcomando: `analyze`

Analisa um único arquivo de log.

### Sintaxe
```bash
log-sentinel analyze ARQUIVO [OPTIONS]
```

### Opções
| Flag | Tipo | Default | Descrição |
|---|---|---|---|
| `--format` | str | `apache` | Formato do log |
| `--ip` | str | None | Filtrar por IP específico |
| `--status-code` | int (múltiplo) | None | Filtrar por código HTTP |
| `--date-start` | str | None | Data início (ISO 8601) |
| `--date-end` | str | None | Data fim (ISO 8601) |
| `--output` | path | None | Salvar relatório em arquivo |
| `--output-format` | str | `json` | Formato do relatório (json) |
| `--display` | str | `table` | Exibição no terminal (table\|json\|none) |
| `--verbose, -v` | flag | False | Output detalhado |
| `--quiet, -q` | flag | False | Apenas erros |

### Exemplos
```bash
# Análise simples com tabela no terminal
log-sentinel analyze access.log

# Filtrar erros 500 e 404
log-sentinel analyze access.log --status-code 500 --status-code 404

# Filtrar por IP e período
log-sentinel analyze access.log \
  --ip 192.168.1.100 \
  --date-start "2026-04-15T00:00:00" \
  --date-end "2026-04-15T23:59:59"

# Exportar para JSON
log-sentinel analyze access.log --output relatorio.json --display none
```

---

## Subcomando: `batch`

Analisa múltiplos arquivos.

### Sintaxe
```bash
log-sentinel batch CAMINHO [OPTIONS]
```

`CAMINHO` pode ser:
- Um diretório (processa todos os `.log` dentro)
- Múltiplos arquivos: `file1.log file2.log file3.log`

### Opções
Todas as do `analyze`, mais:

| Flag | Tipo | Default | Descrição |
|---|---|---|---|
| `--recursive, -r` | flag | False | Buscar logs em subdiretórios |
| `--pattern` | str | `*.log` | Padrão glob para arquivos |
| `--workers` | int | 1 | Processar em paralelo (futuro) |

### Exemplos
```bash
# Diretório inteiro
log-sentinel batch /var/log/apache/

# Recursivo com padrão
log-sentinel batch /var/log/ --recursive --pattern "*.log"

# Múltiplos arquivos explícitos
log-sentinel batch access.log error.log other.log --output consolidado.json
```

---

## Subcomando: `detect`

Aplica detecções específicas.

### Sintaxe
```bash
log-sentinel detect TIPO ARQUIVO [OPTIONS]
```

`TIPO` pode ser: `brute-force`, `scanner`, `traffic-spike`

### `detect brute-force`

```bash
log-sentinel detect brute-force ARQUIVO [OPTIONS]
```

| Flag | Tipo | Default | Descrição |
|---|---|---|---|
| `--threshold` | int | 100 | Mínimo de requisições para alertar |
| `--window` | str | `5m` | Janela de tempo (ex: `5m`, `1h`) |

### `detect scanner`

```bash
log-sentinel detect scanner ARQUIVO [OPTIONS]
```

| Flag | Tipo | Default | Descrição |
|---|---|---|---|
| `--suspicious-paths` | str | (lista padrão) | Paths considerados suspeitos (CSV) |
| `--min-distinct-paths` | int | 5 | Mínimo de paths distintos para alertar |

### `detect traffic-spike`

```bash
log-sentinel detect traffic-spike ARQUIVO [OPTIONS]
```

| Flag | Tipo | Default | Descrição |
|---|---|---|---|
| `--baseline-hours` | int | 24 | Horas usadas como baseline |
| `--multiplier` | float | 3.0 | Quantas vezes acima da média conta como pico |

---

## Subcomando: `formats`

Lista formatos de log suportados.

```bash
$ log-sentinel formats
Formatos suportados:
  • apache (Common Log Format e Combined Log Format)
```

---

## Saída no Terminal

### Modo `table` (padrão)

Usa Rich para renderizar tabelas formatadas:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📊 Análise de access.log                                     ┃
┃ Período: 2026-04-15 00:00 a 2026-04-15 23:59                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─ Métricas Gerais ──────────────────────────────────────────┐
│ Total de requisições:    15.234                            │
│ IPs únicos:              892                               │
│ Bytes transferidos:      2.3 GB                            │
└────────────────────────────────────────────────────────────┘

📈 Top 10 IPs
┌──────────────────┬──────────┬─────────┐
│ IP               │ Requests │ %       │
├──────────────────┼──────────┼─────────┤
│ 192.168.1.100    │ 3.421    │ 22.5%   │
│ 10.0.0.5         │ 1.892    │ 12.4%   │
│ ...              │ ...      │ ...     │
└──────────────────┴──────────┴─────────┘

⚠️  IPs Suspeitos (3)
┌──────────────────┬─────────────┬──────────┬───────┐
│ IP               │ Motivo      │ Requests │ Risco │
├──────────────────┼─────────────┼──────────┼───────┤
│ 203.0.113.42     │ brute-force │ 542      │ ALTO  │
│ ...              │ ...         │ ...      │ ...   │
└──────────────────┴─────────────┴──────────┴───────┘
```

### Modo `json`

Imprime o JSON puro no stdout (útil para piping):

```bash
log-sentinel analyze access.log --display json | jq .suspicious_ips
```

---

## Barras de Progresso

Durante o processamento, usar `rich.progress`:

```
Analisando access.log (1.2 GB)
[████████████████░░░░░░░░░░░░░░░░░░] 47% • 564 MB / 1.2 GB • ETA: 12s
```

---

## Tratamento de Erros

| Situação | Comportamento | Exit Code |
|---|---|---|
| Arquivo não encontrado | Mensagem em vermelho + dica | 2 |
| Formato inválido (RN-02) | Mensagem clara + sugestão | 3 |
| Permissão negada | Mensagem em vermelho | 4 |
| Argumento inválido | Mostrar `--help` | 5 |
| Erro inesperado | Stack trace (com `--verbose`) | 1 |

Exemplo:
```
$ log-sentinel analyze inexistente.log
❌ Erro: Arquivo 'inexistente.log' não encontrado.
💡 Verifique se o caminho está correto. Use ls para listar os arquivos.
```

---

## Estrutura do Código

```
src/log_sentinel/cli/
├── __init__.py
├── main.py                    # App Typer principal
├── commands/
│   ├── __init__.py
│   ├── analyze.py             # Comando analyze
│   ├── batch.py               # Comando batch
│   ├── detect.py              # Comando detect (com subcomandos)
│   └── formats.py             # Comando formats
├── observers.py               # RichProgressObserver
├── renderers.py               # Funções para renderizar tabelas Rich
└── exceptions.py              # Exceções específicas da CLI
```

## Regras Importantes

⚠️ **NUNCA** colocar regex, lógica de contagem ou regra de negócio dentro de `cli/`.
✅ A CLI **apenas**:
1. Recebe argumentos.
2. Valida-os (tipo, formato).
3. Chama o `LogAnalyzer` do Core.
4. Renderiza o resultado.

Exemplo correto:

```python
# cli/commands/analyze.py
import typer
from log_sentinel.core import LogAnalyzer, LogParserFactory, AnalysisFilters
from log_sentinel.cli.renderers import render_report
from log_sentinel.cli.observers import RichProgressObserver

def analyze(
    arquivo: Path,
    formato: str = "apache",
    status_code: list[int] = typer.Option(None),
    output: Path | None = None,
) -> None:
    """Analisa um arquivo de log."""
    parser = LogParserFactory.create(formato)
    observer = RichProgressObserver()
    analyzer = LogAnalyzer(parser=parser, observers=[observer])

    filters = AnalysisFilters(status_codes=status_code)
    report = analyzer.analyze(arquivo, filters=filters)

    render_report(report)
    if output:
        ReportFactory.create("json").save(report, output)
```
