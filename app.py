from textual.app import App, ComposeResult, on
from textual.widgets import Header, Footer, Input, Button, RadioSet, RadioButton, Static, ListView, ListItem, Label
from textual.containers import Container # Importação corrigida
import datetime

class TaskManagerApp(App):
    """Uma aplicação de gerenciador de tarefas baseada em terminal usando Textual."""
    TITLE = "Gerenciador de Tarefas Moderno"
    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("ctrl+q", "quit", "Sair"),
        ("ctrl+n", "focus_new_task_input", "Nova Tarefa")
    ]

    def __init__(self):
        """Inicializa a aplicação e as listas de tarefas."""
        super().__init__()
        self.tarefas_ativas = []
        self.tarefas_concluidas = []
        self.proximo_id_tarefa = 1

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
            'data_criacao': datetime.datetime.now().isoformat()
        }
        self.tarefas_ativas.append(nova_tarefa)
        self.proximo_id_tarefa += 1
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
            self.tarefas_ativas.remove(tarefa_encontrada)
            self.tarefas_concluidas.append(tarefa_encontrada)
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

if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()