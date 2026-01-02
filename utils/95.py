import os
import matplotlib.pyplot as plt
def calculate_line_count(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return sum(1 for _ in file)
def get_sorted_files(directory, prefix='sorted_'):
    return sorted([f for f in os.listdir(directory) if f.startswith(prefix)])
def plot_line_counts(line_counts):
    plt.figure(figsize=(10, 6))
    plt.plot(line_counts, marker='o', linestyle='-', color='g')
    plt.xlabel('File Index')
    plt.ylabel('Line Count')
    plt.title('Line Count of Files Starting with "sorted_"')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def main(directory):
    file_names = get_sorted_files(directory)
    line_counts = []
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        line_count = calculate_line_count(file_path)
        line_counts.append(line_count)
        print(f"File: {file_name}, Line Count: {line_count}")
    plot_line_counts(line_counts)
if __name__ == "__main__":
    directory = os.path.expandvars('%USERPROFILE%\\Documents\\GitHub\\VIB_Snapshots')
    main(directory)
