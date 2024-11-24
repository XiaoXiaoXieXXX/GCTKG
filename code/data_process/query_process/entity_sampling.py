import random
import json

def id2text(file_path:str,file_type:str):
    """
    Returns id2text file.
    Parameters:
    file_type: "entity" or "relation"
    """
    entity_to_text = {}
    with open(file_path + file_type + '2text.txt', 'r', encoding='utf-8') as file:
        for line in file:
            entity, text = line.strip().split('\t')
            entity_to_text[entity] = text

    id_to_text = {}

    with open(file_path + file_type + '2id.txt', 'r', encoding='utf-8') as file:
        for line in file:
            entity, entity_id = line.strip().split('\t')
            if entity in entity_to_text:  
                id_to_text[entity_id] = entity_to_text[entity]

    with open(file_path + file_type + '_id2text.txt', 'w', encoding='utf-8') as file:
        for entity_id, text in id_to_text.items():
            file.write(f'{entity_id}\t{text}\n')
        file.close()


def entity_sampling(file_path:str, entity_size:int,q_num:int,g_num:int):
    """
    Returns constructed queries.
    Parameters:
    q_num: the number of queries for fb15k dataset
    g_num: the number of groups for key words in a query (random number from 0 to g_num)
    """
    queries_entities_id = []
    for i in range(q_num):
        single_query = []
        for j in range(g_num):
            entity_id_random = random.randint(0, entity_size-1)
            while entity_id_random in single_query:
                entity_id_random = random.randint(0, entity_size-1)
            single_query.append(entity_id_random)    
        queries_entities_id.append(single_query)
    print(file_path + "query/" + str(q_num) + "_" + str(g_num) + "_queries2id.txt")
    save_array_to_txt(queries_entities_id, file_path + "query/" + str(q_num) + "_" + str(g_num) + "_queries2id.txt")

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

def queries_id2text(dataset_path:str, q_num:int, g_num:int):
    """
    Convert query to its id and final groups.

    Parameters:
    dataset_path: The path of the dataset.
    q_num: The number of queries.
    g_num: The number of groups.

    Returns:
    """
    threshold = 0.8
    queries_entities_id = read_txt_to_array(dataset_path + "query/" + str(q_num) + "_" + str(g_num) + "_queries2id.txt")
    id_to_text = {}
    with open(dataset_path + 'entity_id2text.txt', 'r', encoding='utf-8') as file:
        for line in file:
            id, text = line.strip().split('\t')
            id_to_text[int(id)] = text
    queries_groups = []
    for query in queries_entities_id:
        print(query)
        query_group = []
        for keyword in query:
            group = {"\"" + str(keyword) + "\"":{}}
            keyword_text = id_to_text[keyword]
            for id in range(len(id_to_text)):
                if longest_common_substring_similarity(keyword_text, id_to_text[id]) >= threshold:
                    group["\"" + str(keyword) + "\""]["\"" + str(id) + "\""] = "\"" + id_to_text[id] + "\""
            query_group.append(group.copy())
        print(query_group)
        queries_groups.append(query_group.copy())
    with open(dataset_path + "/query/" + str(q_num) + "_" + str(g_num) + '_groups.json', 'w', encoding='utf-8') as file:
        file.write(str(queries_groups).replace("\'","").replace("\\","\'"))
        file.close()
    with open(dataset_path + "/query/" + str(q_num) + "_" + str(g_num) + '_groups.json', 'r', encoding='utf-8') as file:
        query_data = json.load(file)
    for i in range(len(query_data)):
        query_ids = []
        for keywords in query_data[i]:
            group_ids = [value for value in list(keywords.values())[0].keys()]
            query_ids.append(group_ids)
            save_array_to_txt(query_ids, dataset_path + "/query/query_" + str(q_num) + "_" + str(g_num) + "/" + str(q_num) + "_" + str(g_num) + "_" + str(i) + ".txt")
        print(query_ids)

def longest_common_substring(s1, s2):
    """
    longest common substring similarity for two string.

    Parameters:
    s1, s2: string that need to compute similarity.

    Returns:
    float 0-1 for higher value, higher similarity
    """
    m = len(s1)
    n = len(s2)
    L = [[0] * (n + 1) for i in range(m + 1)]
    length = 0
    end_index_s1 = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
                if L[i][j] > length:
                    length = L[i][j]
                    end_index_s1 = i
            else:
                L[i][j] = 0

    lcs = s1[end_index_s1 - length: end_index_s1]
    return lcs, length

def longest_common_substring_similarity(s1, s2):
    _, length = longest_common_substring(s1, s2)
    return length / len(s1)



if __name__ == '__main__':
    fb15k_file_path = "/data/LLMKG/CTKG/data/fb15k/"
    fb15k_237_file_path = "/data/LLMKG/CTKG/data/fb15k-237/"
    lmdb_file_path = "/data/LLMKG/CTKG/data/lmdb/"
    entity_size = {"fb15k":14951,"fb15k-237":14541,"lmdb":200240}
    # id2text(fb15k_file_path,"entity")
    # id2text(fb15k_file_path,"relation")
    for g_num in [10,20,30,40]:
        entity_sampling(fb15k_237_file_path, entity_size["fb15k-237"], 200, g_num)
        queries_id2text(fb15k_237_file_path, 200, g_num)

