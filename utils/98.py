import json
import sys
from collections import defaultdict
from wcwidth import wcswidth
position_map = {1: '原作', 2: '导演', 3: '脚本', 4: '分镜', 5: '演出', 6: '音乐', 7: '人物原案', 8: '人物设定', 9: '构图', 10: '系列构成', 11: '美术监督', 13: '色彩设计', 14: '总作画监督', 15: '作画监督', 16: '机械设定', 17: '摄影监督', 18: '监修', 19: '道具设计', 20: '原画', 21: '第二原画', 22: '动画检查', 23: '助理制片人', 24: '制作助理', 25: '背景美术', 26: '色彩指定', 27: '数码绘图', 28: '剪辑', 29: '原案', 30: '主题歌编曲', 31: '主题歌作曲', 32: '主题歌作词', 33: '主题歌演出', 34: '插入歌演出', 35: '企画', 36: '企划制作人', 37: '制作管理', 38: '宣传', 39: '录音', 40: '录音助理', 41: '系列监督', 42: '製作', 43: '设定', 44: '音响监督', 45: '音响', 46: '音效', 47: '特效', 48: '配音监督', 49: '联合导演', 50: '背景设定', 51: '补间动画', 52: '执行制片人', 53: '助理制片人', 54: '制片人', 55: '音乐助理', 56: '制作进行', 57: '演员监督', 58: '总制片人', 59: '联合制片人', 60: '台词编辑', 61: '后期制片协调', 62: '制作助理', 63: '制作', 64: '制作协调', 65: '音乐制作', 66: '特别鸣谢', 67: '动画制作', 69: 'CG 导演', 70: '机械作画监督', 71: '美术设计', 72: '副导演', 73: 'OP・ED 分镜', 74: '总导演', 75: '3DCG', 76: '制作协力', 77: '动作作画监督', 80: '监制', 81: '协力', 82: '摄影', 83: '制作进行协力', 84: '设定制作', 85: '音乐制作人', 86: '3DCG 导演', 87: '动画制片人', 88: '特效作画监督', 89: '主演出', 90: '作画监督助理', 91: '演出助理', 92: '主动画师'}
def usage():
    print("用法：python find_similar.py <-a|-b> [-c] <subject_id> [<subject_id2>]")
    print("    -a：使用 person_id 构成集合（无关职位）")
    print("    -b：使用 (person_id, position) 构成集合（考虑职位）")
    print("    -c：比较两个 subject_id 的相似度并输出交集内容（结合 -a 或 -b 的集合方式）")
    sys.exit(1)
def parse_args():
    args = sys.argv[1:]
    if len(args) < 2 or args[0] not in ['-a', '-b']:
        usage()
    mode = args[0]
    compare_mode = (len(args) >= 3 and args[1] == '-c')
    if compare_mode:
        if len(args) != 4:
            usage()
        sids = [int(args[2]), int(args[3])]
    else:
        if len(args) != 2:
            usage()
        sids = [int(args[1])]
    return mode, compare_mode, sids
def load_jsonlines(path, key_func=None, value_func=None):
    res = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            key = key_func(obj) if key_func else obj["id"]
            value = value_func(obj) if value_func else obj
            res[key] = value
    return res
def get_display_name(sid, subject_names):
    return subject_names.get(sid, f"(ID:{sid})")
def get_person_names():
    try:
        return load_jsonlines(
            "person.jsonlines",
            key_func=lambda o: o["id"],
            value_func=lambda o: o.get("name_cn") or o.get("name") or "<无名>"
        )
    except Exception:
        return {}
def pad(s, width):
    s = str(s)
    gap = width - wcswidth(s)
    return s + (" " * (gap if gap > 0 else 0))
def build_relation_trees():
    relation_map = defaultdict(set)
    with open("subject-relations.jsonlines", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            sid, rid = obj["subject_id"], obj["related_subject_id"]
            relation_map[sid].add(rid)
            relation_map[rid].add(sid)
    visited = set()
    trees = []
    def iterative_dfs(start):
        stack = [start]
        tree = set()
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                tree.add(node)
                stack.extend(relation_map[node] - visited)
        return tree
    for subject_id in relation_map:
        if subject_id not in visited:
            tree = iterative_dfs(subject_id)
            trees.append(tree)
    return trees
def get_tree_for_subject(trees, subject_id):
    for tree in trees:
        if subject_id in tree:
            return tree
    return set()
def main():
    mode, compare_mode, subject_ids = parse_args()
    subject_data = defaultdict(set)
    with open("subject-persons.jsonlines", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            sid = obj["subject_id"]
            person = obj["person_id"]
            elem = person if mode == "-a" else (person, obj["position"])
            subject_data[sid].add(elem)
    subject_names = load_jsonlines(
        "subject.jsonlines",
        key_func=lambda o: o["id"],
        value_func=lambda o: o.get("name_cn") or o.get("name")
    )
    relation_trees = build_relation_trees()
    if compare_mode:
        sid1, sid2 = subject_ids
        if sid1 not in subject_data or sid2 not in subject_data:
            print(f"没有找到 subject_id = {sid1} 或 subject_id = {sid2} 哟~")
            sys.exit(1)
        set1, set2 = subject_data[sid1], subject_data[sid2]
        inter = set1 & set2
        union = set1 | set2
        sim = len(inter) / len(union) if union else 0
        mode_text = "无关职位" if mode == "-a" else "考虑职位"
        print(f"\n{get_display_name(sid1, subject_names)} 与 {get_display_name(sid2, subject_names)} 的相似度为：{sim:.4f}")
        print(f"（模式：{mode_text}）")
        if inter:
            print(f"\n共有 {len(inter)} 个交集：")
            person_names = get_person_names()
            if mode == "-a":
                header = f"{'ID':>10} | {'姓名'}"
                print(header)
                print('-' * wcswidth(header))
                for pid in sorted(inter):
                    print(f"{pid:10} | {person_names.get(pid, '<无名>')}")
            else:
                header = f"{'ID':>10} | {'姓名':<30} | {'职位'}"
                print(header)
                print('-' * wcswidth(header))
                for pid, pos in sorted(inter):
                    position_cn = position_map.get(pos, f"(职位ID:{pos})")
                    print(f"{pid:10} | {pad(person_names.get(pid, '<无名>'), 30)} | {position_cn}")
        else:
            print("\n没有交集内容。")
        sys.exit(0)
    target_id = subject_ids[0]
    if target_id not in subject_data:
        print(f"没有找到 subject_id = {target_id} 哟~")
        sys.exit(1)
    target_set = subject_data[target_id]
    target_tree = get_tree_for_subject(relation_trees, target_id)
    similarities = []
    for sid, s in subject_data.items():
        if sid == target_id or sid in target_tree:
            continue
        inter = target_set & s
        union = target_set | s
        sim = len(inter) / len(union) if union else 0
        similarities.append((sid, sim))
    top_10 = sorted(similarities, key=lambda x: x[1], reverse=True)[:10]
    name_width = 6
    for sid, _ in top_10:
        n = str(get_display_name(sid, subject_names))
        name_width = max(name_width, wcswidth(n))
    target_name = get_display_name(target_id, subject_names)
    mode_name = "无关职位" if mode == "-a" else "考虑职位"
    print(f"\n与《{target_name}》最相似的前 10 个：")
    print(f"（模式：{mode_name}）\n")
    header = f"{'ID':>6} | {pad('名称', name_width)} | {'相似度':>7}"
    print(header)
    print('-' * wcswidth(header))
    for sid, sim in top_10:
        name = get_display_name(sid, subject_names)
        print(f"{sid:6} | {pad(name, name_width)} | {sim:7.4f}")
if __name__ == "__main__":
    main()
