# Escopo do Projeto

## Filosofia de Escopo

> "Faça pouco e faça bem feito."

O escopo abaixo foi cuidadosamente recortado para garantir entrega completa e funcional dentro do prazo do semestre. Cortes foram feitos com critério — nada foi removido por preguiça, mas sim para preservar qualidade.

---

## ✅ Dentro do Escopo (MVP)

### Análise
- [x] Suporte ao formato de log **Apache** (Common Log Format e Combined Log Format)
- [x] Parsing via expressões regulares
- [x] Cálculo de métricas básicas (top IPs, status codes, endpoints, picos por hora)
- [x] Detecção de **força bruta** (mesmo IP > N requisições em janela de tempo)
- [x] Detecção de **scanner de vulnerabilidades** (IP varrendo URLs sensíveis)
- [x] Detecção de **picos de tráfego** anormais

### Interfaces
- [x] CLI completa com Typer + Rich (subcomandos, flags, output formatado)
- [x] GUI interativa com PySide6 (seleção de arquivos, painel de filtros, tabela de resultados)
- [x] Processamento em lote (múltiplos arquivos ou diretório)
- [x] Barras de progresso (CLI e GUI)

### Saída
- [x] Exibição em tabela formatada no terminal
- [x] Exportação em **JSON**
- [x] Relatório consolidado para batch

### Qualidade
- [x] Cobertura de testes ≥ 80%
- [x] Pipeline CI/CD com lint, type check e testes
- [x] Documentação automática (pdoc)
- [x] Empacotamento standalone (PyInstaller)

---

## ❌ Fora do Escopo (Cortes Intencionais)

### Formatos de log adicionais
- ❌ Nginx (poderá ser adicionado em versões futuras via Strategy)
- ❌ Syslog
- ❌ IIS
- ❌ JSON-formatted logs (CloudWatch, Stackdriver)

**Justificativa:** Foco em uma plataforma garante qualidade. A arquitetura suporta extensão.

### Tempo real
- ❌ Tail em arquivos sendo escritos
- ❌ Streaming de logs em tempo real
- ❌ Alertas push (e-mail, Slack)

**Justificativa:** Foco é análise post-mortem. Tempo real é responsabilidade de Grafana/ELK.

### Persistência
- ❌ Banco de dados (SQLite, PostgreSQL)
- ❌ Histórico de análises
- ❌ Cache de resultados

**Justificativa:** Cada análise é independente e exportável em JSON.

### Multiusuário
- ❌ Sistema de login
- ❌ Permissões e perfis
- ❌ Compartilhamento de relatórios via web

**Justificativa:** Ferramenta local. Compartilhamento via JSON exportado.

### Visualizações avançadas
- ❌ Gráficos interativos (Plotly, D3)
- ❌ Mapas geográficos de IPs
- ❌ Dashboards customizáveis

**Justificativa:** Tabelas e métricas simples atendem a maioria dos casos. Gráficos podem ser uma extensão futura.

### Inteligência avançada
- ❌ Machine Learning para detecção de anomalias
- ❌ Correlação entre múltiplos servidores
- ❌ Geolocalização de IPs

**Justificativa:** Detecções baseadas em regras (heurísticas) são suficientes para o MVP e mais auditáveis.

### Outros
- ❌ Internacionalização (i18n) — apenas português
- ❌ Tema escuro/claro configurável
- ❌ Atalhos de teclado customizáveis
- ❌ Plugins de terceiros

---

## Possíveis Extensões Futuras

Caso o tempo permita ao final do projeto, podem ser adicionados (em ordem de prioridade):

1. **Suporte a Nginx** — fortalece o uso de Strategy e Factory
2. **Exportação em CSV** — simples adição via novo `ReportDAO`
3. **Geolocalização básica de IPs** — usando base offline GeoLite2
4. **Tema escuro na GUI** — usando QSS
5. **Detecção de SQL Injection nos logs** — novo `AnomalyDetector`

---

## Critério de "Pronto para Entregar"

O projeto está pronto para entrega final quando:

- [ ] Todos os RFs implementados e testados
- [ ] Todos os RNFs validados (incluindo teste de carga com 1GB)
- [ ] Todas as RNs garantidas por testes automatizados
- [ ] Cobertura ≥ 80% confirmada pelo CI
- [ ] Documentação gerada e publicada
- [ ] Executável funcionando em Linux e Windows
- [ ] README com guia de uso completo
- [ ] Apresentação final preparada
