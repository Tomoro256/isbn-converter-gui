import datetime

sch = [ ["１時限",8,30],
        ["昼休み",12,35]]
now = datetime.datetime.now()
now = now.replace(hour=10)
print(f"現在 = {now:%H:%M:%S}")
for s in sch:
    dt = now.replace(hour=s[1], minute=s[2], second=0) - now
    print(f"{s} = あと{dt}")
