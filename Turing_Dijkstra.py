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



