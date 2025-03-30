import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Hiragino Maru Gothic Pro", "Hiragino sans", "BIZ UDGothic", "MS Gothic"]
 
# CSVファイルを読み込む（名前の列をインデックスで）
df = pd.read_csv("test.csv", index_col=0)

# 国語の棒グラフ（水平）を作って表示する
df["国語"].plot.barh()
plt.legend(loc="lower left")
plt.show()

# 国語と数学の棒グラフ（水平）を作って表示する
df[["国語","数学"]].plot.barh()
plt.legend(loc="lower left")
plt.show()

# C子の棒グラフ（水平）を作って表示する
df.loc["C子"].plot.barh()
plt.legend(loc="lower left")
plt.show()

# C子の円グラフを作って表示する
df.loc["C子"].plot.pie(labeldistance=0.6)
plt.legend(loc="lower left")
plt.show()
