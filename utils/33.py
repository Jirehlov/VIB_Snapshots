import argparse
def compare_files(file1_path, file2_path):
    context_size = 20
    try:
        with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
            position = 0
            buffer1 = file1.read(context_size)
            buffer2 = file2.read(context_size)
            while True:
                byte1 = file1.read(1)
                byte2 = file2.read(1)
                if not byte1 and not byte2:
                    print("Files are identical.")
                    return
                if byte1 != byte2:
                    context1 = buffer1[-context_size:] + byte1 + file1.read(context_size)
                    context2 = buffer2[-context_size:] + byte2 + file2.read(context_size)
                    print(f"First different byte found at position {position}:")
                    print(f"{file1_path}: {byte1} (context: {context1})")
                    print(f"{file2_path}: {byte2} (context: {context2})")
                    return
                buffer1 = buffer1[1:] + byte1
                buffer2 = buffer2[1:] + byte2
                position += 1
    except FileNotFoundError as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two binary files.")
    parser.add_argument("file1", type=str, help="Path to the first file")
    parser.add_argument("file2", type=str, help="Path to the second file")
    args = parser.parse_args()
    compare_files(args.file1, args.file2)
