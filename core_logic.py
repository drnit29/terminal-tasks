import uuid
import datetime
from typing import List, Dict, TypedDict, Union

class Tarefa(TypedDict):
    id: str
    descricao: str
    prioridade: int
    data_criacao: str

tarefas_ativas: List[Tarefa] = []
tarefas_concluidas: List[Tarefa] = []

def adicionar_tarefa_logica(descricao: str, prioridade: int) -> Tarefa:
    """
    Cria um novo objeto Tarefa com um id único e data_criacao atual.
    Adiciona a nova tarefa à lista tarefas_ativas.
    Retorna a tarefa criada.
    """
    nova_tarefa: Tarefa = {
        "id": str(uuid.uuid4()),
        "descricao": descricao,
        "prioridade": prioridade,
        "data_criacao": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    tarefas_ativas.append(nova_tarefa)
    return nova_tarefa

def obter_tarefas_ativas_logica() -> List[Tarefa]:
    """
    Ordena a lista tarefas_ativas:
        1. Primariamente por prioridade (ascendente, 1 primeiro).
        2. Secundariamente por data_criacao (ascendente, mais antigas primeiro)
           para tarefas com a mesma prioridade.
    Retorna a lista ordenada de tarefas ativas.
    """
    return sorted(tarefas_ativas, key=lambda tarefa: (tarefa["prioridade"], tarefa["data_criacao"]))

def marcar_tarefa_concluida_logica(id_tarefa: str) -> bool:
    """
    Busca a tarefa na tarefas_ativas pelo id_tarefa.
    Se encontrada:
        Remove a tarefa da lista tarefas_ativas.
        Adiciona a tarefa à lista tarefas_concluidas.
        Retorna True.
    Se não encontrada, retorna False.
    """
    for i, tarefa in enumerate(tarefas_ativas):
        if tarefa["id"] == id_tarefa:
            tarefa_concluida = tarefas_ativas.pop(i)
            tarefas_concluidas.append(tarefa_concluida)
            return True
    return False