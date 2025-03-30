import requests
from bs4 import BeautifulSoup

#webページを取得して解析する
load_url = "https://www.ymori.com/books/python2nen/test2.html"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

#すべてのliアグを検索して、をの文字列を表示す
for element in soup.find_all("li"):
    print(element.text)
