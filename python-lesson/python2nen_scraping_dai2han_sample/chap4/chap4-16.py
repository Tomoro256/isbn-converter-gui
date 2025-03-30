import pandas as pd

# CSVファイルをデータフレームに読み込む
df = pd.read_csv("200.csv",encoding="shift-jis")

# 消火栓のある地点（緯度、経度）をリスト化する
hydrant = df[["緯度","経度"]].values
print(len(hydrant))
print(hydrant)
