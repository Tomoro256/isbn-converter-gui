import random

def question():
    global playflag, ans, count
    ans = random.randint(1,100)
    count = 0
    print("＞ワタシが考えた数を当ててね。")
    playflag = True

def anscheck():
    global playflag, count
    if indata.isdecimal() == True:
        count += 1
        mynum = int(indata)
        if mynum == ans:
            print(f"{count}回目：当たり！")
            playflag = False 
        elif mynum < ans:
            print(f"{count}回目：もっと大きいよ")
        else:
            print(f"{count}回目：もっと小さいよ")

question()
while True:
    indata = input("入力してね。")
    if playflag == False:
        question()
    else:
        anscheck()
        