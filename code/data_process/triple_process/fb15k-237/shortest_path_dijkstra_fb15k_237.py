import time
import shutil
import os
Lnode = 14541

import heapq

def dijkstra(graph, start):
    # 初始化距离和前驱节点数组
    distances = [float('infinity') for node in range(Lnode)]
    distances[start] = 0
    predecessors = [-1 for node in range(Lnode)]
    
    # 使用优先队列来存储节点和对应的距离
    priority_queue = [(0, start)]
    
    # 用于跟踪已处理节点的集合
    processed_nodes = set()

    while priority_queue:
        # 弹出距离最小的节点
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # 如果节点已经处理过，则跳过
        if current_node in processed_nodes:
            continue
        
        # 标记当前节点为已处理
        processed_nodes.add(current_node)
        
        # 遍历当前节点的邻居
        for neighbor, weight in graph[current_node].items():
            if neighbor not in processed_nodes:
                # 计算通过当前节点到邻居节点的距离
                alternative_route = current_distance + weight
                # 如果找到更短的路径，则更新距离和前驱节点
                if alternative_route < distances[neighbor]:
                    distances[neighbor] = alternative_route
                    predecessors[neighbor] = current_node
                    # 将邻居节点和新的距离加入优先队列
                    heapq.heappush(priority_queue, (alternative_route, neighbor))
    
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

    for start_node in range(9999,10000):
        distances, predecessors = dijkstra(graph.copy(), start_node)
        print(distances)
        save_array_to_txt(distances,"/data/LLMKG/CTKG/data/fb15k-237/shortestdistance_table/"+str(start_node//100*100)+"-"+str((start_node//100+1)*100-1)+".txt")
        save_array_to_txt(predecessors,"/data/LLMKG/CTKG/data/fb15k-237/shortestpath_predecessor/"+str(start_node//100*100)+"-"+str((start_node//100+1)*100-1)+".txt")
        if start_node%10 == 0:
            print("cnt:",start_node)
    