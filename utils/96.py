import os
import matplotlib.pyplot as plt
def calculate_line_count(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return sum(1 for _ in file)
def get_sorted_files(directory, prefix='sorted_'):
    return sorted([f for f in os.listdir(directory) if f.startswith(prefix)])
def plot_line_differences(differences):
    plt.figure(figsize=(10, 6))
    plt.plot(differences, marker='o', linestyle='-', color='m')
    plt.xlabel('File Index')
    plt.ylabel('Line Count Difference')
    plt.title('Line Count Differences Between "sorted_" Files')
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
    line_differences = [line_counts[i] - line_counts[i - 1] for i in range(1, len(line_counts))]
    for i, diff in enumerate(line_differences, start=1):
        print(f"Δ Line Count (File {i-1} → File {i}): {diff}")
    plot_line_differences(line_differences)
if __name__ == "__main__":
    directory = os.path.expandvars('%USERPROFILE%\\Documents\\GitHub\\VIB_Snapshots')
    main(directory)
