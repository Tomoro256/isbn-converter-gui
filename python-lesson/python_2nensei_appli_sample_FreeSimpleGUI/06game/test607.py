import random

def getnextnums(n):
    global nextnums, choicemsg
    nextnums = list(range(n+1, min(32, n+4)))
    choicemsg = f"{nextnums} から入力してください。"
    print(choicemsg)

def question():
    global playflag
    getnextnums(0)
    print("さあ、ゲームを始めるよ！")
    playflag = True

def com_turn(comnum):
    keynums = [2,6,10,14,18,22,26,30]
    getnextnums(comnum)
    comnum += 1
    for n in nextnums:
        if n in keynums:
            comnum = n
    if random.randint(0,1) > 0:
        comnum = nextnums[0]
    print(f"ワタシは、[ {comnum} ] にするよ。")
    getnextnums(comnum)

def my_turn():
    global playflag
    if indata.isdecimal() == True:
        mynum = int(indata)
        if mynum in nextnums:
            if mynum == 31:
                print("あなたの負けだよ。")
                playflag = False
            elif mynum == 30:
                print("あなたの勝ちだよ。")
                playflag = False
            else:
                com_turn(mynum)
        else:
            print(choicemsg)

question()
while True:
    indata = input("入力してね。")
    if playflag == False:
        question()
    else:
        my_turn()
        