def count_bits_in_file(filename):
    lookup_table = [bin(i).count('1') for i in range(256)]
    ones = 0
    total_bytes = 0
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            total_bytes += len(chunk)
            for byte in chunk:
                ones += lookup_table[byte]
    total_bits = total_bytes * 8
    zeros = total_bits - ones
    return ones, zeros
filename = 'sorted1.csv'
ones, zeros = count_bits_in_file(filename)
print(f"1的数量: {ones}")
print(f"0的数量: {zeros}")
