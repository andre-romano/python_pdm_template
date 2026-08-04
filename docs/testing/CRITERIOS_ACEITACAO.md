# Critérios de Aceitação

> Define quando uma feature está "pronta". Cada feature do projeto deve atender TODOS os critérios da sua categoria antes de ser considerada concluída.

## Critérios Universais (toda feature deve atender)

### Código
- [ ] Implementação segue os padrões definidos em `docs/team/CONVENCOES.md`
- [ ] Toda função/método/atributo tipado (type hints)
- [ ] Toda função pública tem docstring (PEP 257)
- [ ] Sem `print()` (usar `logging` ou Rich)
- [ ] Sem TODO/FIXME sem Issue associada

### Testes
- [ ] Testes escritos antes da implementação (TDD)
- [ ] Cobertura local da feature ≥ 80%
- [ ] Testes de "caminho feliz" presentes
- [ ] Testes de defeitos (edge cases) presentes
- [ ] Todos os testes passam localmente
- [ ] Pipeline CI/CD verde

### Qualidade Estática
- [ ] `ruff check` sem violações
- [ ] `pyright` sem erros
- [ ] Sem warnings novos no SonarCloud

### Versionamento
- [ ] Branch criada a partir de `main` atualizada
- [ ] Commits seguem Conventional Commits
- [ ] Pull Request aberto com descrição clara
- [ ] PR aprovado por pelo menos 1 colega
- [ ] Pipeline verde no PR

---

## Critérios por Funcionalidade

### CA-RF01 — Parsing e Extração de Métricas

| # | Critério | Como validar |
|---|---|---|
| 1 | Parseia corretamente Apache Common Log Format | Teste com fixture conhecida |
| 2 | Parseia corretamente Apache Combined Log Format | Teste com fixture conhecida |
| 3 | Retorna `None` para linhas mal-formadas | Teste unitário |
| 4 | Calcula total de requisições corretamente | Teste com fixture de N linhas |
| 5 | Conta requests por IP corretamente | Teste com 3 IPs distintos |
| 6 | Calcula distribuição de status codes | Teste com mix de 2xx, 4xx, 5xx |
| 7 | Identifica top N endpoints | Teste com endpoints repetidos |
| 8 | Calcula picos por hora | Teste com timestamps em horas distintas |
| 9 | Processa 1000 linhas em < 5 segundos | Benchmark |

### CA-RF02 — Interface CLI

| # | Critério | Como validar |
|---|---|---|
| 1 | `log-sentinel --help` exibe todos os comandos | Teste com `CliRunner` |
| 2 | `log-sentinel analyze --help` exibe ajuda específica | Teste com `CliRunner` |
| 3 | Comando aceita arquivo via argumento posicional | Teste de invocação |
| 4 | Flag `--status-code` filtra resultados | Teste comparando outputs |
| 5 | Flag `--ip` filtra por IP | Teste comparando outputs |
| 6 | Flag `--date-range` filtra por período | Teste comparando outputs |
| 7 | Flag `--output` salva em arquivo | Teste verifica arquivo criado |
| 8 | Flag `--format json` produz JSON válido | Teste fazendo `json.loads` |
| 9 | Exit code != 0 em caso de erro | Teste com arquivo inválido |
| 10 | Mensagens de erro são claras e em português | Inspeção manual + teste |

### CA-RF03 — Interface GUI

| # | Critério | Como validar |
|---|---|---|
| 1 | Janela abre sem erros | Teste de smoke |
| 2 | Botão "Selecionar arquivo" abre file picker | Teste manual |
| 3 | Drag & drop de arquivo funciona | Teste manual |
| 4 | Painel de filtros aplica mudanças | Teste de signal |
| 5 | Tabela exibe resultados após análise | Teste manual |
| 6 | Janela não trava durante processamento | Teste com arquivo grande |
| 7 | Barra de progresso atualiza | Teste manual |
| 8 | Botão "Exportar JSON" salva arquivo | Teste manual |
| 9 | Diálogos de erro são exibidos quando esperado | Teste manual |

### CA-RF04 — Processamento em Lote

| # | Critério | Como validar |
|---|---|---|
| 1 | Aceita lista de arquivos como input | Teste CLI |
| 2 | Aceita diretório como input | Teste CLI |
| 3 | Flag `--recursive` busca em subdiretórios | Teste com estrutura de pastas |
| 4 | Flag `--pattern` filtra por padrão glob | Teste com `*.log` e `access*.log` |
| 5 | Métricas são consolidadas corretamente | Teste com 3 arquivos conhecidos |
| 6 | Indica progresso de cada arquivo | Teste de signals/eventos |
| 7 | Erro em 1 arquivo não interrompe os outros | Teste com 1 arquivo corrompido |

### CA-RF05 — Feedback de Execução

| # | Critério | Como validar |
|---|---|---|
| 1 | `on_file_start` é chamado ao iniciar arquivo | Teste com mock observer |
| 2 | `on_progress` é chamado periodicamente | Teste com mock + arquivo de 10MB |
| 3 | `on_file_complete` é chamado ao fim | Teste com mock observer |
| 4 | `on_error` é chamado em caso de erro | Teste com arquivo inválido |
| 5 | CLI exibe barra Rich durante processamento | Teste manual |
| 6 | GUI exibe QProgressBar durante processamento | Teste manual |

---

## Critérios por Requisito Não-Funcional

### CA-RNF01 — Desacoplamento Arquitetural

| # | Critério | Como validar |
|---|---|---|
| 1 | `core/` não importa nada de `cli/` ou `gui/` | Script de validação no CI |
| 2 | `cli/` não contém regex de log | Inspeção manual + grep |
| 3 | `gui/` não contém regex de log | Inspeção manual + grep |
| 4 | Core funciona standalone (sem PySide6/Typer) | Teste de import isolado |

### CA-RNF02 — Responsividade GUI

| # | Critério | Como validar |
|---|---|---|
| 1 | Toda operação pesada usa QThread | Inspeção de código |
| 2 | Janela responde a cliques durante análise | Teste manual com arquivo grande |
| 3 | Cancelamento funciona | Teste manual |

### CA-RNF03 — Memória Eficiente

| # | Critério | Como validar |
|---|---|---|
| 1 | Leitura usa generators | Inspeção de código (grep `yield`) |
| 2 | Sem `.read()` ou `.readlines()` em arquivos completos | Inspeção de código |
| 3 | Uso de RAM ≤ 200MB para arquivo de 1GB | Teste de carga com `memory_profiler` |

### CA-RNF04 — Portabilidade

| # | Critério | Como validar |
|---|---|---|
| 1 | `pdm build` produz wheel funcional | Teste de instalação |
| 2 | PyInstaller produz executável Linux | CI/CD |
| 3 | PyInstaller produz executável Windows | CI/CD (matrix) |
| 4 | Dockerfile constrói imagem funcional | CI/CD |

### CA-RNF05 — Extensibilidade

| # | Critério | Como validar |
|---|---|---|
| 1 | Adicionar novo parser não requer mudança no Core | Demonstração de exemplo |
| 2 | Adicionar novo detector não requer mudança no Core | Demonstração de exemplo |
| 3 | CLI e GUI funcionam com novo parser sem mudança | Teste de integração |

### CA-RNF06 — Documentação e Testes

| # | Critério | Como validar |
|---|---|---|
| 1 | Cobertura ≥ 80% | Relatório do `pytest-cov` |
| 2 | Documentação `pdoc` gera sem erros | Comando `pdoc src/` |
| 3 | README contém: instalação, uso CLI, uso GUI, exemplos | Inspeção manual |
| 4 | Toda função pública tem docstring | Validado pelo `ruff` (regra D) |

---

## Critérios por Regra de Negócio

### CA-RN01 — Somente Leitura

| # | Critério | Como validar |
|---|---|---|
| 1 | Arquivo de log não muda após análise | Teste comparando hash MD5 antes/depois |
| 2 | DAO rejeita modos diferentes de "r" | Teste unitário |
| 3 | Auditoria: nenhum `open(...)` com modo de escrita em arquivos de input | Inspeção via `grep` |

### CA-RN02 — Validação Fail-Fast

| # | Critério | Como validar |
|---|---|---|
| 1 | Validação ocorre antes de processar arquivo inteiro | Teste com mock + verificação de chamadas |
| 2 | Arquivo binário é rejeitado em < 1 segundo | Benchmark |
| 3 | Mensagem de erro indica o problema | Teste de mensagem |
| 4 | Arquivo válido passa pela validação | Teste positivo |

### CA-RN03 — Paridade CLI = GUI

| # | Critério | Como validar |
|---|---|---|
| 1 | Toda flag CLI tem widget GUI equivalente | Checklist de paridade revisado a cada PR |
| 2 | Mesmos filtros produzem mesmos resultados em ambas | Teste de integração `test_cli_gui_parity.py` |
| 3 | Exportação produz arquivos idênticos | Teste comparando hashes |

---

## Definition of Done (DoD) — Geral

Uma feature está "Done" quando:

✅ Implementação completa
✅ Todos os critérios de aceitação atendidos
✅ Cobertura de testes ≥ 80%
✅ Pipeline CI/CD verde
✅ Code review aprovado
✅ Documentação atualizada (se aplicável)
✅ Issue do GitHub fechada
✅ Branch removida após merge

---

## Definition of Done (DoD) — Release

O projeto está pronto para release quando:

✅ Todos os RFs implementados
✅ Todos os RNFs validados
✅ Todos os RNs garantidos por testes
✅ Cobertura geral ≥ 80%
✅ Documentação `pdoc` publicada
✅ Executáveis Linux + Windows gerados
✅ README finalizado com guia completo
✅ Demo gravada (vídeo ou GIFs)
✅ Apresentação preparada
