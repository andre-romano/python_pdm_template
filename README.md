# Log Sentinel

[![CI](https://github.com/202316360036/log-sentinel/actions/workflows/ci.yaml/badge.svg)](https://github.com/202316360036/log-sentinel/actions/workflows/ci.yaml)
[![Tests](https://github.com/202316360036/log-sentinel/actions/workflows/test.yaml/badge.svg)](https://github.com/202316360036/log-sentinel/actions/workflows/test.yaml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)](https://github.com/202316360036/log-sentinel)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Suíte de auditoria e análise post-mortem de logs Apache. Detecta padrões de ataque (força bruta, scanner de vulnerabilidades, picos de tráfego) e gera relatórios consolidados via CLI e GUI.

Projeto desenvolvido na disciplina **Engenharia de Software II** — IFBA 2026.1.

Repositório baseado no template [andre-romano/python_pdm_template](https://github.com/andre-romano/python_pdm_template).

## Como usar este template

1. **Copiar o template**:
   - No GitHub, clique no botão ``Use this template`` (ou ``Usar este template``) na página do repositório.
   - Siga as instruções para criar um novo repositório baseado neste template.

2. **Clonar o repositório**:
   - Clone o novo repositório para sua máquina local:
     ```bash
     git clone https://github.com/seu-usuario/seu-repositorio.git
     cd seu-repositorio
     ```

## Configuração do ambiente

1. **Instalar o PDM**:
   - Certifique-se de que o PDM está instalado. Caso não esteja, instale-o com o seguinte comando:
     ```bash
     python -m pip install pdm
     ```

2. **Instalar dependências**:
   - Execute o comando abaixo para instalar as dependências do projeto:
     ```bash
     python -m pdm install
     ```

3. **Adicionar novas dependências**:
   - Para adicionar uma nova dependência ao projeto, use o comando:
     ```bash
     python -m pdm add nome-da-dependencia
     ```
   - Para adicionar dependências de desenvolvimento (instaladas apenas no ambiente de desenvolvimento - nunca em produção), utilize:
     ```bash
     python -m pdm add -d nome-da-dependencia
     ```

## Executar o projeto

1. **Rodar o projeto**:
   - Após instalar as dependências, você pode executar o projeto diretamente usando:
     ```bash
     python -m pdm run python src/python_pdm_template/__main__.py
     ```

O PDM nao apenas controla dependencias e executa o projeto, ele também pode compilar o projeto Python em arquivos `.WHL` e publicá-los no repositório oficial de pacotes do Python ([PyPi](https://pypi.org/)).

Para mais informações sobre as essas e outras funcionalidades disponíveis no PDM, consulte a [documentação oficial](https://pdm.fming.dev/).

## Estrutura do projeto

- [**``.github/workflows/``**](.github/workflows): Configurações do GitHub Workflows para automacao de CI/CD (Integração Contínua e Entrega Contínua).
- [**``.vscode/``**](.vscode): Configurações do Visual Studio Code.
- [**``src/``**](src/python_pdm_template/): Contém o código-fonte do projeto.
- [**``tests/``**](tests): Contém os testes do projeto.
- [**``pyproject.toml``**](pyproject.md): Arquivo de configuração do projeto, incluindo dependências e metadados.

Cada pasta ou arquivo acima tem um ``README.md`` explicando sua finalidade, como funciona, e como usar cada uma delas. **Clique nos links acima e leia com atenção cada um dos READMEs para entender melhor o projeto.**
- Em cada um dos links acima **há tarefas para você realizar**, para praticar o que foi explicado no README. 
- As tarefas poderão ser **utilizadas para fins de avaliação na disciplina.** Assim, realize todas as tarefas propostas e envie suas respostas no nosso Google Classroom.
