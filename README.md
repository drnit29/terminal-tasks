# Terminal Tasks App

## Descrição

O **Terminal Tasks App** é um gerenciador de tarefas moderno baseado em terminal, construído com a biblioteca [Textual](https://textual.textualize.io/). Ele permite que você adicione, gerencie e acompanhe suas tarefas diretamente do seu terminal.

## Recursos

*   **Adicionar Tarefas:** Crie novas tarefas com descrição e níveis de prioridade (Alta, Média, Baixa).
*   **Listar Tarefas Ativas:** Visualize suas tarefas pendentes, ordenadas por prioridade e data de criação.
*   **Marcar Tarefas como Concluídas:** Mova tarefas da lista de ativas para a lista de concluídas.
*   **Visualizar Tarefas Concluídas:** Acesse uma tela separada para ver todas as tarefas que já foram finalizadas.
*   **Persistência de Dados:** Suas tarefas são salvas localmente no diretório de dados do usuário, garantindo que não sejam perdidas entre as sessões.
*   **Limpeza de Tarefas:** Opções para limpar tarefas ativas, concluídas ou todos os dados, com diálogos de confirmação.
*   **Interface Intuitiva:** Navegação e interação fáceis usando o teclado.

## Instalação

Para instalar o Terminal Tasks App, você precisará do Python 3.8 ou superior.

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    # Se for um repositório git
    git clone <url_do_repositorio>
    cd terminal-tasks-app
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv .venv
    # No Windows
    .venv\Scripts\activate
    # No macOS/Linux
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    O projeto usa `setuptools` para build. Para instalar o pacote localmente em modo editável (para desenvolvimento) ou como um pacote normal:
    ```bash
    pip install -e .  # Modo editável
    # OU
    pip install .     # Instalação normal
    ```
    Isso instalará o `terminal-tasks-app` e suas dependências (`textual`, `platformdirs`).

## Uso

Após a instalação, você pode executar a aplicação com o seguinte comando no seu terminal:

```bash
terminal-tasks
```

A interface principal será exibida, permitindo que você comece a gerenciar suas tarefas.

### Adicionando uma Tarefa

1.  Digite a descrição da tarefa no campo "Descrição da tarefa...".
2.  Selecione a prioridade (1-Alta, 2-Média, 3-Baixa).
3.  Clique no botão "Adicionar Tarefa" ou pressione Enter enquanto o foco estiver no campo de descrição (dependendo da configuração exata do Textual).

### Concluindo uma Tarefa

1.  Selecione uma tarefa na lista "Tarefas Pendentes" usando as teclas de seta.
2.  Clique no botão "Concluir Selecionada".

## Atalhos de Teclado

*   `Ctrl+Q`: Sair da aplicação.
*   `Ctrl+N`: Focar no campo de entrada para adicionar uma nova tarefa.
*   `Ctrl+V`: Abrir a tela de visualização de tarefas concluídas.
*   `Ctrl+A`: Limpar todas as tarefas ativas (com confirmação).
*   `Ctrl+C`: Limpar todas as tarefas concluídas (com confirmação).
*   `Ctrl+X`: Limpar todos os dados de tarefas (ativas e concluídas, com confirmação).
*   `Esc`: (Na tela de tarefas concluídas) Voltar para a tela principal.

## Estrutura do Projeto

*   `src/terminal_tasks_app/app.py`: Contém a lógica principal da aplicação Textual.
*   `src/terminal_tasks_app/styles.tcss`: Arquivo de estilo para a interface da aplicação.
*   `pyproject.toml`: Define os metadados do projeto, dependências e scripts.
*   `DESIGN_DOCUMENT.md`: Documento de design original do projeto.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` (se existir) ou o [`pyproject.toml`](pyproject.toml:11) para mais detalhes. (Atualmente definido como MIT no `pyproject.toml`).