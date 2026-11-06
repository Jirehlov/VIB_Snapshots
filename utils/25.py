import sys
def calculate_smallest_prime_factor(n, prime_list):
    for prime in prime_list:
        if n % prime == 0:
            return prime
    return 0
def file_to_int(input_file, output_file, prime_list):
    with open(input_file, 'rb') as f:
        byte_data = f.read()
        int_data = int.from_bytes(byte_data, byteorder='big')
    sys.set_int_max_str_digits(0)
    with open(output_file, 'w') as f:
        f.write(str(int_data))
        f.write('\n')
        smallest_prime = calculate_smallest_prime_factor(int_data, prime_list)
        print("Smallest prime factor: " + str(smallest_prime))
prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
input_file = "sorted1.csv"
output_file = "int.txt"
file_to_int(input_file, output_file, prime_list)
