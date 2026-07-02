import os
import numpy as np
import matplotlib.pyplot as plt
def calculate_entropy(file_path):
    with open(file_path, 'rb') as file:
        byte_arr = np.frombuffer(file.read(), dtype=np.uint8)
    if len(byte_arr) == 0:
        return 0.0
    counts = np.bincount(byte_arr, minlength=256)
    probs = counts / len(byte_arr)
    non_zero_probs = probs[probs > 0]
    entropy = -np.sum(non_zero_probs * np.log2(non_zero_probs))
    return entropy
def get_sorted_files(directory, prefix='sorted_'):
    return sorted([f for f in os.listdir(directory) if f.startswith(prefix)])
def plot_entropy(entropy_values):
    plt.figure(figsize=(10, 6))
    plt.plot(entropy_values, marker='o', linestyle='-', color='b')
    plt.xlabel('File Index')
    plt.ylabel('Entropy (bits/byte)')
    plt.title('Entropy of Files Starting with "sorted_"')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def main(directory):
    file_names = get_sorted_files(directory)
    entropy_values = []
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        entropy = calculate_entropy(file_path)
        entropy_values.append(entropy)
        print(f"File: {file_name}, Entropy: {entropy:.4f}")
    plot_entropy(entropy_values)
if __name__ == "__main__":
    directory = os.path.expandvars('%USERPROFILE%\\Documents\\GitHub\\VIB_Snapshots')
    main(directory)
