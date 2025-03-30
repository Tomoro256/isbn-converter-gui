import requests

# Webページを取得する
url = "https://www.ymori.com/books/python2nen/test1.html"
response = requests.get(url)

# 文字化けしないようにする
response.encoding = response.apparent_encoding

# ファイルを書き込みモードで開いて
filename = "download.txt"
with open(filename, mode="w") as f:
	# インターネットから取得したデータを書き込む
	f.write(response.text)
