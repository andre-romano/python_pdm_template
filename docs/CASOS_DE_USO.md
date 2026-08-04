# Casos de Uso

## Visão Geral

Este documento descreve os principais cenários de uso do Log Sentinel. Cada caso de uso serve como base para os critérios de aceitação e testes de integração.

---

## CU-01 — Investigação de Tentativa de Ataque

### Ator
Administrador de servidor

### Pré-condição
- O sistema está instalado.
- Existe um arquivo `access.log` do Apache disponível.

### Fluxo Principal (GUI)
1. O ator abre o Log Sentinel pela GUI.
2. Clica em "Selecionar arquivo" e escolhe o `access.log`.
3. O sistema valida o formato e exibe "Arquivo válido".
4. O ator marca a opção "Detectar força bruta" no painel de filtros.
5. Clica em "Analisar".
6. O sistema exibe barra de progresso enquanto processa.
7. Ao concluir, mostra na tabela os IPs suspeitos com:
   - IP de origem
   - Número de tentativas
   - Janela de tempo
   - Nível de risco (baixo/médio/alto)
8. O ator clica em "Exportar JSON" e salva o relatório.

### Fluxo Alternativo (CLI)
```bash
log-sentinel detect brute-force /var/log/apache/access.log \
  --threshold 100 \
  --window 5m \
  --output suspeitos.json
```

### Critério de Sucesso
- Relatório identifica corretamente IPs com mais de 100 requisições em 5 minutos.
- Arquivo de log original permanece intacto (validável por hash).

---

## CU-02 — Auditoria Mensal Automatizada

### Ator
Analista de infraestrutura

### Pré-condição
- O sistema está instalado em um servidor.
- O cron está configurado.
- Existe um diretório com logs mensais.

### Fluxo Principal
1. Cron executa mensalmente o comando:
```bash
log-sentinel batch /var/log/apache/2026/04/ \
  --output /reports/abril-2026.json \
  --format json
```
2. O sistema processa todos os arquivos do diretório.
3. Gera um relatório consolidado em JSON.
4. Outro script consome o JSON e envia por e-mail.

### Critério de Sucesso
- Comando roda sem interação humana.
- Saída em JSON é válida e parseável.
- Relatório contém soma correta das métricas de todos os arquivos.

---

## CU-03 — Análise Visual Rápida

### Ator
Estagiário aprendendo análise de logs

### Pré-condição
- Sistema instalado.
- Tem alguns arquivos de log de exemplo.

### Fluxo Principal
1. Abre a GUI.
2. Arrasta múltiplos arquivos `.log` para a janela.
3. O sistema carrega todos e mostra informação consolidada.
4. Visualiza na tabela:
   - Top 10 IPs com mais requisições
   - Distribuição de status codes em gráfico de barras simples
5. Clica em uma linha do IP para ver detalhes daquele IP.
6. Aplica filtro "Apenas erros 4xx/5xx" no painel lateral.
7. A tabela é atualizada instantaneamente.

### Critério de Sucesso
- Drag & drop funciona com até 20 arquivos.
- Filtros são aplicados sem reprocessar o arquivo.

---

## CU-04 — Detecção de Scanner de Vulnerabilidade

### Ator
Analista de segurança

### Pré-condição
- Existe um log com tentativas de acesso a URLs sensíveis.

### Fluxo Principal (CLI)
```bash
log-sentinel detect scanner access.log \
  --suspicious-paths /admin,/wp-login,/.env,/phpmyadmin \
  --min-distinct-paths 5
```

### Comportamento
- O sistema identifica IPs que tentaram acessar 5 ou mais URLs sensíveis distintas.
- Exibe na tabela: IP, lista de URLs tentadas, total de tentativas.

### Critério de Sucesso
- Detecta corretamente IPs varrendo URLs.
- Permite customizar a lista de paths suspeitos.

---

## CU-05 — Filtro por Período e Status

### Ator
Administrador investigando incidente específico

### Pré-condição
- Sabe a data/hora aproximada do incidente.

### Fluxo Principal (CLI)
```bash
log-sentinel analyze access.log \
  --date-range "2026-04-15 14:00" "2026-04-15 16:00" \
  --status-code 500 \
  --format table
```

### Comportamento
- Filtra apenas linhas no período indicado.
- Filtra apenas erros 500.
- Mostra tabela com endpoints e IPs afetados.

### Critério de Sucesso
- Filtros combinados funcionam corretamente.
- Resultado idêntico ao filtro equivalente na GUI (RN-03).

---

## CU-06 — Validação de Arquivo Inválido (Fail-Fast)

### Ator
Qualquer usuário

### Pré-condição
- Usuário seleciona um arquivo que NÃO é log Apache (ex: PDF, imagem, texto aleatório).

### Fluxo Principal
1. Usuário seleciona o arquivo via GUI ou CLI.
2. O sistema lê as primeiras 5 linhas.
3. Detecta que o conteúdo não casa com o formato Apache.
4. Aborta a operação imediatamente.
5. Exibe mensagem clara:
   - GUI: caixa de diálogo de erro
   - CLI: mensagem em vermelho com `exit code != 0`

### Mensagem esperada
```
ERRO: O arquivo 'documento.pdf' não corresponde ao formato Apache esperado.
Verifique se selecionou o arquivo correto.
```

### Critério de Sucesso
- Operação aborta em menos de 1 segundo.
- Nenhum byte do arquivo é alterado.
- Mensagem é específica e acionável.

---

## CU-07 — Processamento de Arquivo Gigante

### Ator
Administrador com arquivo de log de 5GB

### Pré-condição
- Máquina com apenas 4GB de RAM.

### Fluxo Principal
1. Usuário seleciona arquivo de 5GB.
2. Sistema valida formato (lê apenas primeiras linhas).
3. Inicia processamento, exibindo progresso.
4. Uso de RAM permanece estável (≤ 200MB).
5. Conclui o processamento sem swap excessivo.

### Critério de Sucesso
- Processamento conclui sem `MemoryError`.
- Barra de progresso atualiza pelo menos a cada 1MB.
- GUI permanece responsiva (RNF-02).

---

## Resumo dos Casos de Uso

| ID | Nome | Ator | Interface |
|---|---|---|---|
| CU-01 | Investigação de ataque | Administrador | GUI + CLI |
| CU-02 | Auditoria automatizada | Analista | CLI |
| CU-03 | Análise visual rápida | Estagiário | GUI |
| CU-04 | Detecção de scanner | Analista de segurança | CLI |
| CU-05 | Filtro por período/status | Administrador | CLI + GUI |
| CU-06 | Validação Fail-Fast | Todos | CLI + GUI |
| CU-07 | Arquivo gigante | Administrador | CLI + GUI |
