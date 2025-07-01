import subprocess
import argparse
import os
import glob
from collections import defaultdict, Counter
def find_git_path():
    app_data_path = os.getenv('LOCALAPPDATA')
    base_path = os.path.join(app_data_path, "GitHubDesktop")
    for folder in os.listdir(base_path):
        git_path = os.path.join(base_path, folder, "resources", "app", "git", "mingw64", "bin", "git.exe")
        if os.path.exists(git_path):
            return git_path
    raise FileNotFoundError("未找到 Git 的安装路径，请确认 GitHub Desktop 是否已正确安装。")
def get_repo_path():
    return os.path.expandvars(r"%USERPROFILE%\Documents\GitHub\VIB_Snapshots")
def get_file_relative_path():
    return "server_backup/maxrows.txt"
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=int, choices=[1, 2], required=True,
                        help='1:内容出现次数模式 2:变更次数模式')
    return parser.parse_args()
def get_commit_list(git_path, repo_path, file_relative_path):
    cmd = [git_path, "-C", repo_path, "log", "--pretty=format:%H", "--reverse", "--", file_relative_path]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return result.stdout.strip().split('\n') if result.returncode == 0 else []
def parse_column_data(line):
    if line.startswith("列") and ":" in line:
        col_part, content_part = line.split(":", 1)
        col_name = col_part[len("列"):].split(":")[0].strip()
        content = content_part.strip().strip("[]'")
        return col_name, content
    return None, None
def analyze_data(git_path, repo_path, file_relative_path, mode):
    commits = get_commit_list(git_path, repo_path, file_relative_path)
    column_data = defaultdict(lambda: {
        'counter': Counter(),
        'history': [],
        'changes': 0
    })
    current_state = defaultdict(str)
    for commit in commits:
        if not commit: continue
        cmd = [git_path, "-C", repo_path, "show", f"{commit}:{file_relative_path}"]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0: continue
        for line in result.stdout.splitlines():
            col_name, content = parse_column_data(line)
            if not col_name: continue
            prev_content = current_state.get(col_name)
            if content != prev_content:
                column_data[col_name]['counter'][content] += 1
                column_data[col_name]['history'].append((commit, content))
                column_data[col_name]['changes'] += 1
                current_state[col_name] = content
    if not column_data:
        print("未检测到有效变更")
        return
    if mode == 1:
        sorted_cols = sorted(column_data.items(),
                             key=lambda x: (-len(x[1]['counter']), x[1]['changes']),
                             reverse=False)[:3]
    else:
        sorted_cols = sorted(column_data.items(),
                             key=lambda x: (-x[1]['changes'], len(x[1]['counter'])),
                             reverse=False)[:3]
    print("\n" + "="*50)
    print(f"{'内容种类分析' if mode == 1 else '变更次数分析'} TOP3")
    print("="*50)
    for rank, (col_name, data) in enumerate(sorted_cols, 1):
        print(f"\n🏆 第{rank}名 列：{col_name}")
        print(f"├── 内容种类数：{len(data['counter'])}")
        print(f"├── 总变更次数：{data['changes']}")
        if mode == 1:
            print("└── 完整内容分布：")
            for content, count in data['counter'].most_common():
                print(f"    ▪ {count}次 → [{content}]")
        else:
            print("└── 完整变更历史：")
            for idx, (commit_hash, content) in enumerate(data['history'], 1):
                print(f"    {idx:03d}. {commit_hash[:8]} → [{content}]")
if __name__ == "__main__":
    try:
        GIT_PATH = find_git_path()
        GIT_REPO_PATH = get_repo_path()
        FILE_RELATIVE_PATH = get_file_relative_path()
        args = parse_arguments()
        analyze_data(GIT_PATH, GIT_REPO_PATH, FILE_RELATIVE_PATH, args.mode)
    except Exception as e:
        print(f"发生错误: {e}")
