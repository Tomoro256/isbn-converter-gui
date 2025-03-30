import pandas as pd

# CSVファイルをデータフレームに読み込む
df = pd.read_csv("898.csv")

print(len(df))
print(df.columns.values)