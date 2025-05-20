from textual.app import App, ComposeResult, on
from textual.widgets import Header, Footer, Input, Button, RadioSet, RadioButton, Static, ListView, ListItem, Label
from textual.containers import Container, Vertical, Horizontal # Added Vertical, Horizontal
from textual.screen import Screen, ModalScreen # Added ModalScreen
from textual.binding import Binding # Added import
import datetime
import json
from importlib import resources
from pathlib import Path
from platformdirs import user_data_dir
from typing import Callable # Added Callable

APP_NAME = "TerminalTasksApp"
APP_AUTHOR = "TerminalTasksDeveloper" # Or a generic author
USER_DATA_PATH = Path(user_data_dir(APP_NAME, APP_AUTHOR, roaming=True))
TASKS_FILE_PATH = USER_DATA_PATH / "tasks.json"

class TaskManagerApp(App):
    """Uma aplicação de gerenciador de tarefas baseada em terminal usando Textual."""
    TITLE = "Gerenciador de Tarefas Moderno"
    CSS_PATH = resources.files('terminal_tasks_app').joinpath('styles.tcss').resolve()

    BINDINGS = [
        Binding("ctrl+q", "quit", "Sair"),
        Binding("ctrl+n", "focus_new_task_input", "Nova Tarefa"),
        Binding("ctrl+v", "view_completed_tasks", "Ver Concluídas"),
        Binding("ctrl+a", "clear_active_tasks", "Clear Active Tasks"),
        Binding("ctrl+c", "clear_completed_tasks", "Clear Completed Tasks"),
        Binding("ctrl+x", "clear_all_data", "Clear All Data"),
    ]

    def __init__(self):
        """Inicializa a aplicação e as listas de tarefas."""
        super().__init__()
        self.tarefas_ativas = []
        self.tarefas_concluidas = []
        self.proximo_id_tarefa = 1
        self._carregar_tarefas()

    def _carregar_tarefas(self) -> None:
        if TASKS_FILE_PATH.exists():
            try:
                with open(TASKS_FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tarefas_ativas = data.get("tarefas_ativas", [])
                    self.tarefas_concluidas = data.get("tarefas_concluidas", [])
                    self.proximo_id_tarefa = data.get("proximo_id_tarefa", 1)
                    # Ensure proximo_id_tarefa is at least 1 and greater than any existing ID
                    max_id_ativas = max(t['id'] for t in self.tarefas_ativas) if self.tarefas_ativas else 0
                    max_id_concluidas = max(t['id'] for t in self.tarefas_concluidas) if self.tarefas_concluidas else 0
                    self.proximo_id_tarefa = max(1, max_id_ativas + 1, max_id_concluidas + 1, self.proximo_id_tarefa)
            except (json.JSONDecodeError, IOError) as e:
                self.notify(f"Erro ao carregar tarefas: {e}. Usando listas vazias.", title="Erro de Carregamento", severity="error")
                self.tarefas_ativas = []
                self.tarefas_concluidas = []
                self.proximo_id_tarefa = 1
        else:
            # Se o arquivo não existe, começa com listas vazias (já inicializadas)
            # e salva um arquivo vazio inicial para garantir que o diretório seja válido.
            self._salvar_tarefas()

    def _salvar_tarefas(self) -> None:
        try:
            USER_DATA_PATH.mkdir(parents=True, exist_ok=True) # Ensure directory exists
            with open(TASKS_FILE_PATH, "w", encoding="utf-8") as f:
                data = {
                    "tarefas_ativas": self.tarefas_ativas,
                    "tarefas_concluidas": self.tarefas_concluidas,
                    "proximo_id_tarefa": self.proximo_id_tarefa
                }
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            self.notify(f"Erro ao salvar tarefas: {e}", title="Erro de Salvamento", severity="error")

    def adicionar_tarefa_logica(self, descricao: str, prioridade: int) -> dict:
        """
        Adiciona uma nova tarefa à lista de tarefas ativas.

        Args:
            descricao: A descrição da tarefa.
            prioridade: A prioridade da tarefa (1-Alta, 2-Média, 3-Baixa).

        Returns:
            Um dicionário representando a tarefa adicionada.
        """
        nova_tarefa = {
            'id': self.proximo_id_tarefa,
            'descricao': descricao,
            'prioridade': prioridade,
            'data_criacao': datetime.datetime.now().isoformat(),
            'status': 'ativa' # Added status for clarity, though not strictly used by completed list logic yet beyond presence
        }
        self.tarefas_ativas.append(nova_tarefa)
        self.proximo_id_tarefa += 1
        self._salvar_tarefas()
        return nova_tarefa

    def obter_tarefas_ativas_logica(self) -> list:
        """
        Retorna a lista de tarefas ativas, ordenadas por prioridade e data de criação.

        Returns:
            Uma lista de dicionários, onde cada dicionário representa uma tarefa ativa.
        """
        return sorted(
            self.tarefas_ativas,
            key=lambda t: (t['prioridade'], t['data_criacao'])
        )

    def marcar_tarefa_concluida_logica(self, id_tarefa: int) -> dict | None:
        """
        Move uma tarefa da lista de ativas para a lista de concluídas.

        Args:
            id_tarefa: O ID da tarefa a ser marcada como concluída.

        Returns:
            O dicionário da tarefa concluída se encontrada, caso contrário None.
        """
        tarefa_encontrada = None
        for tarefa in self.tarefas_ativas:
            if tarefa['id'] == id_tarefa:
                tarefa_encontrada = tarefa
                break
        if tarefa_encontrada:
            tarefa_encontrada['status'] = 'concluída' # Update status
            tarefa_encontrada['data_conclusao'] = datetime.datetime.now().isoformat() # Add completion date
            self.tarefas_ativas.remove(tarefa_encontrada)
            self.tarefas_concluidas.append(tarefa_encontrada)
            self._salvar_tarefas()
            return tarefa_encontrada
        return None

    async def _atualizar_listview_tarefas(self) -> None:
        """Atualiza o widget ListView com as tarefas ativas ordenadas."""
        listview = self.query_one("#listview_tarefas", ListView)
        await listview.clear()
        tarefas_ordenadas = self.obter_tarefas_ativas_logica()
        for tarefa_data in tarefas_ordenadas:
            item_label = f"[P{tarefa_data['prioridade']}] {tarefa_data['descricao']}"
            list_item = ListItem(Label(item_label))
            list_item.data = tarefa_data
            
            # Adiciona classe CSS baseada na prioridade da tarefa
            prioridade = tarefa_data['prioridade']
            if prioridade == 1:
                list_item.add_class("prioridade_alta")
            elif prioridade == 2:
                list_item.add_class("prioridade_media")
            elif prioridade == 3:
                list_item.add_class("prioridade_baixa")
                
            await listview.append(list_item)

    async def on_mount(self) -> None:
        """Chamado quando o widget é montado no DOM. Atualiza a lista de tarefas."""
        await self._atualizar_listview_tarefas()

    @on(Button.Pressed, "#botao_adicionar")
    async def handle_adicionar_tarefa_pressed(self) -> None:
        """Manipula o evento de clique do botão 'Adicionar Tarefa'."""
        input_descricao = self.query_one("#input_descricao", Input)
        radioset_prioridade = self.query_one("#radioset_prioridade", RadioSet)
        
        descricao = input_descricao.value
        prioridade_selecionada_id = None
        if radioset_prioridade.pressed_button:
            prioridade_selecionada_id = radioset_prioridade.pressed_button.id

        if not descricao.strip():
            self.notify("Erro: Descrição não pode ser vazia.", title="Erro de Validação", severity="error")
            return

        prioridade_valor = None
        if prioridade_selecionada_id == "prioridade_1": prioridade_valor = 1
        elif prioridade_selecionada_id == "prioridade_2": prioridade_valor = 2
        elif prioridade_selecionada_id == "prioridade_3": prioridade_valor = 3
        
        if prioridade_valor is None:
            self.notify("Erro: Selecione uma prioridade.", title="Erro de Validação", severity="error")
            return

        nova_tarefa = self.adicionar_tarefa_logica(descricao, prioridade_valor)
        input_descricao.value = ""
        
        # Desmarcar o RadioSet
        for radio_button in radioset_prioridade.query(RadioButton):
            radio_button.value = False
        
        await self._atualizar_listview_tarefas()
        self.notify(f"Tarefa '{nova_tarefa['descricao'][:20]}...' adicionada!", title="Sucesso")


    @on(ListView.Selected, "#listview_tarefas")
    def handle_listview_selected(self, event: ListView.Selected) -> None:
        """Manipula o evento de seleção de um item na ListView."""
        botao_concluir = self.query_one("#botao_concluir", Button)
        if event.item is not None: # Um item está selecionado
            botao_concluir.disabled = False
        else:
            # Se nenhum item estiver selecionado (por exemplo, clicar fora ou lista vazia após exclusão)
            botao_concluir.disabled = True

    @on(Button.Pressed, "#botao_concluir")
    async def handle_concluir_tarefa_pressed(self) -> None:
        """Manipula o evento de clique do botão 'Concluir Selecionada'."""
        listview = self.query_one("#listview_tarefas", ListView)
        
        highlighted_item = listview.highlighted_child
        
        if highlighted_item and hasattr(highlighted_item, 'data') and highlighted_item.data:
            id_tarefa_selecionada = highlighted_item.data['id']
            resultado = self.marcar_tarefa_concluida_logica(id_tarefa_selecionada)
            
            if resultado:
                await self._atualizar_listview_tarefas()
                self.notify(f"Tarefa '{resultado['descricao'][:20]}...' concluída!", title="Sucesso")
                self.query_one("#botao_concluir", Button).disabled = True
            else:
                self.notify("Erro ao tentar concluir a tarefa. Tarefa não encontrada.", title="Erro", severity="error")
        else:
            self.notify("Nenhuma tarefa selecionada para concluir.", title="Aviso", severity="warning")

    def action_quit(self) -> None:
        """Ação para sair da aplicação."""
        self.exit()

    def action_focus_new_task_input(self) -> None:
        """Ação para focar no campo de input de nova tarefa."""
        self.query_one("#input_descricao", Input).focus()

    def action_view_completed_tasks(self) -> None:
        """Ação para exibir a tela de tarefas concluídas."""
        self.push_screen(CompletedTasksScreen())

    async def _perform_clear_active_tasks(self) -> None:
        """Executa a lógica de limpar todas as tarefas ativas."""
        if self.tarefas_ativas:
            self.tarefas_ativas = []
            self._salvar_tarefas() # Synchronous call
            await self._atualizar_listview_tarefas() 
            self.notify("Active tasks cleared successfully.", title="Success", severity="information")
        else:
            self.notify("Active tasks list is already empty.", title="Information", severity="information")

    async def action_clear_active_tasks(self) -> None: 
        """Ação para limpar todas as tarefas ativas após confirmação."""
        await self.push_screen( 
            ConfirmationDialog(
                message="Are you sure you want to clear all active tasks?",
                callback=self._perform_clear_active_tasks
            )
        )

    async def _perform_clear_completed_tasks(self) -> None:
        """Executa a lógica de limpar todas as tarefas concluídas."""
        if self.tarefas_concluidas:
            self.tarefas_concluidas = []
            self._salvar_tarefas() # Synchronous call
            # Update the CompletedTasksScreen's ListView if it's the current screen
            if isinstance(self.screen, CompletedTasksScreen):
                await self.screen._atualizar_listview_tarefas_concluidas()
            self.notify("Completed tasks cleared successfully.", title="Success", severity="information")
        else:
            self.notify("Completed tasks list is already empty.", title="Information", severity="information")

    async def action_clear_completed_tasks(self) -> None:
        """Ação para limpar todas as tarefas concluídas após confirmação."""
        await self.push_screen(
            ConfirmationDialog(
                message="Are you sure you want to clear all completed tasks?",
                callback=self._perform_clear_completed_tasks
            )
        )

    async def _perform_clear_all_data(self) -> None:
        """Executa a lógica de limpar todos os dados de tarefas (ativas e concluídas)."""
        if not self.tarefas_ativas and not self.tarefas_concluidas:
            self.notify("All task lists are already empty.", title="Information", severity="information")
            return

        self.tarefas_ativas = []
        self.tarefas_concluidas = []
        self._salvar_tarefas() # Synchronous call
        
        await self._atualizar_listview_tarefas()
        
        if isinstance(self.screen, CompletedTasksScreen):
            await self.screen._atualizar_listview_tarefas_concluidas()
            
        self.notify("All task data cleared successfully.", title="Success", severity="information")

    async def action_clear_all_data(self) -> None:
        """Ação para limpar todos os dados de tarefas após confirmação."""
        await self.push_screen(
            ConfirmationDialog(
                message="Are you sure you want to clear ALL task data (active and completed)? This cannot be undone.",
                callback=self._perform_clear_all_data
            )
        )

    def compose(self) -> ComposeResult:
        """Compõe a interface do usuário da aplicação."""
        yield Header()
        with Container(id="area_adicionar_tarefa"):
            yield Static("Nova Tarefa:", classes="label_secao")
            yield Input(placeholder="Descrição da tarefa...", id="input_descricao")
            with Container(id="container_prioridade_botao"): # Novo container
                yield RadioSet(
                    RadioButton("1 (Alta)", id="prioridade_1"),
                    RadioButton("2 (Média)", id="prioridade_2"),
                    RadioButton("3 (Baixa)", id="prioridade_3"),
                    id="radioset_prioridade"
                )
                yield Button("Adicionar Tarefa", id="botao_adicionar")
        with Container(id="area_listagem_tarefas"):
            yield Static("Tarefas Pendentes:", id="label_tarefas_pendentes")
            yield ListView(id="listview_tarefas")
            yield Button("Concluir Selecionada", id="botao_concluir", disabled=True)
        yield Footer()

class CompletedTasksScreen(Screen):
    """Tela para exibir tarefas concluídas."""
    TITLE = "Tarefas Concluídas"

    BINDINGS = [
        Binding("escape", "pop_screen", "Voltar")
    ]

    def action_pop_screen(self) -> None:
        """Fecha a tela atual e retorna à anterior."""
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        """Compõe a interface da tela de tarefas concluídas."""
        yield Header() 
        yield ListView(id="listview_tarefas_concluidas")
        yield Footer()

    async def on_mount(self) -> None:
        """Chamado quando a tela é montada. Popula a lista de tarefas concluídas."""
        await self._atualizar_listview_tarefas_concluidas()

    async def _atualizar_listview_tarefas_concluidas(self) -> None:
        """Atualiza o ListView com as tarefas concluídas."""
        list_view = self.query_one("#listview_tarefas_concluidas", ListView)
        await list_view.clear()
        
        # Accessing tarefas_concluidas from the main app instance
        completed_tasks = sorted(
            self.app.tarefas_concluidas, 
            key=lambda t: t.get('data_conclusao', ''), 
            reverse=True
        ) # Sort by completion date, newest first
        
        if not completed_tasks:
            # Consider adding a Label here if preferred:
            # yield Label("Nenhuma tarefa concluída ainda.", classes="empty_list_label")
            pass # ListView will be empty
        else:
            for task in completed_tasks:
                # Display task ID and description. Could be extended with completion date.
                item_label = f"ID {task.get('id', 'N/A')}: {task.get('descricao', 'Descrição não disponível')}"
                if 'data_conclusao' in task:
                    try:
                        dt_conclusao = datetime.datetime.fromisoformat(task['data_conclusao']).strftime('%Y-%m-%d %H:%M')
                        item_label += f" (Concluída: {dt_conclusao})"
                    except ValueError: # Handle cases where date might not be a full ISO string
                        item_label += f" (Concluída: {task['data_conclusao']})"

                list_item = ListItem(Static(item_label))
                # list_item.data = task # Store task data if needed for future interactions
                await list_view.append(list_item)

class ConfirmationDialog(ModalScreen):
    """Um modal de confirmação genérico."""

    def __init__(self, message: str, callback: Callable, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.message = message
        self.callback = callback # This will be an async callable

    def compose(self) -> ComposeResult:
        """Compõe o modal com mensagem e botões de Sim/Não."""
        with Vertical(id="confirmation_dialog_vertical", classes="modal_dialog_content"): # Added classes for potential styling
            yield Label(self.message, id="confirmation_message")
            with Horizontal(id="confirmation_buttons_horizontal", classes="modal_buttons_container"): # Added classes
                yield Button("Sim", variant="success", id="yes_button", classes="modal_button")
                yield Button("Não", variant="error", id="no_button", classes="modal_button")
    
    @on(Button.Pressed)
    async def on_button_pressed(self, event: Button.Pressed) -> None: # Make this async
        """Manipula o pressionamento dos botões Sim/Não."""
        if event.button.id == "yes_button":
            if self.callback: # Executa o callback se existir
                await self.callback() # Await the callback as it's async now
        self.app.pop_screen() # Fecha o modal independentemente da escolha


def main():
    USER_DATA_PATH.mkdir(parents=True, exist_ok=True) # Ensure user data directory exists
    app = TaskManagerApp()
    app.run()

if __name__ == "__main__":
    main()
