import csv, sympy
prime_scores = []
composite_scores = []
with open('sorted1.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    rows = []
    for row in reader:
        subject_id = int(row[0])
        score = float(row[4])
        rows.append(subject_id)
        if sympy.isprime(subject_id):
            prime_scores.append(score)
        else:
            composite_scores.append(score)
total_rows = len(rows)
prime_count = len(prime_scores)
prime_pi_of_total = sympy.primepi(total_rows)
prime_avg = sum(prime_scores) / prime_count if prime_count > 0 else 0
composite_avg = sum(composite_scores) / (total_rows - prime_count) if total_rows - prime_count > 0 else 0
print(f"总行数: {total_rows}")
print(f"subject_id 是素数的行数 p: {prime_count}")
print(f"总行数以内素数的个数 pi(总行数): {prime_pi_of_total}")
print(f"pi(总行数) / 总行数: {prime_pi_of_total / total_rows * 100:.3f}%")
print(f"p / 总行数: {prime_count / total_rows * 100:.3f}%")
print(f"素数行的评分平均数: {prime_avg:.4f}")
print(f"合数行的评分平均数: {composite_avg:.4f}")
