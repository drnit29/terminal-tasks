from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Input, ListView, ListItem, Label, RadioSet, RadioButton, Static
from textual.binding import Binding

from core_logic import adicionar_tarefa_logica, obter_tarefas_ativas_logica, marcar_tarefa_concluida_logica, Tarefa

class TaskListItem(ListItem):
    def __init__(self, tarefa):
        super().__init__()
        self.tarefa_id = tarefa["id"]
        self.tarefa_descricao = tarefa["descricao"]
        self.tarefa_prioridade = tarefa["prioridade"]

    def compose(self):
        yield Label(f"[P{self.tarefa_prioridade}] {self.tarefa_descricao}")

class TaskManagerApp(App):
    TITLE = "TaskManager"
    SUB_TITLE = ""
    CSS_PATH = "styles.tcss"

    BINDINGS = [
        Binding("ctrl+q", "quit", "Sair"),
        Binding("ctrl+1", "set_priority_1", "Prioridade Alta (1)"),
        Binding("ctrl+2", "set_priority_2", "Prioridade Média (2)"),
        Binding("ctrl+3", "set_priority_3", "Prioridade Baixa (3)"),
    ]

    def compose(self):
        yield Header()
        with Container(id="main_container"):
            # Área de Adicionar Tarefa
            with Container(id="add_task_area"):
                yield Input(placeholder="Nova tarefa...", id="new_task_description")
                with RadioSet(id="priority_radioset"):
                    yield RadioButton("1 (Alta)", id="priority_1", value=1)
                    yield RadioButton("2 (Média)", id="priority_2", value=2)
                    yield RadioButton("3 (Baixa)", id="priority_3", value=3)
                yield Button("Adicionar Tarefa", id="add_task_button", variant="primary")

            # Área de Listagem de Tarefas Ativas
            with Container(id="active_tasks_area"):
                yield Label("Tarefas Pendentes:", id="active_tasks_label")
                yield ListView(id="active_tasks_list")
                yield Button("Concluir Selecionada", id="complete_task_button", disabled=True)
        
        yield Static(id="status_line", classes="status-bar") # Adicionado para mensagens de status
        yield Footer()

    def on_mount(self):
        """Chamado quando o app é montado."""
        self.atualizar_lista_tarefas()
        # Define a prioridade padrão para Média (2)
        radio_set = self.query_one(RadioSet)
        # radio_set.pressed_index = 1 # Índice 1 corresponde à prioridade 2 (Média) <- Linha original com erro
        try:
            # Os RadioButtons têm IDs: priority_1, priority_2, priority_3
            # Seleciona o RadioButton com id "priority_2" (Média)
            priority_medium_button = radio_set.query_one("#priority_2", RadioButton)
            priority_medium_button.value = True
        except Exception as e:
            # Adiciona um log ou notificação em caso de erro, para debug.
            self.app.bell()
            self.app.log(f"Erro ao definir RadioButton padrão em on_mount: {e}")


    def atualizar_lista_tarefas(self):
        """Busca tarefas ativas da lógica e atualiza a ListView."""
        list_view = self.query_one(ListView)
        list_view.clear()
        tarefas = obter_tarefas_ativas_logica()
        for tarefa in tarefas:
            list_view.append(TaskListItem(tarefa))
        
        # Desabilita o botão de concluir se a lista estiver vazia ou nenhum item selecionado
        btn_concluir = self.query_one("#complete_task_button", Button)
        if not tarefas or list_view.index is None:
            btn_concluir.disabled = True
        else:
            # Se houver itens e um estiver selecionado (após uma atualização, a seleção pode persistir)
            # Reavalia se o botão deve estar habilitado.
            # No entanto, após limpar e popular, o index será None.
            btn_concluir.disabled = list_view.index is None


    def on_button_pressed(self, event: Button.Pressed):
        """Chamado quando um botão é pressionado."""
        if event.button.id == "add_task_button":
            input_descricao = self.query_one("#new_task_description", Input)
            radioset_prioridade = self.query_one("#priority_radioset", RadioSet)
            
            descricao = input_descricao.value
            prioridade_selecionada = radioset_prioridade.pressed_button

            if descricao and prioridade_selecionada:
                # O valor do RadioButton foi definido como o inteiro da prioridade
                prioridade = prioridade_selecionada.value
                if isinstance(prioridade, int):
                    nova_tarefa = adicionar_tarefa_logica(descricao, prioridade)
                    self.atualizar_lista_tarefas()
                    input_descricao.value = ""
                    # Reset RadioSet para o padrão (Média) ou limpar seleção
                    # radioset_prioridade.pressed_index = 1 # Média <- Linha original com erro
                    try:
                        priority_medium_button = radioset_prioridade.query_one("#priority_2", RadioButton)
                        priority_medium_button.value = True
                    except Exception as e:
                        self.app.bell()
                        self.app.log(f"Erro ao resetar RadioButton em on_button_pressed: {e}")
                    self.query_one("#status_line", Static).update(f"Tarefa '{nova_tarefa['descricao']}' adicionada!")
                else:
                    self.query_one("#status_line", Static).update("Erro: Prioridade inválida selecionada.")
            else:
                self.query_one("#status_line", Static).update("Por favor, insira a descrição e selecione a prioridade.")

        elif event.button.id == "complete_task_button":
            list_view = self.query_one(ListView)
            if list_view.highlighted_child: # Verifica se há um item destacado/selecionado
                selected_item = list_view.highlighted_child
                if isinstance(selected_item, TaskListItem):
                    tarefa_id = selected_item.tarefa_id
                    marcar_tarefa_concluida_logica(tarefa_id)
                    self.atualizar_lista_tarefas()
                    self.query_one("#status_line", Static).update(f"Tarefa '{selected_item.tarefa_descricao}' concluída!")
                    # O botão será desabilitado pela atualizar_lista_tarefas se a seleção for perdida
            else:
                self.query_one("#status_line", Static).update("Nenhuma tarefa selecionada para concluir.")


    def on_list_view_selected(self, event: ListView.Selected):
        """Chamado quando um item na ListView é selecionado."""
        btn_concluir = self.query_one("#complete_task_button", Button)
        # O evento Selected garante que event.item não é None
        if event.item:
            btn_concluir.disabled = False
        else: # Embora Selected implique um item, é bom ter um fallback
            btn_concluir.disabled = True
            
    def on_list_view_highlighted(self, event: ListView.Highlighted):
        """Chamado quando um item na ListView é destacado (pode ser None)."""
        btn_concluir = self.query_one("#complete_task_button", Button)
        if event.item is None: # Se nenhum item estiver destacado (ex: lista vazia ou foco perdido)
            btn_concluir.disabled = True
        # Não habilitamos aqui, pois Selected é o evento mais apropriado para habilitar.
        # Highlighted pode ocorrer ao navegar sem uma "seleção" final.

    def action_set_priority_1(self) -> None:
        """Define a prioridade da tarefa como Alta (1) via atalho de teclado."""
        self.app.log("action_set_priority_1 CALLED")
        try:
            radio_button = self.query_one("#priority_1", RadioButton)
            radio_button.value = True
            self.query_one("#new_task_description", Input).focus()
            self.query_one("#status_line", Static).update("Prioridade definida como Alta (1)")
        except Exception as e:
            self.app.log(f"Erro em action_set_priority_1: {e}")
            self.app.bell()

    def action_set_priority_2(self) -> None:
        """Define a prioridade da tarefa como Média (2) via atalho de teclado."""
        self.app.log("action_set_priority_2 CALLED")
        try:
            radio_button = self.query_one("#priority_2", RadioButton)
            radio_button.value = True
            self.query_one("#new_task_description", Input).focus()
            self.query_one("#status_line", Static).update("Prioridade definida como Média (2)")
        except Exception as e:
            self.app.log(f"Erro em action_set_priority_2: {e}")
            self.app.bell()

    def action_set_priority_3(self) -> None:
        """Define a prioridade da tarefa como Baixa (3) via atalho de teclado."""
        self.app.log("action_set_priority_3 CALLED")
        try:
            radio_button = self.query_one("#priority_3", RadioButton)
            radio_button.value = True
            self.query_one("#new_task_description", Input).focus()
            self.query_one("#status_line", Static).update("Prioridade definida como Baixa (3)")
        except Exception as e:
            self.app.log(f"Erro em action_set_priority_3: {e}")
            self.app.bell()

if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()