import random

def read_knowledge_graph(file_path):
    knowledge_graph = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            e1, r, e2 = line.strip().split()
            if e1 not in knowledge_graph:
                knowledge_graph[e1] = set()
            if e2 not in knowledge_graph:
                knowledge_graph[e2] = set()
            knowledge_graph[e1].add((r, e2))
            knowledge_graph[e2].add((r, e1))  # 假设关系是无向的
    return knowledge_graph

def calculate_degree(graph):
    degree = {node: len(edges) for node, edges in graph.items()}
    return degree

def sample_connected_subgraph(graph, n, m):
    degree = calculate_degree(graph)
    # 保留度数最大的m个节点
    top_m_nodes = sorted(degree, key=degree.get, reverse=True)[:m]
    # 确保图中有足够的节点
    if len(graph) < n:
        raise ValueError("The graph does not have enough nodes.")
    
    # 选择一个随机起点，优先从度数大的节点开始
    start_node = random.choice(top_m_nodes)
    visited = set()
    stack = [start_node]

    # 使用DFS来找到连通子图
    while stack and len(visited) < n:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend([edge[1] for edge in graph[node] if edge[1] not in visited])

    # 确保连通子图至少有n个节点
    if len(visited) < n:
        raise ValueError("Could not find a connected subgraph with at least {} nodes.".format(n))

    # 确保度数大的m个节点都在子图中
    for node in top_m_nodes:
        if node not in visited:
            visited.add(node)
            stack.append(node)
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    stack.extend([edge[1] for edge in graph[node] if edge[1] not in visited])

    # 构建采样后的连通子图的三元组列表
    subgraph_triples = []
    for node in visited:
        for r, neighbor in graph[node]:
            if neighbor in visited:
                subgraph_triples.append((node, r, neighbor))

    return subgraph_triples

# 使用示例
input_file_path = '/data/LLMKG/CTKG/data/lmdb/train2id.txt'
output_file_path = 'knowledge_graph2.txt'
n = 2000  # 需要的节点数量
m = 100   # 需要保留的度数大的节点数量
graph = read_knowledge_graph(input_file_path)
subgraph_triples = sample_connected_subgraph(graph, n, m)

# 按输入格式打印采样后的连通子图
e = []
with open(output_file_path,"a") as f:
    for triple in subgraph_triples:
        if set((triple[0],triple[2])) not in e:
            e.append(set((triple[0],triple[2])))
            f.write(f"{triple[0]}\t{triple[1]}\t{triple[2]}\n")
