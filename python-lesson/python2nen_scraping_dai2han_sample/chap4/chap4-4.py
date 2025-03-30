import pandas as pd

# CSVファイルをデータフレームに読み込む
df = pd.read_csv("FEH_00200524_240108155037.csv", index_col="全国・都道府県", encoding="UTF-8")
print(len(df))
print(df.columns.values)