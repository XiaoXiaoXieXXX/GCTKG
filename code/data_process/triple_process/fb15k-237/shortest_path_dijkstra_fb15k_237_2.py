import time
import shutil
import os
Lnode = 14541

def dijkstra(graph, start):
    distances = [float('infinity') for node in range(Lnode)]
    distances[start] = 0
    predecessors = [-1 for node in range(Lnode)]

    while graph:
        current_node = min(graph, key=lambda node: distances[node])
        
        neighbors = graph[current_node]
        for neighbor, weight in neighbors.items():
            alternative_route = distances[current_node] + weight
            if alternative_route < distances[neighbor]:
                distances[neighbor] = alternative_route
                predecessors[neighbor] = current_node
        
        graph.pop(current_node)
    
    return distances, predecessors

def read_graph_from_file(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                node1, edge_id, node2 = parts
                node1, node2, edge_id = int(node1), int(node2), int(edge_id)
                if node1 not in graph:
                    graph[node1] = {}
                if node2 not in graph:
                    graph[node2] = {}
                graph[node1][node2] = 1
                graph[node2][node1] = 1
    return graph

def save_array_to_txt(array:list, file_path:str):
    """
    Save a two-dimensional array to a text file.
    Parameters:
    array: A two-dimensional array.
    file_path: The path where the file will be saved.
    """
    with open(file_path, 'a') as file:
        file.write('\t'.join(map(str, array)) + '\n')
        file.close()



if __name__ == '__main__':
    file_path = '/data/LLMKG/CTKG/data/fb15k-237/train2id.txt'
    # file_path = '/data/LLMKG/CTKG/code/data_process/triple_process/test.txt'
    table_path = "/data/LLMKG/CTKG/data/fb15k-237/shortestpath_table/"
    # shutil.rmtree(table_path)
    # os.mkdir(table_path)
    graph = read_graph_from_file(file_path)

    for start_node in range(5000,9999):
        distances, predecessors = dijkstra(graph.copy(), start_node)
        print(distances)
        save_array_to_txt(distances,"/data/LLMKG/CTKG/data/fb15k-237/shortestdistance_table/"+str(start_node//100*100)+"-"+str((start_node//100+1)*100-1)+".txt")
        save_array_to_txt(predecessors,"/data/LLMKG/CTKG/data/fb15k-237/shortestpath_predecessor/"+str(start_node//100*100)+"-"+str((start_node//100+1)*100-1)+".txt")
        if start_node%10 == 0:
            print("cnt:",start_node)
    