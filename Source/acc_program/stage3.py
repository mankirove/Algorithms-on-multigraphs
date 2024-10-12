import numpy as np
import networkx as nx
import itertools
import time


def read_graphs_from_file(file_path):
    with open(file_path, 'r') as file:
        line = file.readline()
        num_graphs = int(line.strip()) 
        graphs = []
        current_graph = []
        graph_count = 0

        while graph_count < num_graphs:
            line = file.readline().strip()

            if line.isdigit():
                
                size = int(line)
                current_graph = []

               
                for _ in range(size):
                    row = list(map(int, file.readline().strip().split()))
                    current_graph.append(row)

                graphs.append(np.array(current_graph, dtype=int))
                graph_count += 1
    
    return graphs


def find_largest_clique(graph):
    largest_clique = None
    largest_size = 0

    for clique in nx.find_cliques(graph):
        subgraph = graph.subgraph(clique)
        adj_matrix = nx.adjacency_matrix(subgraph).todense()

       
        clique_edges = np.sum(adj_matrix) // 2  

        
        size = len(clique) + clique_edges

        if size > largest_size:
            largest_clique = clique
            largest_size = size

    return largest_clique, largest_size


def clique_to_adj_matrix(graph, clique):
    subgraph = graph.subgraph(clique)
    return nx.adjacency_matrix(subgraph).todense()


def process(file_path):
    graphs = read_graphs_from_file(file_path)
    results = []
    
    for i, graph_matrix in enumerate(graphs):
        start_time = time.time()
        G = nx.MultiGraph()
        for u in range(len(graph_matrix)):
            for v in range(u, len(graph_matrix)):
                for _ in range(graph_matrix[u][v]):
                    G.add_edge(u, v)

        largest_clique, largest_clique_size = find_largest_clique(G)
        adj_matrix = clique_to_adj_matrix(G, largest_clique)
        end_time = time.time() 
        calculation_time_ms = (end_time - start_time) * 1000  
        matrix_str = f"Matrix {i + 1}:\n{np.array2string(graph_matrix, separator=', ')}\n"
        results.append(matrix_str)
        results.append(f"Graph {i+1}: Largest clique size: {largest_clique_size}\nAdjacency Matrix of the largest clique:\n{np.array_str(adj_matrix)}.\nCalculation Time: {calculation_time_ms:.2f} ms\n\n")
        
        
    return "\n".join(results)

