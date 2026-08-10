# Requisitos do Sistema

## Requisitos Funcionais (RF)

### RF-01 — Parsing e Extração de Métricas
O sistema deve ler arquivos de log do Apache, extrair dados estruturados usando expressões regulares e contabilizar métricas.

**Métricas obrigatórias:**
- Número total de requisições
- Número de requisições por IP (top N IPs)
- Frequência de códigos de status HTTP (2xx, 3xx, 4xx, 5xx)
- Endpoints mais acessados (top N)
- Distribuição de tráfego por hora
- Total de bytes transferidos

**Critério de aceitação:**
- Dado um arquivo `access.log` com 1000 linhas, o sistema deve produzir um relatório com todas as métricas acima em menos de 5 segundos.

---

### RF-02 — Interface de Linha de Comando (CLI)
O sistema deve fornecer uma CLI rica baseada em Typer, com subcomandos.

**Comandos obrigatórios:**
```bash
log-sentinel analyze <arquivo>           # Analisa um único arquivo
log-sentinel batch <diretório>           # Analisa múltiplos arquivos
log-sentinel detect brute-force <arq>    # Detecta força bruta
log-sentinel detect scanner <arquivo>    # Detecta scanner
log-sentinel --help                      # Ajuda geral
```

**Flags obrigatórias:**
- `--status-code <int>` — filtrar por código HTTP
- `--ip <str>` — filtrar por IP específico
- `--date-range <start> <end>` — filtrar por período
- `--output <arquivo>` — exportar para arquivo (JSON)
- `--format <table|json>` — formato de saída
- `--verbose` — modo detalhado

**Critério de aceitação:**
- O comando `log-sentinel --help` deve listar todos os subcomandos.
- Cada subcomando deve ter sua própria ajuda contextual.

---

### RF-03 — Interface Gráfica (GUI)
O sistema deve fornecer uma GUI baseada em PySide6 com paridade total à CLI.

**Telas obrigatórias:**
- Tela principal com seletor de arquivos (drag & drop suportado)
- Painel de filtros lateral
- Tabela de resultados com ordenação
- Barra de progresso durante o processamento
- Diálogo de exportação de relatório

**Critério de aceitação:**
- Selecionar arquivo, aplicar filtro, ver resultado em menos de 3 cliques.
- A janela não pode congelar durante processamento de arquivos grandes.

---

### RF-04 — Processamento em Lote (Batch)
Ambas as interfaces devem permitir analisar múltiplos arquivos ou um diretório inteiro, agregando resultados em um relatório consolidado.

**Comportamento:**
- Aceitar lista de arquivos ou caminho de diretório.
- Processar recursivamente (com flag `--recursive`).
- Agregar métricas mantendo ordenação cronológica.
- Indicar progresso de cada arquivo processado.

**Critério de aceitação:**
- Dado um diretório com 10 arquivos, o relatório consolidado deve conter a soma correta de todas as métricas.

---

### RF-05 — Feedback de Execução e Relatórios
O Core deve emitir eventos de progresso para alimentar barras de progresso na CLI (Rich) e na GUI (QProgressBar).

**Eventos obrigatórios:**
- `on_file_start(path, total_bytes)` — início do processamento de um arquivo
- `on_progress(bytes_processed, total_bytes)` — progresso incremental
- `on_file_complete(path, entries_parsed)` — fim do processamento
- `on_error(path, error)` — erro durante processamento

**Critério de aceitação:**
- Em arquivos > 100MB, eventos de progresso devem ser emitidos pelo menos a cada 1MB processado.

---

## Requisitos Não Funcionais (RNF)

### RNF-01 — Desacoplamento Arquitetural
- O Core não pode importar nada de `cli/` ou `gui/`.
- A CLI e a GUI não podem conter regex, lógica matemática ou regra de negócio.
- Validação automática: o pipeline CI/CD verifica imports proibidos.

---

### RNF-02 — Responsividade da GUI (Concorrência)
- Toda operação de I/O ou processamento deve rodar em `QThread`.
- A thread principal só atualiza widgets via signals/slots.
- A janela deve responder a cliques mesmo durante processamento de 5GB.

---

### RNF-03 — Gerenciamento de Memória Eficiente
- Arquivos devem ser lidos via generator (`yield from`).
- Nunca usar `.read()` ou `.readlines()` em arquivos completos.
- Uso máximo de RAM ≤ 200MB independente do tamanho do arquivo.

**Validação:** teste de carga com arquivo de 1GB deve rodar em máquina com 4GB de RAM.

---

### RNF-04 — Portabilidade e Distribuição
- Empacotamento via PyInstaller para Linux e Windows.
- Container Docker opcional para servidores headless.
- Instalação via `pip install` em ambientes Python 3.12+.

---

### RNF-05 — Extensibilidade via Padrões de Projeto
- Novos formatos de log devem ser adicionados criando uma nova classe `LogParserStrategy` sem alterar Core, CLI ou GUI.
- Novos detectores devem ser adicionados criando uma nova classe `AnomalyDetector`.
- Aplicação dos princípios SOLID, especialmente Open/Closed.

---

### RNF-06 — Documentação e Testes
- Cobertura mínima de testes: **80%**.
- Toda função pública com docstring no padrão PEP 257.
- Documentação automática gerada via `pdoc`.
- README com guia de instalação, uso e exemplos.

---

## Regras de Negócio (RN)

### RN-01 — Segurança e Imutabilidade (Somente Leitura)
> O sistema deve abrir os arquivos de log estritamente em modo de leitura. Sob nenhuma circunstância tem permissão para alterar, limpar ou sobrescrever os arquivos originais.

**Implementação:**
- Sempre `open(path, "r", ...)`.
- Validação no DAO: rejeitar qualquer modo que não seja `"r"` ou `"rb"`.
- Teste automatizado garantindo que o arquivo não muda após análise (comparação de hash).

---

### RN-02 — Validação de Formato (Fail-Fast)
> O sistema deve inspecionar as primeiras linhas do arquivo selecionado para garantir que ele corresponde ao formato esperado, abortando a operação com mensagem clara caso seja inválido ou binário.

**Implementação:**
- Ler as primeiras 5 linhas.
- Aplicar regex de validação do formato selecionado.
- Se < 50% das linhas casarem, lançar `InvalidLogFormatError` com mensagem clara.
- Detectar conteúdo binário (presença de bytes nulos) e lançar erro específico.

---

### RN-03 — Paridade de Recursos (CLI = GUI)
> Toda capacidade de filtragem ou exportação existente em uma interface deve existir na outra.

**Implementação:**
- Manter um arquivo `docs/architecture/CLI_DESIGN.md` e `GUI_DESIGN.md` espelhados.
- Checklist de paridade revisado a cada release.
- Testes de integração que validam que ambas interfaces produzem o mesmo resultado dado o mesmo input.
