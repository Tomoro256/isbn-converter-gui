import random
hand = ["グー", "チョキ", "パー"]
message = ["あいこ", "あなたの勝ち", "ワタシの勝ち"]
mynum = random.randint(0,2)
comnum = random.randint(0,2)
print(f"あなたは{hand[mynum]}。ワタシは{hand[comnum]}")
hantei = (comnum - mynum) % 3
print(f"勝敗判定: {message[hantei]} で〜す。")
