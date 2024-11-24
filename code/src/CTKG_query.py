import numpy as np
import time
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
            row = list(map(float, line.strip().split('\t')))
            array.append(row)
    return array

def read_queries_from_fold(datapath:str, q_num:int, g_num:int):
    querypath = datapath + "/query/" + "query_" + str(q_num) + "_" + str(g_num) + "/"
    queryset = []
    for i in range(q_num):
        queryset.append(read_txt_to_array(querypath+str(q_num)+"_"+str(g_num)+"_"+str(i)+".txt"))
    return queryset

def center_entity(datapath:str, query:list, Lnode:int):
    t0 = time.time()
    shortest_distance_path = datapath + "/shortestdistance_table/"
    shortest_path_path = datapath + "/predecessor/"
    cache_D = {}
    cache_g = {}
    in_cache = []


    for gs in query:
        for g in gs:
            g = int(g)
            # if g//100*100 in in_cache:
            #     cache_g[g] = in_cache.index(g//100*100)
            # else:
            cache_g[g] = len(in_cache)
            cache_D[len(in_cache)] = read_txt_to_array(datapath+"/shortestdistance_table/"+str(g//100*100)+"-"+str(g//100*100+99)+".txt")[int(g-g//100*100)]
            in_cache.append(g//100*100)
    
    t1 = time.time()
    print("Cache Time:",t1 - t0)

    k_min = np.zeros((len(query),Lnode))
    g_min = np.zeros((len(query),Lnode))
    for i in range(len(query)):
        g_ = np.array([cache_D[cache_g[int(k)]] for k in query[i]])
        for j in range(Lnode):
            min_m = float("Infinity")
            min_m_idx = 0
            for m in range(len(g_[:,j])):
                if g_[:,j][m] < min_m:
                    min_m = g_[:,j][m]
                    min_m_idx = m
            k_min[i][j] = min_m
            g_min[i][j] = query[i][min_m_idx]

    
    # for gs in query:
    #     for g in gs:
    #         g = int(g)
    #         if g//100*100 in in_cache:
    #             cache_g[g] = in_cache.index(g//100*100)
    #         else:
    #             cache_g[g] = len(in_cache)
    #             cache_D[len(in_cache)] = read_txt_to_array(datapath+"/shortestdistance_table/"+str(g//100*100)+"-"+str(g//100*100+99)+".txt")
    #             in_cache.append(g//100*100)
    
    # t1 = time.time()
    # print("Cache Time:",t1 - t0)

    # k_min = [0]*14951
    # g_min = np.zeros((14951,len(query)))
    # for i in range(len(query)):
    #     g_ = (np.array([cache_D[cache_g[int(k)]][int(k-k//100*100)] for k in query[i]])).T
    #     for j in range(len(k_min)):
    #         k_min[j] = k_min[j] + min(g_[j])
    #         g_min[j][i] = query[i][int(np.argmin(g_[j]))]

    k_min = sum(np.array(k_min))
    print(len(k_min))
    idx = np.argmin(k_min)
    print(idx)
    g_min = g_min[:,idx]
    print("group keywords:",g_min)
    print("distance:",k_min[idx])
    if k_min[idx] == float("Infinity"):
        t2 = time.time()
        return t1-t0, t2-t1, k_min[idx], 0
    t3 = time.time()
    shortest_path_table = read_txt_to_array(datapath+"/shortestpath_predecessor/"+str(idx//100*100)+"-"+str(idx//100*100+99)+".txt")
    t4 = time.time()
    for g in g_min:
        getSP(idx, int(g), shortest_path_table[idx-idx//100*100])
    t2 = time.time()
    print("time:",t2-t1)
    return t1-t0, t2-t1, k_min[idx], t4-t3

def getSP(start, end, predecessor):
    path = []
    while start != end:
        path.append(end)
        end = int(predecessor[end])
    path.append(end)
    print(path)
    return path
        

if __name__ == '__main__':
    entity_size = {"fb15k":14951,"fb15k-237":14541,"lmdb":200240}
    datapath = "/data/LLMKG/CTKG/data/lmdb"
    tpc = []
    for g_num in [1]:
        queryset = read_queries_from_fold(datapath,200,g_num)
        with open(datapath+"/query/CTKG_exp_200_"+str(g_num)+"_.csv", "a") as f:
            i = 0
            for q in queryset[:20]:
                print(i,q)
                i = i + 1
                t_c, t_q, cost, tp = center_entity(datapath, q, entity_size["lmdb"])
                if tp > 0 :
                    tpc.append(tp)
                    print("SPtime:",sum(tpc)/len(tpc))
                f.write(str(t_c)+","+str(t_q)+","+str(cost)+"\n")
            f.close()



