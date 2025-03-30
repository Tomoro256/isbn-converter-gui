import datetime

now = datetime.datetime.now()
print(f"現在 = {now:%m/%d %H:%M:%S}")
goal = now.replace(hour=20, minute=30, second=0)
print(f"目標 = {goal:%m/%d %H:%M:%S}")
td = goal - now
print(td)
