import pandas as pd
import argparse
def compare_csvs(file1, file2, column):
    df1 = pd.read_csv(file1, index_col=0)
    df2 = pd.read_csv(file2, index_col=0)
    common = df1.index.intersection(df2.index)
    old = df1.loc[common, column]
    new = df2.loc[common, column]
    title = df1.loc[common, "中文标题"]
    change = new - old
    summary = pd.DataFrame({
        "中文标题": title,
        "旧值": old,
        "新值": new,
        "变化量": change.map(lambda x: f"{x:+}")
    })
    top10 = summary.sort_values(by="变化量", key=lambda s: s.str.replace('+','').astype(float), ascending=False).head(10)
    bottom10 = summary.sort_values(by="变化量", key=lambda s: s.str.replace('+','').astype(float)).head(10)
    print("\nTop 10 增长最大：")
    print(top10[["中文标题", "旧值", "新值", "变化量"]].to_string())
    print("\nBottom 10 减少最大：")
    print(bottom10[["中文标题", "旧值", "新值", "变化量"]].to_string())
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file1")
    parser.add_argument("file2")
    parser.add_argument("column")
    args = parser.parse_args()
    compare_csvs(args.file1, args.file2, args.column)
