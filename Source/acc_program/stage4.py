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

def find_maximal_common_subgraph(graph1, graph2):
    max_common_subgraph = None
    max_size = 0

    
    for sub_nodes in itertools.chain.from_iterable(itertools.combinations(graph1.nodes, r) for r in range(len(graph1.nodes)+1)):
        subgraph1 = graph1.subgraph(sub_nodes)

        is_common = all(any(nx.is_isomorphic(subgraph1, graph2.subgraph(sub_nodes2)) for sub_nodes2 in itertools.combinations(graph2.nodes, len(sub_nodes))))

        if is_common:
            size = len(sub_nodes)
            if size > max_size:
                max_common_subgraph = subgraph1
                max_size = size

    return max_common_subgraph

def find_maximal_common_subgraph(graph1, graph2):
    max_common_subgraph = None
    max_size = 0

    
    for sub_nodes in itertools.chain.from_iterable(itertools.combinations(graph1.nodes, r) for r in range(len(graph1.nodes)+1)):
        subgraph1 = graph1.subgraph(sub_nodes)

        
        is_common = any(nx.is_isomorphic(subgraph1, graph2.subgraph(sub_nodes2)) for sub_nodes2 in itertools.combinations(graph2.nodes, len(sub_nodes)))

        if is_common:
            size = len(sub_nodes)
            if size > max_size:
                max_common_subgraph = subgraph1
                max_size = size

    return max_common_subgraph


def compare_two_graphs(graph1_matrix, graph2_matrix):
    
    G1 = nx.Graph(graph1_matrix)
    print(G1)
    G2 = nx.Graph(graph2_matrix)
    print(G2)

    
    start_time = time.time()
    max_common_subgraph = find_maximal_common_subgraph(G1, G2)
    end_time = time.time()

    results = []
    if max_common_subgraph:
        calculation_time_ms = (end_time - start_time) * 1000
        results.append("Maximal Common Subgraph found:")
        results.append(f"Size: {len(max_common_subgraph.nodes())}")
        results.append(f"Adjacency Matrix:\n{np.array_str(nx.adjacency_matrix(max_common_subgraph).todense())}")
        results.append(f"Calculation Time: {calculation_time_ms:.4f} ms\n")
    else:
        results.append("No common subgraph found between the two graphs.")
        results.append(f"Calculation Time: {calculation_time_ms:.4f} ms\n")

    return "\n".join(results)

def process(file_path):
    start_time = time.time()
    graphs = read_graphs_from_file(file_path)
    nx_graphs = [nx.Graph(g) for g in graphs]

    
    max_common_subgraph = None
    max_size = 0

    
    for i in range(len(nx_graphs)):
        for j in range(i + 1, len(nx_graphs)):
            common_subgraph = find_maximal_common_subgraph(nx_graphs[i], nx_graphs[j])
            if common_subgraph and len(common_subgraph.nodes) > max_size:
                max_common_subgraph = common_subgraph
                max_size = len(common_subgraph.nodes)

    
    results = []
    end_time = time.time() 
    

    if max_common_subgraph:
        calculation_time_ms = (end_time - start_time) * 1000
        results.append("Maximal Common Subgraph among all graphs:")
        results.append(f"Size: {max_size}")
        results.append(f"Adjacency Matrix:\n{np.array_str(nx.adjacency_matrix(max_common_subgraph).todense())}")
        results.append(f"Calculation Time: {calculation_time_ms:.4f} ms\n")
        
    else:
        results.append("No common subgraph found among all graphs.")
        results.append(f"Calculation Time: {calculation_time_ms:.4f} ms\n")

    return "\n".join(results)
