# Convenções da Equipe

> Padrões obrigatórios para código, commits, branches e processos. Deve ser seguido por todos os integrantes (incluindo o Claude Code).

## 1. Convenções de Código

### Estilo Geral
- Seguir **PEP 8** (validado por `ruff`)
- Indentação: **4 espaços** (sem tabs)
- Comprimento máximo de linha: **100 caracteres**
- Encoding: **UTF-8**
- Quebra de linha: **LF** (Unix)

### Tipagem (Obrigatória)

```python
# ❌ Ruim
def parse(line):
    return result

# ✅ Bom
def parse(line: str) -> LogEntry | None:
    return result
```

Use `from __future__ import annotations` em todos os arquivos para evitar problemas com forward references.

### Nomenclatura

| Item | Convenção | Exemplo |
|---|---|---|
| Variáveis | `snake_case` | `request_count` |
| Funções/métodos | `snake_case` | `parse_line()` |
| Classes | `PascalCase` | `ApacheLogParser` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_FILE_SIZE` |
| Atributos privados | `_snake_case` | `_internal_buffer` |
| Pacotes/módulos | `snake_case` | `log_sentinel.core` |
| Type vars | `PascalCase` curto | `T`, `K`, `V` |

### Docstrings

Estilo: **PEP 257** com parâmetros marcados.

```python
def detect(self, entries: Iterator[LogEntry]) -> list[SuspiciousIP]:
    """Detecta IPs com comportamento de força bruta.

    Analisa as entradas em janelas deslizantes de tempo, identificando
    IPs que fazem mais requisições que o threshold configurado.

    :param entries: Iterator de entradas de log a analisar.
    :return: Lista de IPs identificados como suspeitos.
    :raises ValueError: Se threshold for menor que 1.
    """
```

### Imports

Ordem (separados por linha em branco):
1. Standard library
2. Third-party
3. Local (`log_sentinel.*`)

```python
# Standard library
import re
from datetime import datetime
from pathlib import Path
from typing import Iterator

# Third-party
import typer
from rich.console import Console

# Local
from log_sentinel.core.models import LogEntry
from log_sentinel.core.parsers.base import LogParserStrategy
```

❌ Não usar `from module import *`
❌ Não usar imports relativos (`from ..module import ...`) — usar absolutos.
✅ Usar imports absolutos sempre.

### Gerenciamento de Strings

❌ Concatenação manual:
```python
msg = "Erro em " + path + ": " + str(error)
```

✅ f-strings:
```python
msg = f"Erro em {path}: {error}"
```

### Tratamento de Erros

❌ Ruim — engole exceção:
```python
try:
    do_something()
except:
    pass
```

✅ Bom — específico e logado:
```python
try:
    do_something()
except SpecificError as e:
    logger.error("Falha em do_something: %s", e)
    raise
```

### Logging vs Print

❌ Nunca usar `print()` em código de produção.

✅ Usar `logging` para logs internos:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Processando arquivo %s", path)
```

✅ Usar Rich para output do usuário:
```python
from rich.console import Console
console = Console()
console.print("[green]✓[/green] Arquivo processado.")
```

---

## 2. Convenções de Commits

Seguimos **Conventional Commits**.

### Formato

```
<tipo>(<escopo>): <descrição curta>

<corpo opcional>

<footer opcional>
```

### Tipos

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Mudança apenas em documentação |
| `style` | Formatação, sem mudança de lógica |
| `refactor` | Refatoração sem mudança de comportamento |
| `test` | Adição ou alteração de testes |
| `chore` | Tarefas de manutenção (deps, configs) |
| `ci` | Mudanças no pipeline CI/CD |
| `perf` | Melhoria de performance |
| `build` | Mudanças no sistema de build |

### Escopos

| Escopo | Significado |
|---|---|
| `core` | Mudanças no Core |
| `cli` | Mudanças na CLI |
| `gui` | Mudanças na GUI |
| `tests` | Mudanças em testes |
| `deps` | Mudanças em dependências |
| `docs` | Mudanças em documentação |
| `ci` | Mudanças em pipelines |

### Exemplos

```bash
# Nova funcionalidade
git commit -m "feat(core): adiciona ApacheLogParser com Common Log Format"

# Correção
git commit -m "fix(cli): corrige flag --status-code aceitando múltiplos valores"

# Teste
git commit -m "test(core): adiciona testes para BruteForceDetector"

# Documentação
git commit -m "docs(api): documenta contratos do módulo de DAO"

# Refatoração
git commit -m "refactor(core): extrai lógica de validação para método separado"

# Com corpo (commits maiores)
git commit -m "feat(gui): adiciona drag & drop de arquivos

Permite arrastar arquivos .log diretamente para a janela.
Suporta múltiplos arquivos simultaneamente.

Closes #42"
```

### Regras
- Descrição em **português**
- Verbo no **imperativo** (adiciona, corrige, remove — não "adicionado", "corrigido")
- Primeira letra **minúscula**
- **Sem ponto final** na descrição curta
- Máximo **72 caracteres** na primeira linha
- Linha em branco antes do corpo
- Referenciar issues no footer (`Closes #N`, `Fixes #N`)

---

## 3. Convenções de Branches

### Branch Principal
- `main` — código estável, protegido (não aceita commits diretos)

### Branches de Feature

Formato: `<tipo>/<descricao-curta>`

```
feature/parser-apache
feature/cli-batch-command
feature/gui-drag-and-drop
fix/parser-handle-empty-lines
fix/cli-status-code-multiple-values
docs/update-readme
chore/update-dependencies
ci/add-windows-build
```

### Regras
- Tudo em **kebab-case** (palavras separadas por hífen)
- **Curto e descritivo** (máx 50 caracteres)
- Em **inglês** (mais universal para nomes de branches)
- Prefixo indica o tipo

### Ciclo de vida da branch

```
1. Criar branch a partir de main atualizada
   git checkout main
   git pull origin main
   git checkout -b feature/parser-apache

2. Desenvolver com commits frequentes

3. Manter branch atualizada
   git fetch origin
   git rebase origin/main   # ou merge, se preferir

4. Push
   git push origin feature/parser-apache

5. Abrir Pull Request

6. Após merge, deletar branch
   git checkout main
   git pull origin main
   git branch -d feature/parser-apache
```

---

## 4. Convenções de Pull Requests

### Título
Usar mesmo formato dos commits:
```
feat(core): adiciona ApacheLogParser com suporte a Combined Log Format
```

### Descrição (template)

```markdown
## O quê
Breve descrição do que foi feito.

## Por quê
Contexto e motivação. Link com a Issue:
Closes #N

## Como testar
Passo a passo para o revisor testar localmente:
1. Checkout da branch
2. `pdm install`
3. `pdm run pytest tests/core/test_parsers/test_apache_parser.py`

## Checklist
- [ ] Testes adicionados/atualizados
- [ ] Cobertura ≥ 80% na área alterada
- [ ] Documentação atualizada (se aplicável)
- [ ] Pipeline CI/CD passou
- [ ] Code review por pelo menos 1 colega
```

### Regras
- 1 PR = 1 funcionalidade ou correção
- PRs grandes (> 500 linhas) devem ser quebrados se possível
- Sempre vincular a uma Issue
- Aguardar CI verde antes de pedir review

---

## 5. Convenções de Issues

### Título
Direto e descritivo:
```
[CORE] Implementar ApacheLogParser
[CLI] Adicionar flag --status-code ao comando analyze
[GUI] Implementar drag & drop de arquivos
[BUG] Parser falha com linhas vazias no meio do arquivo
```

### Labels (sugestão)

| Label | Cor | Uso |
|---|---|---|
| `core` | azul | Mudanças no Core |
| `cli` | verde | Mudanças na CLI |
| `gui` | roxo | Mudanças na GUI |
| `ci/cd` | cinza | Mudanças no pipeline |
| `bug` | vermelho | Correção de bug |
| `feature` | azul claro | Nova funcionalidade |
| `docs` | amarelo | Documentação |
| `test` | laranja | Testes |
| `priority:high` | vermelho escuro | Alta prioridade |
| `good-first-issue` | verde claro | Bom para começar |

### Template de Issue

```markdown
## Descrição
O que precisa ser feito.

## Contexto
Por que isso é importante? Link com requisito (RF-XX, RNF-XX, RN-XX).

## Critérios de Aceitação
- [ ] Critério 1
- [ ] Critério 2
- [ ] Testes adicionados
- [ ] Documentação atualizada

## Notas técnicas (opcional)
Detalhes de implementação, dependências, etc.
```

---

## 6. Convenções de Milestones

### Formato
```
M1 - Setup
M2 - Core e Testes
M3 - CLI Funcional
M4 - GUI Funcional
M5 - Polimento e Release
```

### Regras
- Cada milestone tem data de entrega
- Issues vinculadas a milestones
- Acompanhar progresso pelo painel do GitHub

---

## 7. Versionamento

Seguimos **Semantic Versioning**: `MAJOR.MINOR.PATCH`

- `MAJOR` — mudanças incompatíveis na API
- `MINOR` — novas funcionalidades retrocompatíveis
- `PATCH` — correções retrocompatíveis

Versão definida em `pyproject.toml`:
```toml
[project]
version = "0.2.0"
```

Tags do Git:
```bash
git tag v0.2.0
git push origin v0.2.0
```

---

## 8. Checklist Antes de Commitar

```bash
# Rodar antes de cada commit:
python -m pdm run ruff check src/ tests/
python -m pdm run ruff format src/ tests/
python -m pdm run pyright
python -m pdm run pytest
```

Ou criar um pre-commit hook (`.git/hooks/pre-commit`):
```bash
#!/bin/bash
set -e
python -m pdm run ruff check src/ tests/
python -m pdm run pyright
python -m pdm run pytest
```

---

## 9. Documentação Inline

### Quando comentar
- ✅ Lógica não-óbvia
- ✅ Decisões de design importantes
- ✅ Workarounds (com link para a issue/bug)
- ✅ Casos extremos

### Quando NÃO comentar
- ❌ O código já é auto-explicativo
- ❌ Comentários que repetem o nome da função
- ❌ Comentários desatualizados

```python
# ❌ Ruim
# Incrementa contador
counter += 1

# ✅ Bom
# Usa janela deslizante de 5min para evitar burst de requisições legítimas
window_seconds = 300
```

---

## 10. Uso de IA (Conforme Enunciado)

### Permitido
- Geração de código com supervisão humana
- Geração de testes com revisão
- Geração de documentação revisada
- Geração de mensagens de commit

### Obrigatório
- **Documentar** o uso de IA no projeto (arquivo `docs/IA_USAGE.md`)
- Indicar quais partes foram geradas por IA
- Revisar TUDO que IA gera antes de commitar
- Cada integrante deve **entender** o código que commita

### Proibido
- Copiar código sem entender
- Usar IA para evitar aprender
- Não citar o uso de IA quando relevante
