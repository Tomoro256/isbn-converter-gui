import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Hiragino Maru Gothic Pro", "Hiragino sans", "BIZ UDGothic", "MS Gothic"]

# CSVファイルをデータフレームに読み込む
df = pd.read_csv("FEH_00200524_240108155037.csv", index_col="全国・都道府県", encoding="UTF-8")

print(df["2022年"])
# 2022年の列データで棒グラフを作って表示する
df["2022年"].plot.bar()
plt.show()