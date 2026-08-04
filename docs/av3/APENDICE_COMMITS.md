# Apêndice — Commits por integrante (janela 08/04/2026 → 16/06/2026)

> Fonte: `git log --all --no-merges --since=2026-04-01 --until=2026-06-17 --pretty=format:"%ad %an %s" --date=short`
> Corte: 2026-06-16 (entrega original da AV3). Conferido em 2026-06-18.
> Resultado: zero novos commits de código entre 13/05 e 16/06 — a contagem é a mesma da revisão de 2026-06-10.

---

## Elder (`202316360036`) — 9 commits

| Data | Mensagem |
|------|----------|
| 2026-05-12 | fix(ci): corrige lint ruff e move pacote gui para o caminho canonico |
| 2026-05-12 | docs(av2): adiciona especificacao funcional, arquitetura, testes e Gantt |
| 2026-05-11 | ci: desliga regra D104 do ruff para arquivos __init__.py vazios |
| 2026-05-11 | docs: remove secao de dicas orais e fallbacks de 'travar', foca em entendimento |
| 2026-05-11 | docs: adiciona pagina HTML interativa de estudo para AV2 |
| 2026-05-11 | ci: torna SonarCloud opcional quando SONAR_TOKEN nao configurado |
| 2026-05-11 | ci: adiciona workflow de build com PyInstaller para Linux e Windows |
| 2026-05-11 | docs(ci): adiciona badges de CI e cobertura no README |
| 2026-04-28 | Implement test for main function execution |

## Aryan Souza Assis — 9 commits (8 + 1 com config diferente)

| Data | Mensagem |
|------|----------|
| 2026-05-12 | test(core): adiciona teste TDD para LogEntry |
| 2026-05-12 | feat(core): adiciona dataclass LogEntry |
| 2026-04-28 | Update GitHub Actions workflow for pytest and SonarCloud |
| 2026-04-28 | Add conditional execution for SonarCloud Scan |
| 2026-04-28 | Integrate SonarCloud scan into CI workflow |
| 2026-04-28 | Fix sonar.python.version line formatting |
| 2026-04-28 | Add sonar-project.properties configuration file |
| 2026-04-15 | Add as coisas (autoria "Aryan Assis" — config local diferente) |
| 2026-04-08 | Initial commit |

## Rodrigo Cruz — 4 commits

| Data | Mensagem |
|------|----------|
| 2026-05-11 | fix(cli): remove o texto colado por engano no final de main.py |
| 2026-05-11 | feat(cli): adiciona esqueleto Typer com comandos analyze e batch |
| 2026-05-11 | feat(cli): adiciona esqueleto Typer com comandos analyze e batch |
| 2026-05-11 | feat(cli): Cria pacote da CLI |

> Nota: dois commits com a mesma mensagem `feat(cli): adiciona esqueleto Typer...` — provavelmente cherry-pick ou rebase. Consolidar antes da AV5 com `git rebase -i` (interativo, o próprio Rodrigo precisa rodar).

## Helena Santos Freitas — 2 commits

| Data | Mensagem |
|------|----------|
| 2026-05-12 | feat(gui): adiciona esqueleto da MainWindow com PySide6 |
| 2026-05-12 | feat(gui): cria pacote da GUI |

---

## Não conta na contagem da equipe

- **Andre / Andre Luiz Romano Madureira** — autor do template original `andre-romano/python_pdm_template`. Commits dele aparecem por causa do merge do histórico do template.

---

## Comando para regenerar este apêndice

```bash
# Por autor (corte da entrega: 16/06)
git shortlog -sn --all --no-merges --since=2026-04-01 --until=2026-06-17

# Detalhado
git log --all --no-merges --since=2026-04-01 --until=2026-06-17 \
  --pretty=format:"%ad %an %s" --date=short

# Por dia
git log --all --no-merges --since=2026-04-01 \
  --pretty=format:"%ad %an" --date=short | sort | uniq -c
```

## Resultado reproduzido em 2026-06-18 (corte 16/06)

```
$ git shortlog -sn --all --no-merges --since=2026-04-01 --until=2026-06-17
     9  202316360036         (Elder Lopes)
     8  Aryan Souza Assis
     4  Rodrigo Cruz
     2  Helena Santos Freitas
     1  Andre                (template — desconsiderar)
     1  Aryan Assis          (mesma pessoa que Aryan Souza Assis — config local diferente)
```

Total da equipe: **24 commits** (Aryan = 8 + 1 = 9). Consistente com a §3 do [RELATORIO_AV3.md](RELATORIO_AV3.md).
