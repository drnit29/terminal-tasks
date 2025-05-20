# Diretrizes de Desenvolvimento para Agente IA

## 1. Visão Geral do Projeto

### 1.1. Propósito do Projeto
- Implementar um Gerenciador de Tarefas de Terminal interativo.

### 1.2. Pilha de Tecnologia
- Python
- Textual

### 1.3. Funcionalidade Principal (Referência: `DESIGN_DOCUMENT.md`)
- Adicionar tarefas com descrição e prioridade.
- Visualizar tarefas ativas, ordenadas por prioridade (ascendente) e data de criação (ascendente).
- Marcar tarefas como concluídas.
- Interagir através de uma interface de usuário baseada em Textual.

## 2. Arquitetura do Projeto

### 2.1. Estrutura de Diretório e Arquivos Chave
- **[`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1)**: Fonte primária para design, requisitos e funcionalidade. **SEMPRE CONSULTE PRIMEIRO.**
- **`app.py` (ou `main.py`)**: Arquivo principal. Contém a classe `App` do Textual, estruturas de dados de tarefas, e funções de lógica de negócios (`*_logica`).
    - **FAZER:** Implementar toda a lógica de manipulação de dados de tarefas (criar, ler, atualizar, deletar tarefas) DENTRO das funções `*_logica` neste arquivo.
    - **FAZER:** Definir o layout da UI (widgets) no método `compose()` da classe App.
- **`styles.tcss`**: Arquivo de estilização. Contém todas as regras TCSS para a UI.
    - **FAZER:** Implementar TODA a estilização visual neste arquivo.
- **`tasks.json` (Futuro)**: Arquivo para persistência de dados de tarefas (se implementado).
    - **Referência:** Seção 6 do [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:161) ([`DESIGN_DOCUMENT.md:161-178`](DESIGN_DOCUMENT.md:161)) para estrutura e lógica de manipulação.
- **`shrimp-rules.md` (Este documento)**: Regras operacionais para o Agente IA.

## 3. Padrões de Código

### 3.1. Nomenclatura
- Classes Python: `CamelCase` (ex: `TaskItem`, `MainApp`).
- Funções/Métodos Python: `snake_case` (ex: [`adicionar_tarefa_logica()`](DESIGN_DOCUMENT.md:47), `on_button_pressed()`).
- Variáveis Python: `snake_case` (ex: `nova_tarefa`, `tarefas_ativas`).
- Constantes Python: `UPPER_SNAKE_CASE` (ex: `MAX_PRIORITY = 3`).
- IDs de Widgets Textual (em `app.py` e `styles.tcss`): `snake_case` (ex: `id="input_descricao"`, `#input_descricao`).

### 3.2. Formatação
- Código Python: Seguir PEP 8.
- TCSS: Manter formatação consistente, indentação clara para seletores aninhados.

### 3.3. Comentários
- Docstrings: Para todas as classes e funções/métodos públicos em Python.
- Comentários em linha: Apenas para lógica complexa ou não óbvia.
- **NÃO FAZER:** Comentar código óbvio.

## 4. Padrões de Implementação de Funcionalidade

### 4.1. Separação Lógica vs. UI
- **FAZER:** Lógica de negócios (manipulação de dados de tarefas) DEVE residir EXCLUSIVIVAMENTE nas funções `*_logica` em `app.py` (ex: [`adicionar_tarefa_logica()`](DESIGN_DOCUMENT.md:47), [`obter_tarefas_ativas_logica()`](DESIGN_DOCUMENT.md:52), [`marcar_tarefa_concluida_logica()`](DESIGN_DOCUMENT.md:58)). Estas funções NÃO DEVEM interagir diretamente com widgets Textual.
    - **Referência:** Seção 2 do [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:43) ([`DESIGN_DOCUMENT.md:43-63`](DESIGN_DOCUMENT.md:43)).
- **FAZER:** Manipuladores de eventos da UI Textual (ex: `on_button_pressed()`) em `app.py` DEVEM:
    1. Ler dados dos widgets da UI (se necessário).
    2. Chamar as funções `*_logica` apropriadas.
    3. Usar o retorno das funções `*_logica` para atualizar os widgets da UI (ex: repopular `ListView`).
- **NÃO FAZER:** Implementar lógica de manipulação de dados de tarefas diretamente dentro dos manipuladores de eventos da UI.

### 4.2. Atualização da UI
- **FAZER:** Após CADA modificação nos dados das tarefas (adicionar, concluir), a `ListView` de tarefas ativas DEVE ser atualizada. Obtenha os dados atualizados chamando [`obter_tarefas_ativas_logica()`](DESIGN_DOCUMENT.md:52) e repopule o widget.
- **FAZER:** Exibir mensagens de feedback ao usuário (ex: "Tarefa adicionada!") no widget `Footer`.
    - **Referência:** [`DESIGN_DOCUMENT.md:85`](DESIGN_DOCUMENT.md:85), [`DESIGN_DOCUMENT.md:96`](DESIGN_DOCUMENT.md:96), [`DESIGN_DOCUMENT.md:106`](DESIGN_DOCUMENT.md:106).

### 4.3. Estruturas de Dados das Tarefas
- **FAZER:** Utilizar a estrutura de objeto/dicionário para `Tarefa` conforme definido em [`DESIGN_DOCUMENT.md:12-16`](DESIGN_DOCUMENT.md:12) (`id`, `descricao`, `prioridade`, `data_criacao`).
- **FAZER:** Manter `tarefas_ativas` e `tarefas_concluidas` como listas de objetos `Tarefa` em `app.py` ([`DESIGN_DOCUMENT.md:19-20`](DESIGN_DOCUMENT.md:19)).

### 4.4. Tratamento de Erros (Básico)
- **FAZER:** Impedir a conclusão de tarefa se nenhuma estiver selecionada na `ListView` (desabilitar o botão "Concluir Selecionada" ou verificar antes de chamar a lógica).
    - **Referência:** [`DESIGN_DOCUMENT.md:84`](DESIGN_DOCUMENT.md:84), [`DESIGN_DOCUMENT.md:102`](DESIGN_DOCUMENT.md:102).

## 5. Padrões de Uso do Framework Textual

### 5.1. Estrutura da Aplicação Textual
- **FAZER:** Classe principal da aplicação DEVE herdar de `textual.app.App`.
- **FAZER:** Layout inicial dos widgets DEVE ser definido no método `compose()`.
- **FAZER:** Usar `styles.tcss` para TODA estilização principal.
    - **Referência:** [`DESIGN_DOCUMENT.md:70-72`](DESIGN_DOCUMENT.md:70).

### 5.2. Widgets Chave (Conforme [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1) Seção 3)
- `Header`: [`DESIGN_DOCUMENT.md:75`](DESIGN_DOCUMENT.md:75)
- `Input` (descrição): [`DESIGN_DOCUMENT.md:78`](DESIGN_DOCUMENT.md:78)
- `RadioSet` ou `Select` (prioridade): [`DESIGN_DOCUMENT.md:79`](DESIGN_DOCUMENT.md:79). **Implementar com `RadioSet` por padrão.**
- `Button` (Adicionar, Concluir): [`DESIGN_DOCUMENT.md:80`](DESIGN_DOCUMENT.md:80), [`DESIGN_DOCUMENT.md:84`](DESIGN_DOCUMENT.md:84)
- `ListView` / `ListItem`: [`DESIGN_DOCUMENT.md:83`](DESIGN_DOCUMENT.md:83)
- `Footer`: [`DESIGN_DOCUMENT.md:85`](DESIGN_DOCUMENT.md:85)
- **NÃO FAZER:** Usar widgets complexos não especificados no [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1) sem instrução explícita.

### 5.3. Manipulação de Eventos Textual
- **FAZER:** Usar decoradores `on` (ex: `@on(Button.Pressed, "#id_do_botao")`) ou métodos `on_<widget_type>_<event_type>`.

### 5.4. Estilização (TCSS)
- **FAZER:** Definir TODOS os estilos em `styles.tcss`.
- **FAZER:** Usar seletores de ID, tipo e classes de estilo.
- **FAZER:** Aplicar feedback visual para estados (`:focus`, `:hover`, `--current`, `--disabled`) conforme [`DESIGN_DOCUMENT.md:114-119`](DESIGN_DOCUMENT.md:114).
- **NÃO FAZER:** Aplicar estilos inline excessivos no código Python.

## 6. Padrões de Fluxo de Trabalho

### 6.1. Fluxo Principal da Aplicação
- **Referência:** Seção 4 e Diagrama Mermaid na Seção 5 do [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:122) ([`DESIGN_DOCUMENT.md:122-152`](DESIGN_DOCUMENT.md:122)). O fluxo DEVE seguir este diagrama.

### 6.2. Atalhos de Teclado (Bindings)
- **FAZER:** Implementar bindings no atributo `BINDINGS` da classe App.
- **Exemplos:** `Ctrl+Q` (Sair), `Ctrl+N` (Foco no input de nova tarefa).
    - **Referência:** [`DESIGN_DOCUMENT.md:107`](DESIGN_DOCUMENT.md:107).

## 7. Padrões de Interação de Arquivos Chave

- **`app.py` <-> `styles.tcss`**:
    - **FAZER:** Ao adicionar/modificar widget em `app.py` que necessite estilo, adicionar/modificar o estilo correspondente em `styles.tcss` usando o ID do widget.
- **`app.py` <-> [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1)**:
    - **FAZER:** Antes de implementar novas funcionalidades ou alterações significativas, VERIFICAR o [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1).
- **`app.py` <-> `tasks.json` (Futuro)**:
    - **FAZER:** Se persistência for implementada, `app.py` LÊ de `tasks.json` na inicialização e ESCREVE para `tasks.json` após modificações de dados. Estrutura conforme [`DESIGN_DOCUMENT.md:165-173`](DESIGN_DOCUMENT.md:165).

## 8. Padrões de Tomada de Decisão para IA

### 8.1. Prioridade da Fonte de Verdade
    1. [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1)
    2. `shrimp-rules.md` (este documento)
    3. Código existente (para consistência)

### 8.2. Ambiguidade no [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1)
- **FAZER:** Se especificação for vaga e não crítica, usar interpretação mais simples e lógica. Adicionar comentário `# TODO: Clarify [aspecto] from DESIGN_DOCUMENT.md`.

### 8.3. Adição de Funcionalidades Não Especificadas
- **NÃO FAZER:** Adicionar widgets/funcionalidades não descritos no [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1) a menos que seja consequência direta e mínima de uma solicitação explícita E justificada.

## 9. Ações Proibidas

- **NÃO FAZER:** Incluir conhecimento geral de desenvolvimento Python/Textual neste documento.
- **NÃO FAZER:** Explicar a funcionalidade do projeto aqui (usar [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1)).
- **NÃO FAZER:** Modificar estruturas de dados centrais (`Task`, listas de tarefas) de forma incompatível com [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1) sem instrução.
- **NÃO FAZER:** Alterar nomes das funções lógicas principais ([`adicionar_tarefa_logica()`](DESIGN_DOCUMENT.md:47), etc.).
- **NÃO FAZER:** Ignorar requisitos de estilização e feedback visual do [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:109) ([`DESIGN_DOCUMENT.md:109-120`](DESIGN_DOCUMENT.md:109)).
- **NÃO FAZER:** Introduzir novas dependências externas sem aprovação.
- **NÃO FAZER:** Escrever código que não siga os padrões de nomenclatura e formatação aqui definidos.
- **NÃO FAZER:** Especular. Em caso de dúvida, revisar código relacionado ou o [`DESIGN_DOCUMENT.md`](DESIGN_DOCUMENT.md:1).