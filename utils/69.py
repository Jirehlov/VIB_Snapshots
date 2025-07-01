import json
import re
from collections import defaultdict, deque
import sys
position_map = {1: '原作', 2: '导演', 3: '脚本', 4: '分镜', 5: '演出', 6: '音乐', 7: '人物原案', 8: '人物设定', 9: '构图', 10: '系列构成', 11: '美术监督', 13: '色彩设计', 14: '总作画监督', 15: '作画监督', 16: '机械设定', 17: '摄影监督', 18: '监修', 19: '道具设计', 20: '原画', 21: '第二原画', 22: '动画检查', 23: '助理制片人', 24: '制作助理', 25: '背景美术', 26: '色彩指定', 27: '数码绘图', 28: '剪辑', 29: '原案', 30: '主题歌编曲', 31: '主题歌作曲', 32: '主题歌作词', 33: '主题歌演出', 34: '插入歌演出', 35: '企画', 36: '企划制作人', 37: '制作管理', 38: '宣传', 39: '录音', 40: '录音助理', 41: '系列监督', 42: '製作', 43: '设定', 44: '音响监督', 45: '音响', 46: '音效', 47: '特效', 48: '配音监督', 49: '联合导演', 50: '背景设定', 51: '补间动画', 52: '执行制片人', 53: '助理制片人', 54: '制片人', 55: '音乐助理', 56: '制作进行', 57: '演员监督', 58: '总制片人', 59: '联合制片人', 60: '台词编辑', 61: '后期制片协调', 62: '制作助理', 63: '制作', 64: '制作协调', 65: '音乐制作', 66: '特别鸣谢', 67: '动画制作', 69: 'CG 导演', 70: '机械作画监督', 71: '美术设计', 72: '副导演', 73: 'OP・ED 分镜', 74: '总导演', 75: '3DCG', 76: '制作协力', 77: '动作作画监督', 80: '监制', 81: '协力', 82: '摄影', 83: '制作进行协力', 84: '设定制作', 85: '音乐制作人', 86: '3DCG 导演', 87: '动画制片人', 88: '特效作画监督', 89: '主演出', 90: '作画监督助理', 91: '演出助理', 92: '主动画师', 1001: '开发', 1002: '发行', 1003: '游戏设计师', 1004: '剧本', 1005: '美工', 1006: '音乐', 1007: '关卡设计', 1008: '人物设定', 1009: '主题歌作曲', 1010: '主题歌作词', 1011: '主题歌演出', 1012: '插入歌演出', 1013: '原画', 1014: '动画制作', 1015: '原作', 1016: '导演', 1017: '动画监督', 1018: '制作总指挥', 1019: 'QC', 1020: '动画剧 本', 1021: '程序', 1022: '协力', 1023: 'CG 监修', 1024: 'SD原画', 1025: '背景', 1026: '监修', 1027: '系列构成', 1028: ' 企画', 1029: '机械设定', 1030: '音响监督', 1031: '作画监督', 1032: '制作人', 2001: '作者', 2002: '作画', 2003: '插图', 2004: '出版社', 2005: '连载杂志', 2006: '译者', 2007: '原作', 2008: '客串', 2009: '人物原案', 2010: '脚本', 2011: '文库', 2012: '出品方', 3001: '艺术家', 3002: '制作人', 3003: '作曲', 3004: '厂牌', 3005: '原作', 3006: '作词', 3007: '录音', 3008: '编曲', 3009: '插图', 3010: '脚本', 3011: '出版方', 3012: '母带制作', 3013: '混音', 3014: '乐器', 3015: '声乐', 4001: '原作', 4002: '导演', 4003: '编剧', 4004: '音乐', 4005: '执行制片人', 4006: '共同执行制作', 4007: '制片人', 4008: '监制', 4009: '副制作人', 4010: '故事', 4011: '编审', 4012: '剪辑', 4013: '创意总监', 4014: '摄影', 4015: '主题歌演出', 4016: '主演', 4017: '配角', 4018: '制作', 4019: '出品'}
relation_type_map = {1: '改编', 2: '前传', 3: '续集', 4: '总集篇', 5: '全集', 6: '番外篇', 7: '角色出演', 8: '相同世界观', 9: '不同世界观', 10: '不同演绎', 11: '衍生', 12: '主线故事', 14: '联动', 99: '其他', 1002: '系列', 1003: '单行本', 1004: '画集', 1005: '前传', 1006: '续集', 1007: '番外篇', 1008: '主线故事', 1010: '不同版本', 1011: '角色出演', 1012: '相同世界观', 1013: '不同世界观', 1014: '联动', 1099: '其他', 3001: '原声集',3002: '角色歌',3003: '片头曲',3004: '片尾曲',3005: '插入歌',3006: '印象曲',3007: '广播剧',3099: '其他', 4002: '前传',4003: '续集',4006: '外传',4007: '角色出演',4008: '相同世界观',4009: '不同世界观',4010: '不同演绎',4012: '主线故事',4014: '联动',4015: '扩展包',4016: '不同版本',4017: '主版本',4018: '合集',4019: '收录作品',4099: '其他'}
character_type_map = {1: '主角', 2: '配角', 3: '客串'}
def load_names(file, key_prefix, name_extractor):
    with open(file, 'r', encoding='utf-8') as f:
        return {f"{key_prefix}_{data['id']}": name_extractor(data) for line in f for data in [json.loads(line)]}
def extract_name(d):
    m = re.search(r'\|简体中文名= ([^\r\n]+)', d.get('infobox', ''))
    return m.group(1) if m else d.get('name_cn', d.get('name', ''))
def read_jsonlines_to_graph(files):
    graph = defaultdict(set)
    edges = {}
    def add_edge(node1, node2, edge_type):
        graph[node1].add(node2)
        graph[node2].add(node1)
        edges[(node1, node2)] = edge_type
        edges[(node2, node1)] = edge_type
    for file in files:
        with open(file, 'r') as f:
            for data in map(json.loads, f):
                ids = {
                    's': f"s_{data['subject_id']}" if 'subject_id' in data else None,
                    'r': f"s_{data['related_subject_id']}" if 'related_subject_id' in data else None,
                    'p': f"p_{data['person_id']}" if 'person_id' in data else None,
                    'c': f"c_{data['character_id']}" if 'character_id' in data else None,
                }
                if ids['s'] and ids['r']:
                    edge_type = relation_type_map.get(data.get('relation_type'), data.get('relation_type'))
                    add_edge(ids['s'], ids['r'], edge_type)
                if ids['c'] and ids['s']:
                    if 'subject-characters.jsonlines' in file: edge_type = character_type_map.get(data.get('type'), data.get('type'))
                    elif 'person-characters.jsonlines' in file: edge_type = edges.get((ids['c'], ids['s']))
                    add_edge(ids['c'], ids['s'], edge_type)
                if ids['c'] and ids['p']:
                    edge_type = "配音"
                    add_edge(ids['p'], ids['c'], edge_type)
                if ids['p'] and ids['s'] and 'subject-persons.jsonlines' in file:
                    edge_type = position_map.get(data.get('position'), data.get('position'))
                    add_edge(ids['p'], ids['s'], edge_type)
    return graph, edges
def bfs_shortest_path(graph, edges, start, goal, island):
    if start == goal: return 0, [start], []
    if start not in island or goal not in island: return -1, [], []
    queue, visited = deque([(start, [start], [])]), set()
    while queue:
        node, path, edge_types = queue.popleft()
        if node in visited: continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor == goal:
                return len(path), path + [goal], edge_types + [edges[(node, neighbor)]]
            if neighbor not in visited and neighbor in island:
                queue.append((neighbor, path + [neighbor], edge_types + [edges[(node, neighbor)]]))
    return -1, [], []
def bfs_longest_path_from_node(graph, edges, start, island):
    queue, visited, max_steps, longest_path, longest_edge_types = deque([(start, [start], [])]), {start}, -1, [], []
    while queue:
        node, path, edge_types = queue.popleft()
        if len(path) > max_steps:
            max_steps, longest_path, longest_edge_types = len(path), path, edge_types
        for neighbor in graph[node]:
            if neighbor not in visited and neighbor in island:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], edge_types + [edges[(node, neighbor)]]))
    return max_steps - 1, longest_path, longest_edge_types
def find_longest_shortest_path(graph, edges, names, islands):
    max_steps, longest_path, longest_edge_types = -1, [], []
    for island in islands:
        start_node = next(iter(island))
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
        queue = deque([(max_distance_node, [max_distance_node], [])])
        visited = {max_distance_node}
        while queue:
            node, path, edge_types = queue.popleft()
            if len(path) > max_steps:
                max_steps, longest_path, longest_edge_types = len(path), path, edge_types
                print(f"\n找到最长最短步数为{max_steps - 1}的路径:")
                print_path(longest_path, longest_edge_types, names, edges)
            for neighbor in graph[node]:
                if neighbor not in visited and neighbor in island:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], edge_types + [edges[(node, neighbor)]]))
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
def print_path(path, edge_types, names, edges):
    for i in range(len(path) - 1):
        node = path[i]
        next_node = path[i + 1]
        node_type, node_id = node.split("_")
        node_label = {"s": "条目", "p": "人物", "c": "角色"}.get(node_type, '')
        edge_type = edges.get((node, next_node), '')
        arrow = "→"
        print(f"{node_id}, {node_label}, {names.get(node, '')}（{edge_type}{arrow}）")
    last_node = path[-1]
    node_type, node_id = last_node.split("_")
    node_label = {"s": "条目", "p": "人物", "c": "角色"}.get(node_type, '')
    print(f"{node_id}, {node_label}, {names.get(last_node, '')}")
def main():
    files = ['subject-relations.jsonlines', 'subject-persons.jsonlines', 'subject-characters.jsonlines', 'person-characters.jsonlines']
    print("图加载中")
    graph, edges = read_jsonlines_to_graph(files)
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
            max_steps, _ = find_longest_shortest_path(graph, edges, names, islands)
            print(f"\n最长的最短路径长度为{max_steps}步" if max_steps != -1 else "\n不存在最长的最短路径")
        elif len(args) == 2:
            start_node = parse_input(args[0], args[1])
            for island in islands:
                if start_node in island:
                    max_steps, path, edge_types = bfs_longest_path_from_node(graph, edges, start_node, island)
                    if max_steps != -1:
                        print(f"\n从节点{start_node}出发的最长路径长度为：{max_steps}\n路径：")
                        print_path(path, edge_types, names, edges)
                    else:
                        print(f"\n从节点{start_node}出发没有找到路径")
                    break
            else:
                print(f"\n节点{start_node}不属于任何连通分量")
        elif len(args) == 4:
            start_node, goal_node = parse_input(args[0], args[1]), parse_input(args[2], args[3])
            for island in islands:
                if start_node in island and goal_node in island:
                    steps, path, edge_types = bfs_shortest_path(graph, edges, start_node, goal_node, island)
                    if steps != -1:
                        print(f"\n从{start_node}到{goal_node}的最短路径长度为：{steps}步\n路径：")
                        print_path(path, edge_types, names, edges)
                    else:
                        print(f"\n在{start_node}与{goal_node}之间不存在路径")
                    break
            else:
                print(f"\n在{start_node}与{goal_node}之间不存在路径")
        else:
            print("\n无效的命令。请确保输入1个节点（寻找最长路径）或2个节点（寻找最短路径）。")
if __name__ == "__main__":
    main()
