import requests

# Webページを取得する
url = "https://www.ymori.com/books/python2nen/test1.html"
response = requests.get(url)

# 文字化けしないようにする
response.encoding = response.apparent_encoding

# ファイルを書き込みモードで開いて
filename = "download.txt"
f = open(filename, mode="w")

# インターネットから取得したデータを書き込んで
f.write(response.text)

# 最後にファイルを閉じる
f.close()
