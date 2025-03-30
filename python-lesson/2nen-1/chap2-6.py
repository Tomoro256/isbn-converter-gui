import requests
from bs4 import BeautifulSoup

#webページを取得して解析する
load_url = "https://www.ymori.com/books/python2nen/test2.html"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

#idタグで検索し、その仲のすべてのliタグを検索して表示する
chap2 = soup.find(id = "chap2")
for element in chap2.find_all("li"):
    print(element.text)
