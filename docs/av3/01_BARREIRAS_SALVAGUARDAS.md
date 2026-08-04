# Barreiras, Salvaguardas e Condições Latentes

> Documento AV3 — Engenharia de Software II (IFBA 2026.1)
> Projeto: **Log Sentinel** — suíte de auditoria post-mortem de logs Apache.
> Base teórica: modelo "Queijo Suíço" (Reason, 1990) e teoria de defesa em profundidade.

---

## 1. Conceitos adotados

Para fins deste documento usamos as seguintes definições, alinhadas ao referencial da disciplina:

| Termo | Definição operacional no contexto do Log Sentinel |
|---|---|
| **Barreira** | Mecanismo ativo que **impede** que uma falha se propague (ex.: validação de entrada que rejeita um arquivo malformado). |
| **Salvaguarda** | Mecanismo que **mitiga, detecta ou contém** o efeito de uma falha já ocorrida (ex.: logging estruturado que registra exceção para análise posterior). |
| **Condição latente** | Vulnerabilidade dormente, presente desde o desenvolvimento, que só causa dano quando combinada com gatilhos específicos (ex.: regex sem `re.DOTALL` que aceita silenciosamente linhas multi-linha mal formadas). |
| **Defesa em profundidade** | Empilhamento intencional de barreiras heterogêneas para que nenhuma falha única atravesse todas as camadas. |

---

## 2. Mapa de camadas defensivas (visão geral)

```
ENTRADA                      PROCESSAMENTO                  SAÍDA
┌─────────────────┐         ┌────────────────────┐        ┌──────────────────┐
│ B1 Validação    │  ───►  │ B3 Parsing isolado │  ───► │ B5 Sanitização    │
│ de caminho/     │         │ por arquivo        │        │ de relatório      │
│ formato         │         │ (sandbox lógica)   │        │ (escape de saída) │
└──────┬──────────┘         └────────┬───────────┘        └────────┬─────────┘
       │                             │                              │
       ▼                             ▼                              ▼
┌─────────────────┐         ┌────────────────────┐        ┌──────────────────┐
│ S1 Mensagem de  │         │ S3 Geradores       │        │ S5 Confirmação   │
│ erro humanizada │         │ (streaming) p/     │        │ antes de         │
│ (fail-fast)     │         │ evitar OOM         │        │ sobrescrever     │
└─────────────────┘         └────────────────────┘        └──────────────────┘

           ┌─────────────────────────────────────────┐
           │ Camada transversal: CI/CD + testes      │
           │ B0 Lint/type-check  S0 Cobertura ≥ 80%  │
           └─────────────────────────────────────────┘
```

---

## 3. Barreiras (mecanismos preventivos)

| ID | Barreira | Camada | Onde vive no código | Estado |
|----|----------|--------|---------------------|--------|
| **B0** | Lint (`ruff`) + type-check (`pyright`) bloqueando merge | CI/CD | `.github/workflows/ci.yaml`, `pyproject.toml` | ✅ ativa |
| **B1** | Validação de caminho de arquivo antes de abrir (existência, permissão, tamanho > 0) | CLI/GUI | `cli/main.py`, `gui/main_window.py` | ⏳ planejada (CLI ainda em stub) |
| **B2** | Validação de formato Apache (Common/Combined) por regex *fail-fast*: linha que não casa → registrada como `ParseError` e descartada, não para a execução | Core | `core/parsers/apache_parser.py` (a implementar) | ⏳ planejada |
| **B3** | Isolamento por arquivo no modo `batch`: exceção em um arquivo não derruba os outros | Core | `core/pipeline.py` (a implementar) | ⏳ planejada |
| **B4** | Limite explícito de tamanho/linhas processadas via flag `--max-lines` (defesa contra log envenenado de dezenas de GB) | CLI | `cli/main.py` | ⏳ planejada |
| **B5** | Sanitização da saída JSON: escapar `<`, `>`, aspas para evitar XSS quando o relatório for renderizado em browser | Core | `core/dao/report_dao.py` (a implementar) | ⏳ planejada |
| **B6** | GUI roda processamento em `QThread`: barreira contra travamento da thread de UI (RNF-02) | GUI | `gui/workers.py` (a implementar) | ⏳ planejada |
| **B7** | Imports proibidos: pipeline de CI rejeita PR onde `core/` importa `cli/` ou `gui/` (RNF-01) | CI/CD | script de verificação a adicionar | ⏳ planejada |
| **B8** | Geradores (`yield from`) em vez de `.read()` / `.readlines()`: barreira contra estouro de memória (RNF-03) | Core | `core/dao/log_file_dao.py` (a implementar) | ⏳ planejada |

---

## 4. Salvaguardas (mecanismos mitigatórios e de detecção)

| ID | Salvaguarda | Função | Onde vive | Estado |
|----|-------------|--------|-----------|--------|
| **S0** | Cobertura de testes ≥ 80% reportada na CI | Detectar regressões antes do merge | `pytest --cov`, `coverage.xml` | ✅ infra pronta, cobertura ainda parcial |
| **S1** | Mensagens de erro humanizadas com sugestão de correção (em vez de stack trace cru) | Reduzir tempo de diagnóstico do usuário | `cli/`, `gui/` | ⏳ planejada |
| **S2** | Logging interno estruturado (`logging` da stdlib + nível configurável via `--verbose`) | Permitir auditoria do próprio Log Sentinel após incidente | transversal | ⏳ planejada |
| **S3** | Streaming + barra de progresso: dá ao usuário a possibilidade de **abortar** processamento longo | Conter desperdício de tempo/recursos | CLI (Rich), GUI (QProgressBar) | ⏳ planejada |
| **S4** | Lista de linhas rejeitadas no relatório final (com número da linha e motivo) | Auditoria do parsing — operador vê o que foi ignorado | `core/dao/report_dao.py` | ⏳ planejada |
| **S5** | Diálogo de confirmação antes de sobrescrever arquivo de saída | Prevenir perda de relatório anterior | CLI flag `--force`, GUI dialog | ⏳ planejada |
| **S6** | Hash SHA-256 do arquivo de log incluído no relatório | Cadeia de custódia: provar que o log analisado é o mesmo da origem | `core/dao/log_file_dao.py` | ⏳ planejada |
| **S7** | Versão do Log Sentinel embutida no JSON de saída | Rastreabilidade: reprodução futura do relatório | `core/dao/report_dao.py` | ⏳ planejada |
| **S8** | SonarCloud / SAST opcional na CI | Detecção contínua de smells e CVEs em deps | `sonar-project.properties` | ✅ ativo (opcional) |

---

## 5. Condições latentes identificadas

São vulnerabilidades **dormentes** já presentes no projeto ou risco real de surgirem. Cada uma é endereçada por uma barreira ou salvaguarda acima.

| ID | Condição latente | Origem | Gatilho que ativa o dano | Mitigada por |
|----|------------------|--------|--------------------------|--------------|
| **CL-01** | Regex de parsing Apache pode aceitar silenciosamente linhas multi-linha mal formadas, gerando `LogEntry` com campos vazios | Decisão de design do parser | Log corrompido por crash do Apache no meio de uma linha | B2 + S4 |
| **CL-02** | Falta de limite de tamanho permitiria DoS por log envenenado (ex.: 1 TB) | Ausência de flag `--max-lines` | Atacante deposita arquivo gigante na pasta auditada | B4 + S3 |
| **CL-03** | `.read()` em arquivo grande causaria `MemoryError` em máquinas de 4 GB de RAM | Hábito comum de Python | Operador analisa log de 10 GB localmente | B8 |
| **CL-04** | GUI sem `QThread` congelaria janela durante batch, fazendo o usuário matar o processo e perder progresso | Esqueleto inicial do PySide6 | Operador analisa diretório com 50 arquivos | B6 + S3 |
| **CL-05** | JSON com aspas/HTML não escapados poderia executar script se relatório for aberto num visualizador web | Confiança implícita no log de entrada | Atacante coloca payload no `User-Agent` de uma requisição | B5 |
| **CL-06** | Acoplamento entre `core/` e `gui/` (já corrigido na branch `fix/ci-ruff-and-gui-path`) | Estrutura de pacotes herdada do template | PR futuro reintroduzindo import circular | B7 |
| **CL-07** | Testes podem ficar verdes ao mockar leitura de disco, escondendo bug de I/O real | Hábito de unit test puro | Refatoração futura | S0 + testes de integração com arquivos reais |
| **CL-08** | Mensagem de erro com caminho absoluto pode vazar nome de usuário em screenshots | Default do Python tracebacks | Operador compartilha screenshot em chat público | S1 |
| **CL-09** | Sobrescrita silenciosa de relatório anterior em loop de cron | Default de modo `w` | Job mensal pisa relatório anterior | S5 |
| **CL-10** | Branch de avaliação (AV) mesclada sem revisão suficiente por causa do prazo apertado | Pressão de calendário | Prazo de AV3 em 17/06 | Code review obrigatório no GitHub + S0 |

---

## 6. Matriz Barreira × Condição Latente

Leitura: cada condição latente é coberta por **pelo menos duas** defesas (defesa em profundidade).

| | B0 | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | S0 | S1 | S3 | S4 | S5 | S6 | S7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-01 | | | ✅ | | | | | | | ✅ | | | ✅ | | | |
| CL-02 | | ✅ | | | ✅ | | | | | | | ✅ | | | | |
| CL-03 | | | | | ✅ | | | | ✅ | ✅ | | | | | | |
| CL-04 | | | | | | | ✅ | | | | | ✅ | | | | |
| CL-05 | | | | | | ✅ | | | | ✅ | | | | | | |
| CL-06 | ✅ | | | | | | | ✅ | | ✅ | | | | | | |
| CL-07 | | | | | | | | | | ✅ | | | | | ✅ | |
| CL-08 | | | | | | | | | | | ✅ | | | | | |
| CL-09 | | | | | | | | | | | ✅ | | | ✅ | | ✅ |
| CL-10 | ✅ | | | | | | | | | ✅ | | | | | | |

---

## 7. Acompanhamento

- Barreiras marcadas como ⏳ viram **issues no GitHub** rotulados `barrier:Bxx`.
- Salvaguardas ⏳ viram issues `safeguard:Sxx`.
- Cada PR que implementa uma deve referenciar o ID neste documento na descrição.
- Revisão deste documento ocorre em todo fechamento de milestone (AV2 ✅ AV3 ⏳ AV4 AV5).

## 8. Referências

- Reason, J. (1990). *Human Error*. Cambridge University Press. (Modelo Swiss Cheese.)
- Leveson, N. (2011). *Engineering a Safer World*. MIT Press. (STAMP, condições latentes.)
- OWASP Top 10 — categorias A03 (Injection) e A05 (Security Misconfiguration) embasam B5 e CL-05.
- Documento interno: [`docs/REQUISITOS.md`](../REQUISITOS.md) — RF/RNF de origem das barreiras.
- Documento interno: [`docs/architecture/ARQUITETURA.md`](../architecture/ARQUITETURA.md) — onde cada barreira é instalada.
