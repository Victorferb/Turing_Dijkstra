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
       
        self.states = states
        self.tape = list(tape) + ['_']  
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.head = 0  
    
    def run(self):
       
        priority_queue = [(0, self.start_state, self.head, list(self.tape), [])]  
        visited = set()

        while priority_queue:
            cost, state, head, tape, path = heapq.heappop(priority_queue)  
            
            
            if (state, head, tuple(tape)) in visited:
                continue
            visited.add((state, head, tuple(tape)))
            
            
            if state in self.accept_states:
                return ''.join(tape), path, cost
            
            
            current_symbol = tape[head] if 0 <= head < len(tape) else '_'
            
            
            if (state, current_symbol) in self.transitions:
                for next_state, write_symbol, move, weight in self.transitions[(state, current_symbol)]:
                    new_tape = tape[:]
                    new_tape[head] = write_symbol  
                    new_head = head + (1 if move == 'R' else -1)  
                    
                    
                    if new_head < 0:
                        new_tape.insert(0, '_')
                        new_head = 0
                    elif new_head >= len(new_tape):
                        new_tape.append('_')
                    
                    
                    heapq.heappush(priority_queue, (cost + weight, next_state, new_head, new_tape, path + [(state, next_state, weight)]))
        
        return None  

