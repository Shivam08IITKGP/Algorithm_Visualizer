import networkx as nx


def custom_graph_input_weighted(data):
    lines = data.strip().split('\n')
    a = lines[0]
    a = a.lower()
    a = a.strip("\n")
    b = a.strip("\n")
    c = b.strip(' ')
    c = c.strip()
    if c == "directed":
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    print(f'This is a {c} graph')
    for line in lines[1:]:
        u, v, w = map(int, line.split())
        G.add_edge(u, v, weight=w)
        if c == 'undirected':
            G.add_edge(v, u, weight=w)
    return G


def custom_graph_input_unweighted(data):
    lines = data.strip().split('\n')
    a = lines[0]
    a = a.lower()
    a = a.strip("\n")
    b = a.strip("\n")
    c = b.strip(' ')
    c = c.strip()
    if c == "directed":
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    print(f'This is a {c} graph')
    for line in lines[1:]:
        u, v = map(int, line.split())
        G.add_edge(u, v)
        if c == 'undirected':
            G.add_edge(v, u)
    return G
