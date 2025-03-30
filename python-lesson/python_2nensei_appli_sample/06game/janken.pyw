import PySimpleGUI as sg
import random
sg.theme("DarkBrown3")

layout = [[sg.T("ワタシと、じゃんけんをしよう！")],
          [sg.Im("futaba0.png",k="img1"), sg.Im(k="img2")],
          [sg.T(k="txt")],
          [sg.B(" グー ", k="btn0"),
           sg.B(" チョキ ", k="btn1"),
           sg.B(" パー ", k="btn2")]]
win = sg.Window("じゃんけんアプリ", layout, font=(None,14))

handimg = ["h0.png", "h1.png", "h2.png"]
message = ["あいこ", "あなたの勝ち", "ワタシの勝ち"]
faceimg = ["futaba0.png","futaba1.png","futaba2.png"]

def janken(mynum):
    comnum = random.randint(0,2)
    win["img2"].update(handimg[comnum])
    hantei = (comnum - mynum) % 3
    win["txt"].update(message[hantei] + "で〜す。")
    win["img1"].update(faceimg[hantei])

while True:
    e, v = win.read()
    if e == "btn0":
        janken(0)
    if e == "btn1":
        janken(1)
    if e == "btn2":
        janken(2)
    if e == None:
        break
win.close()
