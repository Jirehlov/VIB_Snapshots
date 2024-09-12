import json
import re
from collections import defaultdict, deque
import sys
import time
def load_names(file, key_prefix, name_extractor):
    with open(file, 'r', encoding='utf-8') as f:
        return {f"{key_prefix}_{data['id']}": name_extractor(data) for line in f for data in [json.loads(line)]}
def extract_name(data):
    match = re.search(r'\|简体中文名= ([^\r\n]+)', data.get('infobox', ''))
    if match: return match.group(1)
    name_cn = data.get('name_cn')
    if name_cn: return name_cn
    return data.get('name', '')
def read_jsonlines_to_graph(files):
    graph = defaultdict(set)
    def add_edge(node1, node2):
        graph[node1].add(node2)
        graph[node2].add(node1)
    for file in files:
        with open(file, 'r') as f:
            for data in map(json.loads, f):
                ids = {
                    's': f"s_{data['subject_id']}" if 'subject_id' in data else None,
                    'r': f"s_{data['related_subject_id']}" if 'related_subject_id' in data else None,
                    'p': f"p_{data['person_id']}" if 'person_id' in data else None,
                    'c': f"c_{data['character_id']}" if 'character_id' in data else None,
                }
                if ids['s'] and ids['r']: add_edge(ids['s'], ids['r'])
                if ids['c'] and ids['s']: add_edge(ids['c'], ids['s'])
                if ids['c'] and ids['p']: add_edge(ids['p'], ids['c'])
                if ids['p'] and ids['s'] and 'subject-persons.jsonlines' in file:
                    add_edge(ids['p'], ids['s'])
    return graph
def bfs_shortest_path(graph, start, goal, island):
    if start == goal: return 0, [start]
    if start not in island or goal not in island: return -1, []
    queue, visited = deque([(start, [start])]), set()
    while queue:
        node, path = queue.popleft()
        if node in visited: continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor == goal: return len(path), path + [goal]
            if neighbor not in visited and neighbor in island:
                queue.append((neighbor, path + [neighbor]))
    return -1, []
def bfs_longest_path_from_node(graph, start, island):
    queue, visited, max_steps, longest_path = deque([(start, [start])]), {start}, -1, []
    while queue:
        node, path = queue.popleft()
        if len(path) > max_steps:
            max_steps, longest_path = len(path), path
        for neighbor in graph[node]:
            if neighbor not in visited and neighbor in island:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return max_steps - 1, longest_path
def find_longest_shortest_path(graph, names, islands):
    max_steps, longest_path = -1, []
    for island in islands:
        start_node = next(iter(island))
        current_time = time.time()
        start_time = time.time()
        max_distance_node = None
        max_distance = -1
        queue = deque([(start_node, 0)])
        visited = {start_node}
        while queue:
            node, distance = queue.popleft()
            if distance > max_distance:
                max_distance = distance
                max_distance_node = node
            for neighbor in graph[node]:
                if neighbor not in visited and neighbor in island:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        queue = deque([(max_distance_node, [max_distance_node])])
        visited = {max_distance_node}
        while queue:
            node, path = queue.popleft()
            if len(path) > max_steps:
                max_steps = len(path)
                longest_path = path
                print(f"\n找到最长最短步数为{max_steps - 1}的路径:")
                print_path(longest_path, names)
            for neighbor in graph[node]:
                if neighbor not in visited and neighbor in island:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
    return max_steps - 1, longest_path
def find_islands(graph):
    visited = set()
    islands = []
    def dfs(node):
        stack, island = [node], set()
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                island.add(current)
                stack.extend(graph[current] - visited)
        return island
    for node in graph:
        if node not in visited:
            islands.append(dfs(node))
    return islands
def parse_input(input_type, input_id):
    return f"{input_type[1]}_{input_id}"
def print_path(path, names):
    for node in path:
        node_type, node_id = node.split("_")
        node_label = {"s": "条目", "p": "人物", "c": "角色"}.get(node_type, '')
        print(f"{node_id}, {node_label}, {names.get(node, '')}")
def main():
    files = ['subject-relations.jsonlines', 'subject-persons.jsonlines', 'subject-characters.jsonlines', 'person-characters.jsonlines']
    print("图加载中")
    graph = read_jsonlines_to_graph(files)
    print("名称加载中")
    names = {**load_names('subject.jsonlines', 's', extract_name), **load_names('person.jsonlines', 'p', extract_name), **load_names('character.jsonlines', 'c', extract_name)}
    print("连通分量计算中")
    islands = sorted(find_islands(graph), key=len)
    while True:
        command = input("\n\n请选择功能或输入节点：\n-s 指定subject\n-p 指定person\n-c 指定character\nisland 显示所有连通分量\nlongest 找到最长的最短路径\nexit 退出\n请输入命令: ").strip()
        if command == "exit": break
        args = command.split()
        if len(args) == 0: continue
        if args[0] == "island":
            print("连通分量的节点数量（升序排列）：")
            for i, island in enumerate(islands, 1):
                node = next(iter(island))
                print(f"连通分量{i}: {len(island)} 个节点, 一个节点示例: {node}, 名称: {names.get(node, 'Unknown')}")
        elif args[0] == "longest":
            max_steps, _ = find_longest_shortest_path(graph, names, islands)
            print(f"\n最长的最短路径长度为{max_steps}步" if max_steps != -1 else "\n不存在最长的最短路径")
        elif len(args) == 2:
            start_node = parse_input(args[0], args[1])
            for island in islands:
                if start_node in island:
                    max_steps, path = bfs_longest_path_from_node(graph, start_node, island)
                    if max_steps != -1:
                        print(f"\n从节点{start_node}出发的最长路径长度为：{max_steps}\n路径：")
                        print_path(path, names)
                    else:
                        print(f"\n从节点{start_node}出发没有找到路径")
                    break
            else:
                print(f"\n节点{start_node}不属于任何连通分量")
        elif len(args) == 4:
            start_node, goal_node = parse_input(args[0], args[1]), parse_input(args[2], args[3])
            for island in islands:
                if start_node in island and goal_node in island:
                    steps, path = bfs_shortest_path(graph, start_node, goal_node, island)
                    if steps != -1:
                        print(f"\n从{start_node}到{goal_node}的最短路径长度为：{steps}步\n路径：")
                        print_path(path, names)
                    else:
                        print(f"\n在{start_node}与{goal_node}之间不存在路径")
                    break
            else:
                print(f"\n在{start_node}与{goal_node}之间不存在路径")
        else:
            print("\n无效的命令。请确保输入1个节点（寻找最长路径）或2个节点（寻找最短路径）。")
if __name__ == "__main__":
    main()
