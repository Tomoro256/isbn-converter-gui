import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Hiragino Maru Gothic Pro", "Hiragino sans", "BIZ UDGothic", "MS Gothic"]

# CSVファイルをデータフレームに読み込む
df1 = pd.read_csv("Preview_20240107184148.csv", index_col="時点", skiprows=1)
df2 = pd.read_csv("Preview_20240107184235.csv", index_col="時点", skiprows=1)
df3 = pd.read_csv("Preview_20240107184333.csv", index_col="時点", skiprows=1)
df2 = df2.rename(columns={"東京都":"最高気温"})
df3 = df3.rename(columns={"東京都":"最低気温"})

# ３つのグラフを重ねて表示
df1["年平均気温【℃】"].plot()
df2["最高気温"].plot()
df3["最低気温"].plot()
plt.ylim(-10,40)
plt.legend(loc="lower right")
plt.show()