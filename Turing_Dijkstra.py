"""
Implementação de uma máquina de turing nao determinista e de fita limitada
onde as arestas são ponderadas e dar como resultados:

- fita final
- caminho percorrido
- soma ponderada das arestas

O truque é alterar o grafo da máquina e trocar o bfs por um djkistra
"""

#Bibliotecas utilizadas
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class TuringMachine:
    def __init__(self, states, tape, transitions, start_state, accept_states):
        """
        Inicializa a Máquina de Turing.
        
        :param states: Conjunto de estados da máquina.
        :param tape: Lista representando a fita inicial.
        :param transitions: Dicionário de transições, onde a chave é (estado, símbolo) e o valor é uma lista de tuplas
                            (próximo estado, símbolo a ser escrito, direção do movimento, peso da transição).
        :param start_state: Estado inicial da máquina.
        :param accept_states: Conjunto de estados de aceitação.
        """
        self.states = states
        self.tape = list(tape) + ['_']  # Garante que a fita termina em um espaço em branco
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.head = 0  # Posição inicial do cabeçote na fita
    
    def run(self):
        """
        Executa a Máquina de Turing usando Dijkstra para encontrar o caminho de menor peso até um estado de aceitação.
        
        :return: (fita final, caminho percorrido, soma ponderada das arestas) ou None se nenhum estado de aceitação for atingido.
        """
        # Fila de prioridade (min-heap) para escolher sempre o caminho de menor custo primeiro
        priority_queue = [(0, self.start_state, self.head, list(self.tape), [])]  # (custo, estado, posição da cabeça, fita, caminho percorrido)
        visited = set()  # Conjunto para armazenar estados já visitados e evitar loops infinitos
        
        while priority_queue:
            cost, state, head, tape, path = heapq.heappop(priority_queue)  # Extrai o nó de menor custo
            
            # Verifica se esse estado já foi visitado para evitar ciclos
            if (state, head, tuple(tape)) in visited:
                continue
            visited.add((state, head, tuple(tape)))
            
            # Se chegamos a um estado de aceitação, retornamos o resultado
            if state in self.accept_states:
                return ''.join(tape), path, cost
            
            # Obtém o símbolo atual da fita (ou '_' caso esteja fora dos limites)
            current_symbol = tape[head] if 0 <= head < len(tape) else '_'
            
            # Verifica se há transições para o estado atual e símbolo lido
            if (state, current_symbol) in self.transitions:
                for next_state, write_symbol, move, weight in self.transitions[(state, current_symbol)]:
                    new_tape = tape[:]
                    new_tape[head] = write_symbol  # Escreve na fita
                    new_head = head + (1 if move == 'R' else -1)  # Move a cabeça para direita (R) ou esquerda (L)
                    
                    # Se o movimento for para fora da fita, expande a fita
                    if new_head < 0:
                        new_tape.insert(0, '_')
                        new_head = 0
                    elif new_head >= len(new_tape):
                        new_tape.append('_')
                    
                    # Adiciona a nova configuração na fila de prioridade
                    heapq.heappush(priority_queue, (cost + weight, next_state, new_head, new_tape, path + [(state, next_state, weight)]))
        
        return None  # Retorna None se nenhum estado de aceitação for atingido

def draw_graph(transitions):
    """ Gera uma visualização do grafo de transições da Máquina de Turing """
    G = nx.DiGraph()
    
    for (state, symbol), transitions_list in transitions.items():
        for next_state, write_symbol, move, weight in transitions_list:
            G.add_edge(state, next_state, label=f'{symbol}/{write_symbol}, {move}, {weight}')
    
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

# Definição dos estados, fita inicial, transições e estado inicial
states = {'q0', 'q1', 'q2', 'q3', 'q_accept'}  # Conjunto de estados da máquina

tape = ['1', '0', '1', '1', '0']  # Configuração inicial da fita

# Definição das transições da máquina
# Formato: (estado atual, símbolo lido) -> [(próximo estado, símbolo escrito, direção do movimento, peso da transição)]
transitions = {
    ('q0', '1'): [('q1', '0', 'R', 4)],
    ('q1', '0'): [('q2', '1', 'R', 3)],
    ('q2', '1'): [('q3', '0', 'R', 6)],
    ('q3', '1'): [('q4', '1', 'R', 1)],
    ('q4', '0'): [('q_accept', '_', 'R', 3)],
    ('q4', '_'): [('q_accept', '_', 'R', 2)]
}


start_state = 'q0'  # Estado inicial
accept_states = {'q_accept'}  # Estados de aceitação



# Criando e executando a máquina de Turing
machine = TuringMachine(states, tape, transitions, start_state, accept_states)
result = machine.run()

# Exibindo os resultados
print("Fita final:", result[0] if result else "Rejeitado")
print("Caminho percorrido:", result[1] if result else "Nenhum")
print("Soma ponderada:", result[2] if result else "N/A")

# Gerando o grafo de transições
draw_graph(transitions)

