import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()


G.add_weighted_edges_from([
('A','B',4),
('A','E',5),
('E','F',6),
('F','D',7),
('B','C',8),
('F','G',9),
('F','H',11)])

pos = nx.shell_layout(G) 
nx.draw_networkx_nodes(G, pos, node_color="pink", node_size=700)
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
nx.draw_networkx_edges(G, pos, width=4)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

print("Ruta mas barata: ", nx.algorithms.shortest_path(G, 'A', 'H')," y su Gasto de Combustible: ",nx.dijkstra_path_length(G,'A','E'))


plt.show()