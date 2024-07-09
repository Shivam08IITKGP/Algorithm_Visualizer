from cgi import test
import sys
import random
import networkx as nx
from sorting.quick_sort import visualize_quick_sort
from sorting.merge_sort import visualize_merge_sort
from sorting.bubble_sort import visualize_bubble_sort
from sorting.insertion_sort import visualize_insertion_sort
from graph.random_graph import generate_random_connected_directed_unweighted_graph_no_self_loops, \
    generate_random_connected_directed_graph_no_self_loops
from graph.Dijkstra import visualize_dijkstra
from graph.dfs import visualize_dfs
from graph.bfs import visualize_bfs
from graph.kruskal_mst import visualize_kruskal
from graph.prims_mst import visualize_prim
from graph.articulation_point import visualize_articulation_points
from graph.bridges import visualize_bridges
from graph.custom_graph_input import custom_graph_input_weighted, custom_graph_input_unweighted
from graph.random_traversal import visualize_random_traversal
from dp.knapsack_01 import visualize_knapsack_01
from dp.knapsack_duplicate import visualize_knapsack_duplicate
from dp.LCSubsequence import visualize_lcs
from dp.LCSubstring import visualize_lcsu
from trees.tree_level_order_traversal import visualize_level_order_traversal
from trees.ZigZagOrderTraversal import visualize_zig_zag_order_traversal
from trees.SegmentTree import SegmentTree
from strings.kmp import visualize_kmp_array
from strings.z_array import visualize_z_array
from strings.suffix_array import visualize_suffix_array_construction
import json

if __name__ == '__main__':
    algorithm = sys.argv[1]
    test_case_type = sys.argv[2]
    custom_input = sys.argv[3]
    output_file = sys.argv[4]
    result_data = {}

    if algorithm == "Dijkstra's Algorithm":
        if test_case_type == "Random":
            graph = generate_random_connected_directed_graph_no_self_loops(6, 10)
        else:
            graph = custom_graph_input_weighted(custom_input)
        distances, traversal_order = visualize_dijkstra(graph, output_file)
        result_data['distances'] = distances
        result_data['traversal_order'] = traversal_order

    elif algorithm == "DFS":
        if test_case_type == "Random":
            graph = generate_random_connected_directed_unweighted_graph_no_self_loops(6, 10)
        else:
            graph = custom_graph_input_unweighted(custom_input)
        traversal_order = visualize_dfs(graph, output_file)
        result_data['traversal_order'] = traversal_order

    elif algorithm == "BFS":
        if test_case_type == "Random":
            graph = generate_random_connected_directed_unweighted_graph_no_self_loops(6, 10)
        else:
            graph = custom_graph_input_unweighted(custom_input)
        traversal_order = visualize_bfs(graph, output_file)
        result_data['traversal_order'] = traversal_order

    elif algorithm == "Quick Sort":
        if test_case_type == "Random":
            array = random.sample(range(1, 100), 10)
        else:
            array = list(map(int, custom_input.split(',')))
        array = visualize_quick_sort(array, output_file)
        result_data['sorted_array'] = array

    elif algorithm == "Merge Sort":
        if test_case_type == "Random":
            array = random.sample(range(1, 100), 10)
        else:
            array = list(map(int, custom_input.split(',')))
        array = visualize_merge_sort(array, output_file)
        result_data['sorted_array'] = array

    elif algorithm == "Bubble Sort":
        if test_case_type == "Random":
            array = random.sample(range(1, 100), 10)
        else:
            array = list(map(int, custom_input.split(',')))
        array = visualize_bubble_sort(array, output_file)
        result_data['sorted_array'] = array

    elif algorithm == "Insertion Sort":
        if test_case_type == "Random":
            array = random.sample(range(1, 100), 10)
        else:
            array = list(map(int, custom_input.split(',')))
        array = visualize_insertion_sort(array, output_file)
        result_data['sorted_array'] = array

    elif algorithm == "Kruskal MST":
        if test_case_type == "Random":
            graph = generate_random_connected_directed_graph_no_self_loops(6, 10)
        else:
            graph = custom_graph_input_weighted(custom_input)
        mst = visualize_kruskal(graph, output_file)
        result_data['mst'] = [(u, v, mst[u][v]['weight']) for u, v in mst.edges()]

    elif algorithm == "Prims MST" or algorithm == "Prim MST":
        if test_case_type == "Random":
            graph = generate_random_connected_directed_graph_no_self_loops(6, 10)
        else:
            graph = custom_graph_input_weighted(custom_input)
        mst = visualize_prim(graph, output_file)
        result_data['mst'] = [(u, v, mst[u][v]['weight']) for u, v in mst.edges()]

    elif algorithm == "0/1 Knapsack":
        if test_case_type == "Random":
            weights = [1, 3, 4, 5]
            values = [10, 40, 50, 70]
            capacity = 8
        else:
            arrays = custom_input.split('\n')
            arrays[0].strip(' ')
            arrays[1].strip(' ')
            arrays[2].strip(' ')
            weights = list(map(int, arrays[0].split()))
            values = list(map(int, arrays[1].split()))
            capacity = int(arrays[2])

        max_value = visualize_knapsack_01(weights, values, capacity, output_file)
        result_data['max_value'] = max_value
        result_data['array'].append(weights)
        result_data['array'].append(values)

    elif algorithm == "Duplicate Knapsack":
        if test_case_type == "Random":
            weights = [1, 3, 4, 5]
            values = [10, 40, 50, 70]
            capacity = 8
        else:
            arrays = custom_input.split('\n')
            arrays[0].strip()
            arrays[1].strip()
            arrays[2].strip()
            weights = list(map(int, arrays[0].split()))
            values = list(map(int, arrays[1].split()))
            capacity = int(arrays[2])
            # print(f'Weights = {weights}')
            # print(f'Values = {values}')
            # print(f'Capacity = {capacity}')
        max_value = visualize_knapsack_duplicate(weights, values, capacity, output_file)
        result_data['max_value'] = max_value
        result_data['array'].append(weights)
        result_data['array'].append(values)

    elif algorithm == "Level Order Traversal":
        graph = {
            1: [2, 3],
            2: [4, 5],
            3: [6, 7],
            4: [],
            5: [],
            6: [],
            7: []
        }
        traversal = visualize_level_order_traversal(graph, output_file)
        result_data['traversal_order'] = traversal

    elif algorithm == "KMP":
        if test_case_type == "Random":
            text = "abababca"
        else:
            text = custom_input
        positions = visualize_kmp_array(text, output_file)
        result_data['positions'] = positions

    elif algorithm == "Z-Array":
        if test_case_type == "Random":
            text = "ababcababcabc"
        else:
            text = custom_input
        z_array = visualize_z_array(text, output_file)
        result_data['z_array'] = z_array

    elif algorithm == 'Bridges':
        if test_case_type == "Random":
            graph = nx.DiGraph()
            graph.add_edges_from([(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (1, 5), (5, 6), (6, 7), (7, 5)])
        else:
            graph = custom_graph_input_unweighted(custom_input)
        bridges = visualize_bridges(graph, output_file)
        result_data['bridges'] = bridges

    elif algorithm == 'Articulation Point':
        if test_case_type == "Random":
            graph = nx.DiGraph()
            graph.add_edges_from([(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (1, 5), (5, 6), (6, 7), (7, 5)])
        else:
            graph = custom_graph_input_unweighted(custom_input)
            line = custom_input.strip().split('\n')
            t = line[0].lower()
            t = t.strip()
            print(f'The first word is = {t}')
        articulation_points = visualize_articulation_points(graph, output_file)
        result_data['ap'] = articulation_points

    elif algorithm == 'Longest Common Subsequence':
        if test_case_type == "Random":
            A = "ABCBDAB"
            B = "BDCAB"
        else:
            arrays = custom_input.split('\n')
            A = arrays[0].strip()
            B = arrays[1].strip()
        string = visualize_lcs(A, B, output_file)
        result_data['string'] = string

    elif algorithm == 'Longest Common Substring':
        if test_case_type == "Random":
            A = "ABCBDAB"
            B = "BDCAB"
        else:
            arrays = custom_input.split('\n')
            A = arrays[0].strip()
            B = arrays[1].strip()
        string = visualize_lcsu(A, B, output_file)
        result_data['string'] = string

    elif algorithm == 'Longest Palindromic Subsequence':
        if test_case_type == "Random":
            A = "BBABCBCAB"
            B = A[::-1]
        else:
            A = custom_input.strip()
            B = A[::-1]
        string = visualize_lcs(A, B, output_file)
        result_data['string'] = string

    elif algorithm == 'Zig Zag Order Traversal':
        graph = {
            1: [2, 3],
            2: [4, 5],
            3: [6, 7],
            4: [],
            5: [],
            6: [],
            7: []
        }
        traversal_order = visualize_zig_zag_order_traversal(graph, output_file)
        result_data['traversal_order'] = traversal_order

    elif algorithm == 'Random Traversal':
        if test_case_type == "Random":
            graph = generate_random_connected_directed_unweighted_graph_no_self_loops(6, 10)
        else:
            graph = custom_graph_input_unweighted(custom_input)
        traversal_order = visualize_random_traversal(graph, output_file)
        result_data['traversal_order'] = traversal_order

    elif algorithm == 'Suffix Array':
        if test_case_type == "Random":
            text = "abababca"
        else:
            text = custom_input
        suffix_array = visualize_suffix_array_construction(text, output_file)
        result_data['suffix_array'] = suffix_array
        
    elif algorithm == 'Segment Tree':
        ans = list()     
        array = list()  
        print("Hello")
        if test_case_type == "Random":
            array=random.sample(range(1, 10), 5)
            segmenttree=SegmentTree(array)
            queries = [[2, 5, 5], [2, 4], [1, 4]]
            ans=segmenttree.visualize_segment_tree_operations(output_file=output_file)
        else:
            lines = custom_input.split('\n')
            lines[0] = lines[0].strip(' ')
            array = list(map(int, lines[0].split(',')))
            segmenttree = SegmentTree(array)
            queries = []
            print(type(queries))
            for query in lines[1:]:
                q = query.strip(' ')
                q = q.strip('\n')
                q = list(map(int, q.split(',')))
                queries.append(q)
            ans=segmenttree.visualize_segment_tree_operations(queries=queries, output_file=output_file)
        print(ans)
        print(test_case_type)
        print(array)
        result_data['sorted_array']=ans
        result_data['array']=array

    else:
        print(f"Algorithm {algorithm} not found")
        exit(1)

    result_data['algorithm'] = algorithm  # Add this line
    with open('result.json', 'w') as outfile:
        json.dump(result_data, outfile)
