import pandas as pd
def generate_combinations(original_data, result, results):
    if 0 not in result:
        results.append(list(original_data) + result)
    else:
        for replacement in [1, -1]:
            new_result = result[:]
            new_result[result.index(0)] = replacement
            generate_combinations(original_data, new_result, results)
def count_patterns(df):
    pattern_to_ids = {}
    for _, row in df.iterrows():
        pattern_str = str(tuple(row[7:17]))
        if pattern_str not in pattern_to_ids:
            pattern_to_ids[pattern_str] = []
        pattern_to_ids[pattern_str].append(row.iloc[0])
    pattern_counts = {k: len(v) for k, v in pattern_to_ids.items()}
    pattern_counts_df = pd.DataFrame(list(pattern_counts.items()), columns=['Pattern', 'Count'])
    pattern_counts_df['IDs'] = pattern_counts_df['Pattern'].apply(lambda x: pattern_to_ids[x])
    return pattern_counts_df.sort_values(by='Count', ascending=False)
df = pd.read_csv('sorted1.csv', encoding='utf-8-sig')
columns = list(df.columns[:7]) + ['2-1', '3-2', '4-3', '5-4', '6-5', '7-6', '8-7', '9-8', '10-9']
results, intermediate_results = [], []
for _, row in df.iterrows():
    original_data = row.iloc[:7]
    data = row.iloc[7:17]
    result = [0 if data.iloc[i] == data.iloc[i+1] else 1 if data.iloc[i] < data.iloc[i+1] else -1 for i in range(9)]
    intermediate_results.append(list(original_data) + result)
    if 0 in result:
        generate_combinations(original_data, result, results)
    else:
        results.append(list(original_data) + result)
intermediate_df = pd.DataFrame(intermediate_results, columns=columns)
intermediate_df.to_csv('output470.csv', index=False)
count_patterns(intermediate_df).to_csv('output470_patterns.csv', index=False)
output_df = pd.DataFrame(results, columns=columns)
output_df.to_csv('output47.csv', index=False)
count_patterns(output_df).to_csv('output47_patterns.csv', index=False)
