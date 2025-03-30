import PySimpleGUI as sg
import random
sg.theme("DarkBrown3")

layout = [[sg.T("ワタシが考えた数を当ててね。1〜100までの数だよ。")],
          [sg.Im(k="img1"), sg.T(k="txt1")],
          [sg.I(k="in1", size=(10)),
           sg.B(" 入力 ", k="btn", bind_return_key=True)]]
win = sg.Window("数当てゲーム", layout, font=(None,14), finalize=True)

def question():
    global playflag, ans, count
    ans = random.randint(1,100)
    count = 0
    win["txt1"].update("")
    win["img1"].update("futaba0.png")
    playflag = True

def anscheck():
    global playflag, count
    if v["in1"].isdecimal() == False:
        win["txt1"].update("数字を入力してね。")
    else:
        count += 1
        mynum = int(v["in1"])
        if mynum == ans:
            win["txt1"].update(f"{count}回目：当たり！\n入力ボタンで、また遊べるよ。")
            win["img1"].update("futaba2.png")
            playflag = False 
        elif mynum < ans:
            win["txt1"].update(f"{count}回目：もっと大きいよ")
        else:
            win["txt1"].update(f"{count}回目：もっと小さいよ")

question()
while True:
    e, v = win.read()
    if e == "btn":
        if playflag == False:
            question()
        else:
            anscheck()
    if e == None:
        break
win.close()
