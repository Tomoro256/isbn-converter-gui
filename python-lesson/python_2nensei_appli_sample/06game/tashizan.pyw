import PySimpleGUI as sg
import random
sg.theme("DarkBrown3")

layout = [[sg.T(k="txt1")],
          [sg.Im(k="img"), sg.T(k="txt2")],
          [sg.T(k="txt3"), sg.I(k="in1", size=(10)),
          sg.B(" 入力 ", k="btn", bind_return_key=True)]]
win = sg.Window("足し算ゲーム", layout, font=(None,14), finalize=True)

def question():
    global playflag, ans
    a = random.randint(0,100)
    b = random.randint(0,100)
    ans = a + b
    win["txt1"].update("足し算ゲームです。問題の答えを入力してね。")
    win["txt2"].update("")
    win["txt3"].update(f"問題：{a} + {b} =?")
    win["img"].update("futaba0.png")
    playflag = True

def anscheck():
    global playflag
    if v["in1"].isdecimal() == False:
        win["txt2"].update("数字を入力してね。")
    else:
        mynum = int(v["in1"])
        if mynum == ans:
            win["txt2"].update("正解で〜す！")
            win["txt1"].update("入力ボタンを押すと、次の問題が出るよ。")
            win["img"].update("futaba2.png")
            playflag = False
        else:
            win["txt2"].update(f"{mynum}じゃないよ。")

question()
while True:
    e, v = win.read()
    if e == "btn":
        if playflag == False:
            question()
        else :
            anscheck()
    if e == None:
        break
win.close()
