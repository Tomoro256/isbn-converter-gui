import PySimpleGUI as sg
sg.theme("DarkBrown3")

layout = [[sg.T("あなたの出生の秘密をお答えしましょう。")],
          [sg.T("あなたは何歳?"),sg.I("18", k="in1")],
          [sg.T("お母さんは何歳?"),sg.I("48", k="in2")],
          [sg.B(" 実行 ", k="btn")],
          [sg.T(k="txt")]]
win = sg.Window("出生の秘密アプリ", layout,
                font=(None,14), size=(420,170))

def execute():
    in1 = int(v["in1"])
    in2 = int(v["in2"])
    txt = f"お母さんが{in2 - in1}歳のとき、あなたを産みましたよ。"
    win["txt"].update(txt)

while True:
    e, v = win.read()
    if e == "btn":
      execute()
    if e == None:
        break
win.close()
