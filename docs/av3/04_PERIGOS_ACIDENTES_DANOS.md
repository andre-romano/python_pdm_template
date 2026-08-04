# Perigos, Acidentes e Danos

> Documento AV3 — Engenharia de Software II (IFBA 2026.1)
> Projeto: **Log Sentinel**
> Base teórica: Leveson (2011) *Engineering a Safer World* (STAMP/STPA); IEC 61508; NIST SP 800-30 (risco).

---

## 1. Conceitos adotados

| Termo | Definição operacional |
|---|---|
| **Perigo (hazard)** | Condição do sistema ou do ambiente que, combinada a um gatilho, **pode** levar a um acidente. É potencial, não realizado. |
| **Acidente (mishap)** | Evento não planejado que **realiza** o perigo e produz uma consequência indesejada. |
| **Dano (harm)** | Consequência material, operacional, reputacional ou legal sofrida por um stakeholder. |
| **Severidade** | Magnitude do dano (Catastrófica / Crítica / Marginal / Insignificante — IEC 61508). |
| **Probabilidade** | Chance de o gatilho ocorrer com o perigo presente (Frequente / Provável / Ocasional / Remota / Improvável). |
| **Risco** | Severidade × Probabilidade. |

> O Log Sentinel é uma ferramenta de **análise post-mortem** local. Não controla atuadores, não influencia processos físicos em tempo real. Portanto a maioria dos danos é **operacional, decisório e reputacional**, não físico — o que **não** os torna desprezíveis: uma decisão errada sobre bloquear um IP ou abrir um chamado pode ter efeito real.

---

## 2. Stakeholders e ativos potencialmente danificáveis

| Stakeholder | O que tem a perder |
|---|---|
| Sysadmin / SRE | Tempo, credibilidade no time, decisões erradas tomadas com base em relatório falso |
| Empresa / instituição que opera o servidor | Postura de segurança, evidência num processo, conformidade (LGPD/SOX/PCI) |
| Usuários finais do servidor analisado | Privacidade (IPs e User-Agents podem identificá-los), bloqueios indevidos |
| Equipe do Log Sentinel | Confiabilidade percebida do produto, nota acadêmica |
| Máquina do operador | Disco cheio, memória estourada, CPU saturada |

---

## 3. Matriz de severidade × probabilidade

| | Improvável | Remota | Ocasional | Provável | Frequente |
|---|---|---|---|---|---|
| **Catastrófica** | médio | alto | crítico | crítico | crítico |
| **Crítica** | baixo | médio | alto | crítico | crítico |
| **Marginal** | baixo | baixo | médio | alto | alto |
| **Insignificante** | baixo | baixo | baixo | médio | médio |

---

## 4. Catálogo de perigos, acidentes e danos

> Cada perigo recebe um ID `HZ-xx`. A coluna **Mitigação** referencia barreiras/salvaguardas do [doc 01](01_BARREIRAS_SALVAGUARDAS.md).

### HZ-01 — Falso negativo: ataque real não detectado

| Campo | Conteúdo |
|---|---|
| **Perigo** | Parser ou detector deixa de identificar padrão malicioso real presente no log. |
| **Gatilho** | Regex incompleta, threshold mal calibrado, log com formato sutilmente diferente. |
| **Acidente** | Sysadmin lê relatório "limpo" e **não abre chamado** de incidente real em andamento. |
| **Dano** | Ataque continua, escala para comprometimento de dados; potencial violação de LGPD; reputação. |
| **Severidade** | **Catastrófica** |
| **Probabilidade** | Ocasional |
| **Risco** | **Crítico** |
| **Mitigação** | B2 (parser fail-fast com lista de descartes — operador vê o que ficou de fora), S4 (lista de linhas rejeitadas), testes com logs reais conhecidos, threshold configurável por flag, documentação de limites do detector. |

### HZ-02 — Falso positivo: usuário legítimo acusado

| Campo | Conteúdo |
|---|---|
| **Perigo** | Detector marca como ataque um padrão de tráfego legítimo (crawler de buscador, cliente atrás de NAT corporativo, healthcheck). |
| **Gatilho** | Threshold baixo demais, ausência de allowlist, janela de tempo curta. |
| **Acidente** | Sysadmin **bloqueia IP de cliente real** ou abre chamado contra colega. |
| **Dano** | Indisponibilidade para usuário legítimo, atrito interno, perda comercial. |
| **Severidade** | **Crítica** |
| **Probabilidade** | Provável (se sem allowlist) |
| **Risco** | **Crítico** |
| **Mitigação** | Threshold configurável, suporte a **allowlist** de IPs/User-Agents, exibir contexto da detecção (não só IP), relatório lista linhas que dispararam a regra. |

### HZ-03 — Estouro de memória durante análise

| Campo | Conteúdo |
|---|---|
| **Perigo** | Pipeline carrega arquivo inteiro em RAM (uso de `.read()`/`.readlines()`). |
| **Gatilho** | Log de 5–10 GB, máquina com 4–8 GB de RAM. |
| **Acidente** | Processo morto pelo OOM-killer; análise não conclui. |
| **Dano** | Tempo perdido; em servidor compartilhado, pode derrubar outros processos. |
| **Severidade** | Crítica |
| **Probabilidade** | Provável (sem barreira) |
| **Risco** | **Crítico** |
| **Mitigação** | B8 (geradores/streaming), PENF-02 (limite RAM ≤ 200 MB com teste de carga). |

### HZ-04 — Disco cheio por relatório gigante

| Campo | Conteúdo |
|---|---|
| **Perigo** | Relatório JSON contém todas as entradas, não apenas métricas. |
| **Gatilho** | Operador roda batch num diretório enorme sem `--summary`. |
| **Acidente** | Disco da máquina lota; outros serviços param. |
| **Dano** | Indisponibilidade local; possível corrupção de outros arquivos. |
| **Severidade** | Crítica |
| **Probabilidade** | Ocasional |
| **Risco** | **Alto** |
| **Mitigação** | Padrão = só métricas agregadas; flag `--include-raw` exige opt-in explícito; barra de progresso mostra tamanho do JSON em construção; avisar se > 1 GB. |

### HZ-05 — Sobrescrita silenciosa de relatório anterior

| Campo | Conteúdo |
|---|---|
| **Perigo** | Modo `w` por padrão; sem diálogo de confirmação. |
| **Gatilho** | Cron mensal roda com mesmo `--output`. |
| **Acidente** | Relatório do mês anterior é destruído. |
| **Dano** | Perda de evidência; impossibilidade de comparação histórica. |
| **Severidade** | Crítica |
| **Probabilidade** | Ocasional |
| **Risco** | **Alto** |
| **Mitigação** | S5 (confirmação), default `--no-overwrite`, sufixo automático com timestamp se arquivo existir. |

### HZ-06 — Travamento da GUI durante batch longo

| Campo | Conteúdo |
|---|---|
| **Perigo** | Processamento na thread principal do Qt. |
| **Gatilho** | Operador analisa diretório com 50 arquivos pela GUI. |
| **Acidente** | Janela "Não Responde"; operador mata o app via Gerenciador de Tarefas. |
| **Dano** | Análise perdida; frustração; possível perda de relatório parcial. |
| **Severidade** | Marginal |
| **Probabilidade** | Provável (sem QThread) |
| **Risco** | **Alto** |
| **Mitigação** | B6 (QThread workers), botão Cancelar, salva relatório incremental. |

### HZ-07 — Exposição de dados pessoais no relatório compartilhado

| Campo | Conteúdo |
|---|---|
| **Perigo** | Relatório inclui IPs e User-Agents que podem identificar pessoas (LGPD art. 5º). |
| **Gatilho** | Sysadmin envia o JSON num chat público ou anexa em ticket sem mascarar. |
| **Acidente** | Vazamento de dado pessoal. |
| **Dano** | Multa LGPD, perda de confiança do usuário, sanção interna. |
| **Severidade** | **Crítica** |
| **Probabilidade** | Ocasional |
| **Risco** | **Alto** |
| **Mitigação** | Flag `--anonymize-ips` (truncar último octeto), aviso na CLI ao exportar relatório com IPs intactos, documentação de boas práticas. |

### HZ-08 — Adulteração da evidência (cadeia de custódia quebrada)

| Campo | Conteúdo |
|---|---|
| **Perigo** | Relatório não comprova a qual versão do log se refere. |
| **Gatilho** | Investigação interna ou litígio jurídico; log original é rotacionado/perdido. |
| **Acidente** | Relatório é contestado e descartado como prova. |
| **Dano** | Caso enfraquecido; tempo de análise jogado fora. |
| **Severidade** | Crítica |
| **Probabilidade** | Remota |
| **Risco** | **Médio** |
| **Mitigação** | S6 (hash SHA-256 no relatório), S7 (versão do app), timestamp de execução, parâmetros usados. |

### HZ-09 — Execução de script via relatório malicioso (XSS reflexivo)

| Campo | Conteúdo |
|---|---|
| **Perigo** | JSON exportado contém payload HTML/JS vindo de User-Agent malicioso, e o operador abre o relatório num visualizador web. |
| **Gatilho** | Atacante injetou `<script>` num User-Agent legítimo do servidor. |
| **Acidente** | Visualizador renderiza o script; cookies do operador são exfiltrados. |
| **Dano** | Comprometimento da máquina do operador. |
| **Severidade** | Crítica |
| **Probabilidade** | Remota |
| **Risco** | **Médio** |
| **Mitigação** | B5 (sanitização da saída JSON), documentação reforça abrir o JSON apenas em editores texto. |

### HZ-10 — DoS do próprio Log Sentinel por log envenenado

| Campo | Conteúdo |
|---|---|
| **Perigo** | Atacante deposita arquivo de 100 GB ou linhas com regex catastrófica (ReDoS). |
| **Gatilho** | Operador roda `analyze` no arquivo. |
| **Acidente** | App congela / consome 100% CPU por horas / estoura disco. |
| **Dano** | Indisponibilidade da ferramenta de investigação no momento mais crítico. |
| **Severidade** | Crítica |
| **Probabilidade** | Ocasional |
| **Risco** | **Alto** |
| **Mitigação** | B4 (limite `--max-lines`/`--max-bytes`), regex sem backtracking catastrófico (validar com `re2`/timeout), timeout por linha. |

### HZ-11 — Atualização do parser corrompendo análises antigas

| Campo | Conteúdo |
|---|---|
| **Perigo** | Mudança de regex no parser muda interpretação de linhas. |
| **Gatilho** | Release nova; operador re-roda análise sobre log antigo para comparação. |
| **Acidente** | Métricas diferem para o mesmo log → operador desconfia de tudo. |
| **Dano** | Perda de confiança na ferramenta. |
| **Severidade** | Marginal |
| **Probabilidade** | Ocasional |
| **Risco** | **Médio** |
| **Mitigação** | S7 (versão do Log Sentinel no relatório), changelog explícito de mudanças no parser, snapshot tests, política de versionamento semântico. |

### HZ-12 — Relatório com mensagem de erro vazando dados

| Campo | Conteúdo |
|---|---|
| **Perigo** | Stack trace cru sai no `stderr` com caminho absoluto contendo nome de usuário e estrutura interna do servidor. |
| **Gatilho** | Operador cola log do terminal em chat público para pedir ajuda. |
| **Acidente** | Vazamento involuntário de info da infraestrutura. |
| **Dano** | Engenharia social facilitada; reconhecimento por atacante. |
| **Severidade** | Marginal |
| **Probabilidade** | Provável |
| **Risco** | **Alto** |
| **Mitigação** | S1 (mensagens humanizadas, sem caminho absoluto por padrão), flag `--debug` opt-in para stack trace completo. |

### HZ-13 — Branch de avaliação mesclada sem revisão

| Campo | Conteúdo |
|---|---|
| **Perigo** | Pressão de prazo da AV faz integrantes pular code review. |
| **Gatilho** | Aproximação da data de entrega (15/06/2026). |
| **Acidente** | Bug entra em master e bloqueia a apresentação. |
| **Dano** | Nota acadêmica; tempo do grupo na véspera. |
| **Severidade** | Marginal |
| **Probabilidade** | Provável (sem regra) |
| **Risco** | **Alto** |
| **Mitigação** | Branch protection rule no GitHub exigindo 1 review + CI verde; sprints com folga; demo intermediária 3 dias antes. |

---

## 5. Tabela resumo de risco

| ID | Perigo | Severidade | Probabilidade | **Risco** | Status da mitigação |
|----|--------|-----------|---------------|-----------|---------------------|
| HZ-01 | Falso negativo | Catastrófica | Ocasional | 🔴 Crítico | ⏳ a implementar |
| HZ-02 | Falso positivo | Crítica | Provável | 🔴 Crítico | ⏳ a implementar |
| HZ-03 | OOM | Crítica | Provável | 🔴 Crítico | ⏳ a implementar (B8) |
| HZ-04 | Disco cheio | Crítica | Ocasional | 🟠 Alto | ⏳ a implementar |
| HZ-05 | Sobrescrita silenciosa | Crítica | Ocasional | 🟠 Alto | ⏳ a implementar (S5) |
| HZ-06 | Travamento GUI | Marginal | Provável | 🟠 Alto | ⏳ a implementar (B6) |
| HZ-07 | Exposição LGPD | Crítica | Ocasional | 🟠 Alto | ⏳ a implementar |
| HZ-08 | Cadeia de custódia | Crítica | Remota | 🟡 Médio | ⏳ a implementar (S6/S7) |
| HZ-09 | XSS no relatório | Crítica | Remota | 🟡 Médio | ⏳ a implementar (B5) |
| HZ-10 | DoS por log envenenado | Crítica | Ocasional | 🟠 Alto | ⏳ a implementar (B4) |
| HZ-11 | Regressão de parser | Marginal | Ocasional | 🟡 Médio | ⏳ a implementar (snapshot) |
| HZ-12 | Vazamento por erro | Marginal | Provável | 🟠 Alto | ⏳ a implementar (S1) |
| HZ-13 | PR sem revisão | Marginal | Provável | 🟠 Alto | ✅ branch protection a configurar |

Legenda: 🔴 Crítico · 🟠 Alto · 🟡 Médio · 🟢 Baixo

---

## 6. Priorização (o que atacar primeiro)

Ordem de tratamento sugerida para os próximos 30 dias:

1. **HZ-01 e HZ-02** (falsos negativos/positivos) — coração do produto; testes com logs reais conhecidos.
2. **HZ-03** (OOM) — barreira B8 elimina a categoria inteira.
3. **HZ-10** (DoS por log envenenado) — barreira B4 é uma linha de código.
4. **HZ-06** (travamento GUI) — bloqueia a demo da AV3.
5. **HZ-05 e HZ-12** — baratos e visíveis na demonstração.
6. **HZ-04, HZ-07, HZ-08, HZ-09, HZ-11, HZ-13** — janela AV4/AV5.

---

## 7. Relação com os outros documentos

- Cada **mitigação** mencionada está detalhada como B/S no [doc 01](01_BARREIRAS_SALVAGUARDAS.md).
- As **propriedades emergentes** afetadas estão em [doc 02](02_PROPRIEDADES_EMERGENTES.md).
- **HZ-01, HZ-02, HZ-09, HZ-10** se cruzam com o modelo de ameaças em [doc 05](05_AMEACAS_VULNERABILIDADES.md) — os perigos aqui têm um *adversário* lá.
- **HZ-07 e HZ-08** se conectam à dimensão de **privacy** e **security** do [doc 03](03_DIMENSOES_CONFIANCA.md).
