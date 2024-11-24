import numpy as np
import json
import time

# Lnode = 14951
# Lnode = 14541
Lnode = 200240

def getD(v, u, LV):
    u = str(u)
    v = str(v)
    set1 = set(list(LV[v].keys()))
    set2 = set(list(LV[u].keys()))
    list1 = list(set1&set2)
    if len(list1) == 0:
        return float("infinity")
    else:
        min_id = min(list1, key=lambda h:LV[u][h][0]+LV[v][h][0])
        return LV[u][min_id][0]+LV[v][min_id][0]

def keykg(HL, query):
    t0 = time.time()
    # print(query)
    M = np.zeros((len(query)-1, Lnode)).tolist()
    for i in range(1, len(query)):
        for j in range(Lnode):
            hi = {-1:float("Infinity")}
            for q in query[i]:
                q = str(q)
                if str(j) in HL[q] and str(HL[q][str(j)][0]) != "Infinity" and HL[q][str(j)][0] < list(hi.values())[0]:
                    hi = {q:HL[q][str(j)][0]}
                    if -1 in hi:
                        del hi[-1]
            if -1 in hi:
                M[i-1][j] = None
            else:
                M[i-1][j] = hi
    # print(M)
    U = [[] for i in range(len(query[0]))]
    W = [0 for i in range(len(query[0]))]
    for L in range(len(query[0])):
        v1 = query[0][L]
        U[L].append(str(v1))
        for i in range(1, len(query)):
            vi = None
            disti = float("Infinity")
            for hj in HL[str(v1)]:
                hj = int(hj)
                print(hj, M[i-1][hj])
                if M[i-1][hj]:
                    d = getD(v1, hj, HL) + list(M[i-1][hj].values())[0]
                    if d < disti:
                        disti = d
                        vi = list(M[i-1][hj].keys())[0]
            W[L] = W[L] + disti
            U[L].append(vi)
    W_min = min(W)
    if W_min == float("Infinity"):
        t1 = time.time()
        return t1-t0, W_min
    Ux = U[W.index(W_min)]
    Mu = {u:HL[str(u)] for u in Ux}
    Tu = [0 for u in Ux]
    Pu = [None for u in Ux]
    Ux = list(Ux)
    for i in range(len(Ux)):
        Tu[i] = sum([getD(Ux[i], v, Mu) for v in Ux])
        Pu[i] = [HL_distance_path(Mu, Ux[i], v) for  v in Ux]
    
    t2 = time.time()    
    return t2-t0, min(Tu)

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
    return P

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

def read_txt_to_array(file_path:str):
    """
    Read a text file and convert it to a two-dimensional integer array.

    Parameters:
    file_path: The path of the file to be read.

    Returns:
    A two-dimensional integer array.
    """
    array = []
    with open(file_path, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split('\t')))
            array.append(row)
    return array

def read_queries_from_fold(datapath:str, q_num:int, g_num:int):
    querypath = datapath + "/query/" + "query_" + str(q_num) + "_" + str(g_num) + "/"
    queryset = []
    for i in range(q_num):
        queryset.append(read_txt_to_array(querypath+str(q_num)+"_"+str(g_num)+"_"+str(i)+".txt"))
    return queryset

if __name__ == '__main__':
    datapath = "/data/LLMKG/CTKG/data/lmdb"
    with open(datapath + '/HL.json', 'r') as f:
        HL = json.load(f)
        f.close()
    for g_num in [1]:
        queryset = read_queries_from_fold(datapath,200,g_num)
        with open(datapath+"/query/KeyKG_exp_200_"+str(g_num)+".csv", "a") as f:
            i = 0
            for q in queryset[:50]:
                print(i,q)
                i = i + 1
                t, cost = keykg(HL, q)
                f.write(str(t)+","+str(cost)+"\n")
            f.close()
