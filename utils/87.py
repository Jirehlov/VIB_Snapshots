import pandas as pd
import glob
import os
from tqdm import tqdm
from collections import defaultdict
def generate_combinations(original_data, result, results):
    if 0 not in result:
        results.append(list(original_data) + result)
    else:
        for replacement in [1, -1]:
            new_result = result[:]
            new_result[result.index(0)] = replacement
            generate_combinations(original_data, new_result, results)
def get_pattern(row):
    data = row.iloc[7:17]
    return tuple(0 if data.iloc[i] == data.iloc[i+1] else 1 if data.iloc[i] < data.iloc[i+1] else -1 for i in range(9))
def process_csv(filepath, subject_patterns):
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    subjects = df.iloc[:, 0].values
    patterns = [get_pattern(df.iloc[i]) for i in range(len(df))]
    titles = df.iloc[:, 3].values
    for i in range(len(subjects)):
      subject = subjects[i]
      pattern = patterns[i]
      title = titles[i]
      if subject not in subject_patterns:
          subject_patterns[subject] = []
      subject_patterns[subject].append((pattern, title))
    return subject_patterns
def count_pattern_changes(subject_patterns):
    change_counts = defaultdict(int)
    for subject, patterns_and_titles in subject_patterns.items():
        changes = 0
        if len(patterns_and_titles) > 1:
            for i in range(len(patterns_and_titles) - 1):
                if patterns_and_titles[i][0] != patterns_and_titles[i+1][0]:
                    changes += 1
        change_counts[subject] = (changes, subject_patterns[subject][0][1])
    return change_counts
def main():
    filepaths = sorted(glob.glob('year_end_report/2024/sorted_*.csv'), key=lambda x: int(x.split('_')[-1].split('.')[0]))
    subject_patterns = {}
    for filepath in tqdm(filepaths, desc="Processing CSV files"):
        subject_patterns = process_csv(filepath, subject_patterns)
    change_counts = count_pattern_changes(subject_patterns)
    sorted_changes = sorted(change_counts.items(), key=lambda item: item[1][0], reverse=True)
    for subject, (count, title) in sorted_changes[:10]:
        print(f"{subject},{title},{count}")
if __name__ == "__main__":
    main()