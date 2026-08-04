# Papéis da Equipe

> Este documento detalha as responsabilidades, áreas de código e entregáveis específicos de cada integrante da equipe.

## Visão Geral

| Integrante | Papel | Áreas de Responsabilidade |
|---|---|---|
| **Elder** | Engenheiro de CI/CD | Pipeline, qualidade, build, infraestrutura |
| **Aryan** | Engenheiro de Core | Motor de análise, padrões de projeto |
| **Rodrigo** | Engenheiro de CLI | Interface terminal |
| **Helena** | Engenheira de GUI | Interface gráfica |

---

## Elder — Engenheiro de CI/CD

### Áreas de código
```
.github/workflows/        # Pipelines GitHub Actions
.vscode/                  # Configurações compartilhadas do editor
pyproject.toml            # Dependências, configurações de ferramentas
Dockerfile                # (se aplicável)
scripts/                  # Scripts de automação
```

### Responsabilidades
- Configurar e manter o pipeline CI/CD no GitHub Actions
- Garantir que ruff, pyright e pytest rodam no CI
- Configurar SonarCloud para análise contínua
- Configurar proteção de branch (somente PR + review)
- Configurar integração com cobertura de testes
- Gerar executáveis com PyInstaller
- Configurar Dockerfile (opcional)
- Documentar processos de deploy

### Entregáveis específicos
- [ ] Workflow `.github/workflows/ci.yml` funcionando
- [ ] Workflow `.github/workflows/build.yml` para gerar executáveis
- [ ] Workflow `.github/workflows/release.yml` para criar releases
- [ ] Badge de cobertura no README
- [ ] Badge de status do CI no README
- [ ] Documentação no `docs/devops/` sobre como contribuir

### Métricas de sucesso
- Pipeline roda em < 5 minutos
- 0 falsos positivos em validação
- Cobertura de testes monitorada continuamente
- Releases automatizados via tag git

---

## Aryan — Engenheiro de Core

### Áreas de código
```
src/log_sentinel/core/    # Todo o motor do sistema
tests/core/               # Testes do core
```

### Responsabilidades
- Projetar e implementar todas as classes do Core
- Implementar parsers de log (Apache)
- Implementar detectores de anomalia (força bruta, scanner, picos)
- Implementar pipeline de processamento
- Implementar DAOs (LogFileDAO, ReportDAO)
- Implementar factories
- Implementar sistema de eventos para progresso
- Garantir que Core funciona standalone (sem CLI/GUI)
- Aplicar padrões de projeto (Strategy, DAO, Factory)
- Aplicar princípios SOLID

### Entregáveis específicos
- [ ] `core/models.py` com dataclasses
- [ ] `core/parsers/apache.py` com Common e Combined Log Format
- [ ] `core/detectors/brute_force.py`
- [ ] `core/detectors/scanner.py`
- [ ] `core/detectors/traffic_spike.py`
- [ ] `core/dao/log_file.py`
- [ ] `core/dao/report.py` com saída JSON
- [ ] `core/factories.py`
- [ ] `core/pipeline.py`
- [ ] `core/events.py` (Observer)
- [ ] `core/__init__.py` exportando API pública
- [ ] Testes unitários com cobertura ≥ 80% no Core

### Métricas de sucesso
- Core 100% testável sem instalar PySide6 ou Typer
- Adicionar novo formato de log = criar 1 nova classe
- Performance: 1MB/s mínimo de processamento

---

## Rodrigo — Engenheiro de CLI

### Áreas de código
```
src/log_sentinel/cli/     # Toda a CLI
tests/cli/                # Testes da CLI
```

### Responsabilidades
- Implementar todos os subcomandos com Typer
- Implementar renderização de tabelas com Rich
- Implementar barras de progresso com Rich
- Implementar `RichProgressObserver` (adapter do Observer do Core)
- Garantir tratamento de erros amigável
- Garantir mensagens em português
- Implementar validação de argumentos
- Manter paridade com a GUI (RN-03)

### Entregáveis específicos
- [ ] `cli/main.py` — app Typer principal
- [ ] `cli/commands/analyze.py`
- [ ] `cli/commands/batch.py`
- [ ] `cli/commands/detect.py` (com subcomandos)
- [ ] `cli/commands/formats.py`
- [ ] `cli/observers.py` — `RichProgressObserver`
- [ ] `cli/renderers.py` — funções de renderização
- [ ] `cli/exceptions.py`
- [ ] Entry point configurado no `pyproject.toml`
- [ ] Testes com `typer.testing.CliRunner`

### Métricas de sucesso
- Todos os comandos têm `--help` em português
- Exit codes seguem convenção Unix
- Mensagens de erro orientam o usuário
- 100% das funcionalidades do Core acessíveis via CLI

---

## Helena — Engenheira de GUI

### Áreas de código
```
src/log_sentinel/gui/     # Toda a GUI
tests/gui/                # Testes da GUI
```

### Responsabilidades
- Projetar a interface gráfica (mockup → implementação)
- Implementar `MainWindow` e widgets
- Implementar workers (`QThread`) para não travar a UI
- Implementar `QtProgressObserver` (adapter)
- Garantir UX fluida e responsiva
- Implementar drag & drop
- Implementar atalhos de teclado
- Implementar diálogos de erro e exportação
- Manter paridade com a CLI (RN-03)

### Entregáveis específicos
- [ ] `gui/app.py` — setup do QApplication
- [ ] `gui/main_window.py` — janela principal
- [ ] `gui/workers.py` — `AnalysisWorker`, `BatchWorker`
- [ ] `gui/observers.py` — `QtProgressObserver`
- [ ] `gui/widgets/` — todos os widgets componentizados
- [ ] `gui/dialogs/` — diálogos de erro e exportação
- [ ] `gui/resources/styles.qss` — estilo Qt
- [ ] Mockup no Figma ou draw.io
- [ ] Entry point configurado no `pyproject.toml`
- [ ] Testes de smoke com `pytest-qt`

### Métricas de sucesso
- Janela responsiva durante análise de arquivo de 1GB
- Drag & drop funciona com até 20 arquivos
- Filtros aplicáveis sem reprocessar
- 100% das funcionalidades do Core acessíveis via GUI

---

## Colaboração entre Papéis

### Quando há cruzamento de responsabilidades

#### Core ↔ CLI
- **Quem decide o contrato:** Aryan (Core)
- **Quem usa:** Rodrigo (CLI)
- **Conflito?** Discutir em PR. Contrato sempre é definido no Core primeiro, com testes.

#### Core ↔ GUI
- **Quem decide o contrato:** Aryan (Core)
- **Quem usa:** Helena (GUI)
- **Sinais Qt:** Helena cria adapter `QtProgressObserver` que implementa o Protocol do Core.

#### CLI ↔ GUI (paridade)
- **Coordenação:** Rodrigo e Helena revisam paridade a cada feature.
- **Documentação:** atualizar `CLI_DESIGN.md` e `GUI_DESIGN.md` em sincronia.

#### CI/CD ↔ Todos
- **Elder define os padrões** (ruff, pyright, formato de commit).
- **Todos seguem.** Se um padrão prejudica produtividade, abrir Issue para revisar.

---

## Processo de Pull Request

### Fluxo

1. Engenheiro abre branch a partir de `main` atualizada
2. Implementa a feature seguindo TDD
3. Roda testes locais e linters
4. Push e abre PR no GitHub
5. Marca pelo menos 1 colega para review
6. Aguarda CI/CD passar
7. Aplica feedbacks
8. Após aprovação + CI verde → merge (squash recomendado)
9. Branch é deletada automaticamente

### Quem revisa o quê?

| Quem abre PR | Revisor sugerido | Por quê |
|---|---|---|
| Aryan (Core) | Rodrigo ou Helena | Eles consomem a API |
| Rodrigo (CLI) | Aryan | Conhece o Core |
| Helena (GUI) | Aryan | Conhece o Core |
| Elder (CI/CD) | Qualquer | Mudanças afetam todos |

### Code Review — checklist do revisor

- [ ] O código atende aos critérios de aceitação?
- [ ] Os testes cobrem os casos principais?
- [ ] A documentação foi atualizada?
- [ ] Há violação de fronteiras de camada?
- [ ] Performance é razoável?
- [ ] Mensagens de erro são claras?
- [ ] Tipos estão corretos?

---

## Comunicação

### Canais
- **WhatsApp:** decisões rápidas, combinados gerais
- **GitHub Issues:** discussões técnicas, dúvidas sobre implementação
- **GitHub Discussions:** propostas, RFCs
- **Reuniões:** ao menos 1x por semana (definir dia fixo)

### Responsabilidade pela documentação

| Tipo de doc | Quem mantém |
|---|---|
| `CLAUDE.md`, `docs/PROJETO.md` | Elder (mantenedor geral) |
| `docs/architecture/CORE_API.md` | Aryan |
| `docs/architecture/CLI_DESIGN.md` | Rodrigo |
| `docs/architecture/GUI_DESIGN.md` | Helena |
| `docs/testing/*` | Todos contribuem |
| `README.md` | Elder coordena, todos contribuem |
