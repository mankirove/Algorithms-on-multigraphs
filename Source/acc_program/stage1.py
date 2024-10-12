import numpy as np
import networkx as nx
import itertools
import time

import numpy as np

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
        
        num_vertices = G.number_of_nodes()
        num_edges = G.size()  
        graph_size = num_vertices + num_edges

        end_time = time.time() 
        calculation_time = (end_time - start_time)*1000
        matrix_str = f"Matrix {i + 1}:\n{np.array2string(graph_matrix, separator=', ')}\n"
        results.append(f"Graph  {i+1}: Vertices: {num_vertices}, Edges: {num_edges}, Size: {graph_size}")
        results.append(f"Calculation Time: {calculation_time:.4f} ms\n")
        results.append(matrix_str)

    return "\n".join(results)