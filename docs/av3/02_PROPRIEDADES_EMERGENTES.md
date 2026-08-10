# Propriedades Emergentes — Funcionais e Não-Funcionais

> Documento AV3 — Engenharia de Software II (IFBA 2026.1)
> Projeto: **Log Sentinel**
> Base teórica: Pressman & Maxim (Engenharia de Software), Sommerville (capítulos sobre systems-of-systems e qualidade), ISO/IEC 25010.

---

## 1. O que entendemos por "emergente"

Uma **propriedade emergente** é uma característica observável **apenas no sistema como um todo**, que não está presente em nenhum componente isolado e não pode ser deduzida apenas pela soma das partes.

> Exemplo intuitivo: o parser sabe ler **uma linha**; o detector sabe avaliar **uma janela de eventos**; o DAO sabe gravar **um relatório**. Mas a capacidade de **"identificar um ataque de força bruta a partir de um log bruto"** só existe quando os três operam juntos no pipeline. Essa capacidade é emergente.

Dividimos em dois grupos, como pedido na pauta:

- **Emergentes funcionais**: capacidades que o usuário observa como funcionalidade.
- **Emergentes não-funcionais**: qualidades observáveis (desempenho, confiabilidade, usabilidade, etc.).

---

## 2. Propriedades emergentes **funcionais**

| ID | Propriedade emergente | Componentes que precisam interagir | Como se manifesta | Requisitos relacionados |
|----|-----------------------|-------------------------------------|-------------------|--------------------------|
| **PEF-01** | Detecção de força bruta a partir de log bruto | `LogFileDAO` + `ApacheParser` + `BruteForceDetector` + `ReportDAO` | CLI `log-sentinel detect brute-force` retorna lista de IPs com nº de tentativas e janela | RF-01, RF-02 |
| **PEF-02** | Detecção de scanner de vulnerabilidades | DAO + Parser + `ScannerDetector` | Saída lista IPs varrendo URLs sensíveis (/admin, /.env, /wp-login) | RF-02 |
| **PEF-03** | Detecção de pico anormal de tráfego | DAO + Parser + `TrafficSpikeDetector` + agregação por hora | Saída lista janelas de 1 h com volume > N desvios-padrão | RF-01, RF-02 |
| **PEF-04** | Auditoria consolidada de diretório (batch) | DAO + Pipeline + Aggregator + ReportDAO | `log-sentinel batch /var/log/apache/` produz **um único** JSON com métricas somadas e ordenadas cronologicamente | RF-04 |
| **PEF-05** | Paridade CLI ↔ GUI | Core + duas Views | Qualquer análise feita na CLI pode ser reproduzida na GUI e vice-versa com resultado idêntico | RNF-01 |
| **PEF-06** | Relatório auto-contido e reprodutível | ReportDAO + versionamento + hash do log | Um JSON exportado contém: versão do app, hash SHA-256 do log de origem, parâmetros usados → permite reprodução futura | S6, S7 (ver [doc 01](01_BARREIRAS_SALVAGUARDAS.md)) |
| **PEF-07** | Feedback de progresso responsivo | Core emite eventos + CLI (Rich) ou GUI (QProgressBar) consome | Barra de progresso atualizada a cada 1 MB processado, em qualquer interface | RF-05 |
| **PEF-08** | Cadeia de custódia do log | DAO (lê) + Hash (calcula) + ReportDAO (grava) | Operador prova ao auditor que o relatório se refere exatamente ao arquivo daquele momento | S6 |

> Observação: **PEF-01, 02 e 03** não são "três funcionalidades independentes". Compartilham a mesma espinha dorsal (DAO → Parser → Aggregator). A separação evidencia que a arquitetura Pipe-and-Filter permite **plugar** novos detectores como filtros adicionais sem alterar nenhum componente existente — essa **extensibilidade** é em si uma propriedade emergente (PENF-08 abaixo).

---

## 3. Propriedades emergentes **não-funcionais**

Organizadas pelas categorias da ISO/IEC 25010.

### 3.1 Eficiência de performance

| ID | Propriedade | Como emerge | Métrica/limite | Estado |
|----|-------------|-------------|----------------|--------|
| **PENF-01** | Processar 1 GB de log em ≤ 60 s | Generator (DAO) + parser linear + agregação O(n) | tempo no `pytest-benchmark` | ⏳ a validar |
| **PENF-02** | Uso máximo de RAM ≤ 200 MB independente do tamanho do log | DAO streaming + estruturas leves (`Counter`, `defaultdict`) + ausência de cópia integral | `tracemalloc` em teste de carga | ⏳ a validar |

### 3.2 Confiabilidade

| ID | Propriedade | Como emerge | Métrica/limite | Estado |
|----|-------------|-------------|----------------|--------|
| **PENF-03** | Resiliência a log parcialmente corrompido | B2 (parser fail-fast por linha) + B3 (isolamento por arquivo) | continua processando após linha inválida; relatório lista descartes (S4) | ⏳ a implementar |
| **PENF-04** | Determinismo dos relatórios | Pipeline puro + ausência de I/O escondido + ordenação estável | Mesmo input ⇒ mesmo output (hash do JSON é estável) | ⏳ a testar com snapshot tests |

### 3.3 Usabilidade

| ID | Propriedade | Como emerge | Métrica/limite | Estado |
|----|-------------|-------------|----------------|--------|
| **PENF-05** | Tempo até primeiro resultado ≤ 3 cliques na GUI | MainWindow + drag-and-drop + auto-detecção de formato | teste de usabilidade descrito em [CRITERIOS_ACEITACAO.md](../testing/CRITERIOS_ACEITACAO.md) | ⏳ a implementar |
| **PENF-06** | GUI não congela durante processamento | `QThread` worker + signals/slots | teste manual: clique em "Cancelar" responde em < 1 s mesmo com arquivo de 5 GB | ⏳ a implementar |

### 3.4 Manutenibilidade

| ID | Propriedade | Como emerge | Métrica/limite | Estado |
|----|-------------|-------------|----------------|--------|
| **PENF-07** | Substituibilidade do parser (Apache → Nginx) sem alterar CLI/GUI/Detectors | Padrão Strategy + ParserFactory + interface `ILogParser` | adicionar parser Nginx em ≤ 1 PR, sem tocar em pastas `cli/` ou `gui/` | ⏳ planejado pós-MVP |
| **PENF-08** | Pluggabilidade de novos detectores | Pipe-and-Filter + DetectorRegistry | adicionar detector novo = criar uma classe + registrar; zero alteração nos existentes | ⏳ a implementar |
| **PENF-09** | Cobertura de testes ≥ 80% mantida durante refatorações | TDD + CI bloqueando merge | `pytest-cov` no CI | 🔄 em construção |

### 3.5 Segurança (security)

| ID | Propriedade | Como emerge | Métrica/limite | Estado |
|----|-------------|-------------|----------------|--------|
| **PENF-10** | Análise totalmente offline (zero requisições de rede) | Ausência de import de `requests`/`urllib`/sockets no Core + linter customizado | linter falha CI se algum desses módulos for importado em `core/` | ⏳ a adicionar regra |
| **PENF-11** | Integridade do log preservada (read-only) | DAO abre arquivos com `mode='r'` apenas + ausência de `open(..., 'w'/'a')` sobre o log de entrada | inspeção de código + teste que verifica `mtime` antes/depois | ⏳ a testar |

### 3.6 Portabilidade

| ID | Propriedade | Como emerge | Métrica/limite | Estado |
|----|-------------|-------------|----------------|--------|
| **PENF-12** | Executável standalone Linux + Windows | Código Python puro + PyInstaller + matrix do GitHub Actions | artefatos publicados a cada tag | ✅ workflow pronto, falta release oficial |

---

## 4. Como as propriedades emergem (visão de pipeline)

```
ARQUIVO DE LOG
      │
      ▼
[LogFileDAO]                  ← B8: streaming, S6: hash, PENF-02: memória
      │ yield linha
      ▼
[ApacheParser]                ← B2: fail-fast, S4: descarte rastreado
      │ yield LogEntry
      ▼
[Detector(s)]                 ← PEF-01/02/03: capacidades emergem aqui
      │ yield Detection
      ▼
[Aggregator]                  ← PEF-04: consolidação batch
      │
      ▼
[ReportDAO]                   ← B5: sanitização, S7: versão, PEF-06: reprodutibilidade
      │
      ▼
JSON / Tabela / Diálogo GUI   ← PEF-05: paridade CLI/GUI
```

A leitura horizontal mostra **uma única passagem em streaming**. A leitura vertical (✦) é onde cada propriedade emergente "se cria".

---

## 5. Como serão medidas

| Tipo de medição | Ferramenta | Onde está descrita |
|---|---|---|
| Performance e memória | `pytest-benchmark`, `tracemalloc` | [ESTRATEGIA_TESTES.md](../testing/ESTRATEGIA_TESTES.md) |
| Determinismo | testes de snapshot (saída JSON canonicalizada) | a adicionar em `tests/integration/` |
| Paridade CLI↔GUI | teste de paridade que invoca ambos e compara JSON | `tests/integration/test_cli_gui_parity.py` (a criar) |
| Acoplamento (RNF-01) | script `tools/check_imports.py` rodando na CI | a criar |
| Cobertura | `pytest-cov` + SonarCloud | já no CI |

---

## 6. Relação com os outros documentos da AV3

- Os **mecanismos** que tornam essas propriedades possíveis são as Barreiras/Salvaguardas do documento [01](01_BARREIRAS_SALVAGUARDAS.md).
- As **dimensões de confiança** do documento [03](03_DIMENSOES_CONFIANCA.md) são a "qualidade percebida" derivada destas propriedades.
- Quando alguma destas propriedades falha, os efeitos são descritos em [04 — Perigos, Acidentes e Danos](04_PERIGOS_ACIDENTES_DANOS.md).
