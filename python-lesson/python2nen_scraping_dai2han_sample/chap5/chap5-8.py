import requests
import json
from pprint import pprint

# 5日間（3時間ごと）の天気を取得する：東京
key="取得したAPIキー"
city="Tokyo,JP"
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&lang=ja&units=metric"

jsondata = requests.get(url).json()
pprint(jsondata)
