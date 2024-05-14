import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz

def create_graph_from_nodes(nodes):
    G = nx.DiGraph()  # Cria um grafo direcionado
    
    # Adiciona os nós ao grafo
    for node in nodes:
        G.add_node(node.name, expression=node.expression)
    
    # Adiciona as arestas ao grafo com base nos nós conectados
    for node in nodes:
        for connected_node in node.connected_nodes:
            G.add_edge(node.name, connected_node.name)
    
    return G

def draw_graph(G):
    # Gera o layout do grafo usando Graphviz para estilo hierárquico
    pos = graphviz_layout(G, prog='dot')
    
    # Desenha os nós
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=5000, alpha=0.6)
    
    # Desenha as arestas
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20)
    
    # Desenha os rótulos dos nós com os passos
    labels = {node: f"Passo {idx + 1}: {G.nodes[node]['expression']}" for idx, node in enumerate(G.nodes())}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=9)
    
    plt.title('Visualização Hierárquica do Grafo de Passos SQL')
    plt.axis('off')  # Desativa os eixos
    plt.show()
