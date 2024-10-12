import numpy as np
import networkx as nx
import itertools
import time
from math import ceil
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

 
def are_isomorphic(G1, G2):
   
    GM = nx.isomorphism.MultiGraphMatcher(G1, G2, edge_match=lambda e1, e2: e1 == e2)
    return GM.is_isomorphic()


def hamming_distance(graph1, graph2):
    
   
    max_vertices = max(graph1.shape[0], graph2.shape[0])
    size_difference = abs(graph1.shape[0] - graph2.shape[0])

   
    extended_graph1 = extend_graph(graph1, max_vertices)
    extended_graph2 = extend_graph(graph2, max_vertices)
   
    difference = np.sum(np.triu(extended_graph1) != np.triu(extended_graph2))
    difference= difference+size_difference
    return difference



def extend_graph(graph, new_size):
    current_size = graph.shape[0]
    if current_size == new_size:
        return graph
    else:
        
        extended_graph = np.zeros((new_size, new_size), dtype=graph.dtype)
        
        extended_graph[:current_size, :current_size] = graph
        return extended_graph


def calculate_all_hamming_distances(graphs):
    num_graphs = len(graphs)

    for i in range(num_graphs):
        for j in range(i + 1, num_graphs):
           
            extended_graph1 = extend_graph(graphs[i], max(len(graphs[i]), len(graphs[j])))
            extended_graph2 = extend_graph(graphs[j], max(len(graphs[i]), len(graphs[j])))

            
            if are_isomorphic(extended_graph1, extended_graph2):
                print(f"Graph {i + 1} and Graph {j + 1} are isomorphic.")
                distance = 0 
            else:
                
                distance = hamming_distance(extended_graph1, extended_graph2)

            print(f"Hamming Distance between Graph {i + 1} and Graph {j + 1}: {distance}")

def process(file_path):
    graphs = read_graphs_from_file(file_path)
    results = []
    
    for i in range(len(graphs)):
        for j in range(i + 1, len(graphs)):
            start_time = time.time()

            
            G1 = nx.MultiGraph()
            G2 = nx.MultiGraph()
            for u in range(len(graphs[i])):
                for v in range(len(graphs[i][u])):
                    if graphs[i][u][v] > 0:
                        G1.add_edges_from([(u, v)] * graphs[i][u][v])
            for u in range(len(graphs[j])):
                for v in range(len(graphs[j][u])):
                    if graphs[j][u][v] > 0:
                        G2.add_edges_from([(u, v)] * graphs[j][u][v])

         
            if are_isomorphic(G1, G2):
                distance = 0
                isomorphism_status = "are isomorphic"
                matrix_str1 = f"Matrix {i + 1}:\n{np.array2string(nx.convert_matrix.to_numpy_array(G1)/2, separator=', ')}\n"
                matrix_str2 = f"Matrix {j + 1}:\n{np.array2string(nx.convert_matrix.to_numpy_array(G2)/2, separator=', ')}\n"
                results.append(matrix_str1)
                results.append(matrix_str2)
            else:
                
                adj_matrix_G1 = nx.convert_matrix.to_numpy_array(G1)
                adj_matrix_G2 = nx.convert_matrix.to_numpy_array(G2)
                distance = hamming_distance(adj_matrix_G1, adj_matrix_G2)
                isomorphism_status = "are not isomorphic"
                matrix_str1 = f"Matrix {i + 1}:\n{np.array2string(adj_matrix_G1/2, separator=', ')}\n"
                matrix_str2 = f"Matrix {j + 1}:\n{np.array2string(adj_matrix_G2/2, separator=', ')}\n"
                results.append(matrix_str1)
                results.append(matrix_str2)

            end_time = time.time() 
            calculation_time_ms = (end_time - start_time) * 1000 
            
            results.append(f"Graph {i + 1} and Graph {j + 1} {isomorphism_status}. Hamming Distance: {distance}. Calculation Time: {calculation_time_ms:.2f} ms")

    return "\n".join(results)


def compare_two_graphs(graph1_matrix, graph2_matrix):
   
    G1 = nx.MultiGraph()
    G2 = nx.MultiGraph()
    result = []
    
    for i in range(len(graph1_matrix)):
        for j in range(len(graph1_matrix[i])):
            if graph1_matrix[i][j] > 0:
                G1.add_edges_from([(i, j)] * graph1_matrix[i][j])

    for i in range(len(graph2_matrix)):
        for j in range(len(graph2_matrix[i])):
            if graph2_matrix[i][j] > 0:
                G2.add_edges_from([(i, j)] * graph2_matrix[i][j])

    
    if are_isomorphic(G1, G2):
                distance = 0
                
    
    adj_matrix_G1 = nx.convert_matrix.to_numpy_array(G1)
    adj_matrix_G2 = nx.convert_matrix.to_numpy_array(G2)

    
    distance = hamming_distance(adj_matrix_G1, adj_matrix_G2)
    if are_isomorphic(G1, G2):
                distance = 0
                
    matrix_str1 = f"Matrix {1}:\n{np.array2string(adj_matrix_G1/2, separator=', ')}\n"
    matrix_str2 = f"Matrix {2}:\n{np.array2string(adj_matrix_G2/2, separator=', ')}\n"
    result.append(matrix_str1)
    result.append(matrix_str2)
    result.append(f"Graphs are {'isomorphic.Hamming Distance = 0 ' if are_isomorphic(G1, G2) else 'not isomorphic '}.\nHamming Distance: {distance}")
    return "\n".join(result)
    