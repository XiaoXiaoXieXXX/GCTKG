import numpy as np
import time
import heapq
from groupset import GroupSet


def read_txt_to_array(file_path: str):
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
            row = list(map(float, line.strip().split('\t')))
            array.append(row)
    return array


def read_queries_from_fold(datapath: str, q_num: int, g_num: int):
    querypath = datapath + "/query/" + "query_" + str(q_num) + "_" + str(g_num) + "/"
    queryset = []
    for i in range(q_num):
        queryset.append(read_txt_to_array(querypath + str(q_num) + "_" + str(g_num) + "_" + str(i) + ".txt"))
    return queryset


def find_center_groups(groups: list, DistTable: dict, Lnode:int):
    k_min = np.zeros((len(groups), Lnode))
    g_min = np.zeros((len(groups), Lnode))
    for i in range(len(groups)):
        g_ = np.array([DistTable[int(k)] for k in groups[i]])
        for j in range(Lnode):
            min_m = float("Infinity")
            min_m_idx = 0
            for m in range(len(g_[:, j])):
                if g_[:, j][m] < min_m:
                    min_m = g_[:, j][m]
                    min_m_idx = m
                elif g_[:, j][m] == min_m and m in groups[i]:
                    min_m = g_[:, j][m]
                    min_m_idx = m

            k_min[i][j] = min_m
            g_min[i][j] = groups[i][min_m_idx]

    k_min = sum(np.array(k_min))
    idx = np.argmin(k_min)
    g_min = g_min[:, idx]
    cost = k_min[idx]
    return g_min, idx, cost


def center_entity(graph, datapath: str, query: list, Lnode: int):
    t0 = time.time()
    shortest_distance_path = datapath + "/shortestdistance_table/"
    shortest_path_path = datapath + "/predecessor/"
    cache_D = {}

    for gs in query:
        for g in gs:
            g = int(g)
            cache_D[g] = read_txt_to_array(
                datapath + "/shortestdistance_table/" + str(g // 100 * 100) + "-" + str(g // 100 * 100 + 99) + ".txt")[
                int(g - g // 100 * 100)]

    t1 = time.time()
    t_cache = t1 - t0
    print("Finish cache!")

    g_min, idx, cost = find_center_groups(query, cache_D, Lnode)
    print("center:", idx)
    # print("group keywords:", g_min)
    cache_D = {int(g):cache_D[int(g)] for g in g_min}
    # print("distance:", cost)

    if cost == float("Infinity"):
        t2 = time.time()
        return t1 - t0, t2 - t1, cost, 0

    Q = []
    center_list = []
    path_list_center = []
    heapq.heappush(Q, GroupSet(g_min, idx, cost, None))

    while len(Q)>0:
        gpset = heapq.heappop(Q)
        if len(gpset.grouplist) == 0:
            continue
        if gpset.center == None:
            if gpset.newadd not in center_list:
                t_tmp = time.time()
                cache_D[gpset.newadd] = read_txt_to_array(
                    datapath + "/shortestdistance_table/" + str(gpset.newadd // 100 * 100) + "-" + str(
                        gpset.newadd // 100 * 100 + 99) + ".txt")[int(gpset.newadd - gpset.newadd // 100 * 100)]
                center_list.append(gpset.newadd)
                t_cache = t_cache + time.time() - t_tmp
            if len(gpset.grouplist) == 1:
                path_list_center.append([gpset.newadd, gpset.grouplist[0], cache_D[gpset.newadd][int(gpset.grouplist[0])]])

            else:
                gps = [[g] for g in gpset.grouplist]
                gps.append([gpset.newadd])
                _, ct, cost = find_center_groups(gps, cache_D, Lnode)
                if ct == gpset.newadd:
                    path_list_center.extend([[gpset.newadd, g, cache_D[gpset.newadd][int(g)]] for g in gpset.grouplist])

                else:
                    dist_c = cache_D[gpset.newadd][ct]
                    heapq.heappush(Q, GroupSet(gpset.grouplist, ct, cost - dist_c, None))
                    path_list_center.append([gpset.newadd, ct, dist_c])

        else:
            min_cost = float("Infinity")
            min_set = []
            min_set_ = []
            for nei in graph[gpset.center]:
                SET = []
                SET_ = []
                COST = graph[gpset.center][nei]
                for g in gpset.grouplist:
                    if cache_D[g][nei] <= cache_D[g][gpset.center]:
                        SET.append(g)
                        COST = COST + cache_D[g][nei]
                    else:
                        SET_.append(g)
                        COST = COST + cache_D[g][gpset.center]
                if COST < min_cost or (COST == min_cost and len(SET) < len(gpset.grouplist)):
                    min_cost = COST
                    min_set = SET
                    min_set_ = SET_
            if min_cost > gpset.cost:
                path_list_center.extend([[gpset.center, g, cache_D[g][gpset.center]] for g in gpset.grouplist])
            else:
                heapq.heappush(Q, GroupSet(min_set, None, gpset.cost, gpset.center))
                heapq.heappush(Q, GroupSet(min_set_, None, gpset.cost, gpset.center))

    cost = 0
    for p in path_list_center:
        cost = cost + p[2]

    t2 = time.time()
    print("time:", t2 - t0 - t_cache)
    print("path:",path_list_center)
    print("distance:", cost)
    print("group keywords:", g_min)
    print("Cache Time:", t_cache)
    return t_cache, t2 - t0 - t_cache, cost, t_cache


def getSP(start, end, predecessor):
    path = []
    while start != end:
        path.append(end)
        end = int(predecessor[end])
    path.append(end)
    print(path)
    return path


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


        

if __name__ == '__main__':
    entity_size = {"fb15k":14951,"fb15k-237":14541,"lmdb":200240}
    datapath = "/data/LLMKG/CTKG/data/fb15k-237"
    tpc = []
    graph = read_graph_from_file(datapath+"/train2id.txt")
    for g_num in [40]:
        queryset = read_queries_from_fold(datapath,200,g_num)
        with open(datapath+"/query/CTKGp_exp_200_"+str(g_num)+"_.csv", "a") as f:
            i = 0
            for q in queryset:
                print(i,q)
                i = i + 1
                t_c, t_q, cost, tp= center_entity(graph, datapath, q, entity_size["fb15k-237"])
                if tp > 0 :
                    tpc.append(tp)
                    print("SPtime:",sum(tpc)/len(tpc))
                f.write(str(t_c)+","+str(t_q)+","+str(cost)+"\n")
            f.close()
