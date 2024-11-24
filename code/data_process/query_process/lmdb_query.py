import numpy as np

def generate_arrays(datasize, q_num, g_num):
    # Generate q_num 2D arrays
    arrays = []
    for _ in range(q_num):
        # For each array, generate g_num rows
        rows = []
        for _ in range(g_num):
            # Generate a random number n from 1 to 10 following normal distribution
            n = int(np.random.normal(loc=5.5, scale=2.5))  # mean=5.5, std=2.5
            n = max(1, min(n, 10))  # ensure n is between 1 and 10

            # Generate n random integers m from 0 to datasize-1 following uniform distribution
            m_values = np.random.choice(range(datasize), size=n, replace=False)

            rows.append(m_values)
        arrays.append(rows)
    return arrays

def queries_id2text(query_data, dataset_path:str, q_num:int, g_num:int):
    for i in range(len(query_data)):
        save_array_to_txt(query_data[i], dataset_path + "/query/query_" + str(q_num) + "_" + str(g_num) + "/" + str(q_num) + "_" + str(g_num) + "_" + str(i) + ".txt")

def save_array_to_txt(array:list, file_path:str):
    """
    Save a two-dimensional array to a text file.
    Parameters:
    array: A two-dimensional array.
    file_path: The path where the file will be saved.
    """
    with open(file_path, 'w') as file:
        for row in array:
            file.write('\t'.join(map(str, row)) + '\n')

if __name__ == '__main__':
    fb15k_file_path = "/data/LLMKG/CTKG/data/fb15k/"
    fb15k_237_file_path = "/data/LLMKG/CTKG/data/fb15k-237/"
    lmdb_file_path = "/data/LLMKG/CTKG/data/lmdb/"
    entity_size = {"fb15k":14951,"fb15k-237":14541,"lmdb":200240}
    # id2text(fb15k_file_path,"entity")
    # id2text(fb15k_file_path,"relation")
    for g_num in [1]:
        queries_id2text(generate_arrays(entity_size["lmdb"], 200, g_num), lmdb_file_path, 200, g_num)
