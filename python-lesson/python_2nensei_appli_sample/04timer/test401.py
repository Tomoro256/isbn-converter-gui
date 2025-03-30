import datetime

now = datetime.datetime.now()
print(f"{now:%H時%M分%S秒}")
print(f"{now:%H:%M:%S}")
print(f"{now:%p %I:%M:%S}")
print(f"{now:%Y/%m/%d(%a)}")
