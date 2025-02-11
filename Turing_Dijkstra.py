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

