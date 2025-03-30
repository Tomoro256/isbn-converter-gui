import random

def question():
    global playflag, ans
    a = random.randint(0,100)
    b = random.randint(0,100)
    ans = a + b
    print(f"問題：{a} + {b} =?")
    playflag = True

def anscheck():
    global playflag
    if indata.isdecimal() == True:
        mynum = int(indata)
        if mynum == ans:
            print("正解で〜す！")
            playflag = False
        else:
            print(f"{mynum}じゃないよ。")

question()
while True:
    indata = input("入力してね。")
    if playflag == False:
        question()
    else:
        anscheck()