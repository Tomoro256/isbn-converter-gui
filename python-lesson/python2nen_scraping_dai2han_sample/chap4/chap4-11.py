import pandas as pd

# CSVファイルをデータフレームに読み込む
df1 = pd.read_csv("Preview_20240107184148.csv", index_col="時点", skiprows=1)
df2 = pd.read_csv("Preview_20240107184235.csv", index_col="時点", skiprows=1)
df3 = pd.read_csv("Preview_20240107184333.csv", index_col="時点", skiprows=1)

print(df1.columns.values)
print(df2.columns.values)
print(df3.columns.values)