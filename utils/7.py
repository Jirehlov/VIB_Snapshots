import pandas as pd
df1 = pd.read_csv('sorted1.csv')
df2 = pd.read_csv('sorted2.csv')
merged_df = pd.merge(df1, df2, on='subject', how='outer')
merged_df.to_csv('merged_file.csv', index=False)
