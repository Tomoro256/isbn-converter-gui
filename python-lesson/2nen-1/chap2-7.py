import requests
from bs4 import BeautifulSoup

load_url = "https://www.aozora.gr.jp/cards/000879/files/92_14545.html"
html=requests.get(load_url)
soup=BeautifulSoup(html.content,"html.parser")
print(soup)