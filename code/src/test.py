import time
import numpy as np
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

def getSP(start, end, predecessor):
    path = []
    while start != end:
        path.append(end)
        end = int(predecessor[start][end])
    path.append(end)
    print(path)
    return path

t0 = time.time()
# gs = [[0,1,2],[3,5,7],[8,4,10],[23,35,67]]
gs = [[0,1,2],[3,5,7],[8,4,10],[23,35,67],[44,55,66],[64,65,76],[77,78,79],[71,62,33,24]]
shortest_distance_table = read_txt_to_array("G:/code/table/0-99.txt")
k_min = [0]*14951
g_min = np.zeros((14951,len(gs)))
for j in range(len(gs)):
    g_ = (np.array(shortest_distance_table)[gs[j]]).T
    for i in range(len(k_min)):
        k_min[i] = k_min[i] + min(g_[i])
        g_min[i][j] = gs[j][int(np.argmin(g_[i]))]

idx = np.argmin(k_min)
print(idx)
print("group keywords:",g_min[idx])
print("distance:",k_min[idx])
shortest_path_table = read_txt_to_array("G:/code/predecessor/0-99.txt")
for g in g_min[idx]:
    getSP(idx, int(g), shortest_path_table)
t1 = time.time()
print("time:",t1-t0)
