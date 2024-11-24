import json
import sys
import time

Lnode = 14951
# Lnode = 14541
# Lnode = 200240

import heapq

def getD(v, u, LV):
    set1 = set(list(LV[str(v)].keys()))
    set2 = set(list(LV[str(u)].keys()))
    list1 = list(set1&set2)
    if len(list1) == 0:
        return float("infinity")
    else:
        min_id = min(list1, key=lambda h:LV[u][h][0]+LV[v][h][0])
        return LV[u][min_id][0]+LV[v][min_id][0]


def dijkstra(graph):
    V = {node:len(graph[node]) for node in graph}
    Vbc = list(dict(sorted(V.items(), key=lambda item: item[1], reverse=True)).keys())
    LV = {node:{node:(float("infinity"),node)} for node in range(Lnode)}
    cnt = 0

    for vi in Vbc:
        cnt += 1
        visited = [0 for node in range(Lnode)]
        distances = [float('infinity') for node in range(Lnode)]
        distances[vi] = 0

        priority_queue = [(0, vi)]

        while priority_queue:
            
            u_distance, u_node = heapq.heappop(priority_queue)
            visited[u_node] = 1

            if u_distance <= getD(vi, u_node, LV):
                LV[u_node][vi] = (u_distance,vi)
                
                for w, weight in graph[u_node].items():
                    if visited[w] == 0:
                        if distances[u_node] + 1 < getD(vi, w, LV):
                            distances[w] = distances[u_node] + 1
                            LV[w][vi] = (distances[w], u_node)
                            heapq.heappush(priority_queue, (int(distances[w]), w))

        print("\r", end="")
        print("Processing: {}%: ".format(cnt/Lnode*100), "▓" * (cnt // (2*Lnode//100)), end="")
        sys.stdout.flush()
        time.sleep(0.05)
    return LV


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


def save_array_to_txt(array: list, file_path: str):
    """
    Save a two-dimensional array to a text file.
    Parameters:
    array: A two-dimensional array.
    file_path: The path where the file will be saved.
    """
    with open(file_path, 'a') as file:
        file.write('\t'.join(map(str, array)) + '\n')
        file.close()

def HL_distance_path(HL:dict, u:int, v:int):
    u = str(u)
    v = str(v)
    u_d = HL[str(u)]
    v_d = HL[str(v)]
    U_ = set(u_d.keys())
    V_ = set(v_d.keys())
    UV_ = list(U_&V_)
    d_min = float("infinity")
    h_min = None
    for h in UV_:
        d = u_d[h][0] + v_d[h][0]
        if d < d_min:
            d_min = d
            h_min = h
    if d_min == float("infinity"):
        return float("infinity"), None
    P = [h_min]
    y = u
    while y != h_min:
        p = str(HL[y][h_min][1])
        P.append(p)
        y = p
    y = v
    while y != h_min:
        p = str(HL[y][h_min][1])
        P.append(p)
        y = p
    return d_min

if __name__ == '__main__':
    # graph = read_graph_from_file("train2id.txt")
    # LV = dijkstra(graph.copy())
    # with open('HL.json', 'w') as f:
    #     json.dump(LV, f)
    with open('/data/LLMKG/CTKG/data/fb15k/HL.json', 'r') as f:
        data = json.load(f)
        f.close()
    D = HL_distance_path(data,7785, 4)
    print(D)
