import requests

# Webページを取得する
url = "https://www.ymori.com/books/python2nen/test1.html"
response = requests.get(url)

#文字化けしないようにする
response.encoding = response.apparent_encoding

#取得した文字列データを表示する
print(response.text)