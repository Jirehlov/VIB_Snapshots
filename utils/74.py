import csv, sympy
with open('sorted1.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    rows = [int(row[0]) for row in reader]
total_rows = len(rows)
prime_count = sum(1 for x in rows if sympy.isprime(x))
prime_pi_of_total = sympy.primepi(total_rows)
print(f"总行数: {total_rows}")
print(f"subject_id 是素数的行数 p: {prime_count}")
print(f"总行数以内素数的个数 pi(总行数): {prime_pi_of_total}")
print(f"pi(总行数) / 总行数: {prime_pi_of_total / total_rows * 100:.3f}%")
print(f"p / 总行数: {prime_count / total_rows * 100:.3f}%")