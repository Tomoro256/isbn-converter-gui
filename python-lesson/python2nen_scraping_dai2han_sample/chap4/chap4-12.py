import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Hiragino Maru Gothic Pro", "Hiragino sans", "BIZ UDGothic", "MS Gothic"]

# CSVファイルをデータフレームに読み込む
df1 = pd.read_csv("Preview_20240107184148.csv", index_col="時点", skiprows=1)

# 平均気温で折れ線グラフを表示
df1["年平均気温【℃】"].plot()
plt.show()