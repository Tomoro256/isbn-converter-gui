import pandas as pd

# CSVファイルをデータフレームに読み込む
df = pd.read_csv("13TOKYO.CSV", header=None, encoding="shift_jis", dtype=str)

print(len(df))
print(df.columns.values)