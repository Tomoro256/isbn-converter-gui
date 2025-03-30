import requests
import json

# 現在の天気を取得する：神戸
key="取得したAPIキー"
city="Kobe,JP"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=ja&units=metric"

jsondata = requests.get(url).json()
print(jsondata)
