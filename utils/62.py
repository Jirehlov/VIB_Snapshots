import os
import pandas as pd
import argparse
def calculate_sums(directory):
    csv_files = [f for f in os.listdir(directory) if f.startswith('sorted_') and f.endswith('.csv')]
    results = []
    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(directory, csv_file), encoding='utf-8-sig')
        hitnrun_columns = [f'tc{i}' for i in range(1, 74, 8)]
        if not all(col in df.columns for col in hitnrun_columns):
            print(f"Skipping {csv_file}: Missing one or more required columns.")
            continue
        df_total_sum = df[hitnrun_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum().sum()
        file_key = csv_file.split('_')[1].split('.')[0]
        results.append([file_key, df_total_sum])
    result_df = pd.DataFrame(results, columns=['Timestamps', 'Sum'])
    result_df = result_df.sort_values('Timestamps').reset_index(drop=True)
    result_df['Difference'] = result_df['Sum'].diff().fillna(0).astype(int)
    result_df.to_csv('hitnrun_sums.csv', index=False, encoding='utf-8-sig')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate sums for sorted_*.csv files.')
    parser.add_argument('directory', type=str, help='Directory containing the sorted_*.csv files.')
    args = parser.parse_args()
    calculate_sums(args.directory)
