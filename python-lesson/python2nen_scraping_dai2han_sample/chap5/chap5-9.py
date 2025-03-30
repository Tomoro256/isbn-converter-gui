from datetime import datetime, timedelta, timezone

#UTC（協定世界時）をJST（日本標準時）に変換
timestamp = 1709964000

tz = timezone(timedelta(), 'UTC')
utc = datetime.fromtimestamp(timestamp, tz)
print(utc)

tz = timezone(timedelta(hours=+9), 'JST')
jst = datetime.fromtimestamp(timestamp, tz)
print(jst)
print(str(jst)[:-9])
