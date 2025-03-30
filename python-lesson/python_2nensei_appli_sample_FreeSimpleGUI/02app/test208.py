import FreeSimpleGUI as sg
sg.theme("DarkBrown3")

layout = [[sg.I("フタバ", k="in")],
          [sg.B("実行", k="btn")],
          [sg.T(k="txt")]]
win = sg.Window("あいさつテスト", layout,
                font=(None,14), size=(250,120))

def execute():
    txt = "こんにちは、"+v["in"] + "さん！"
    win["txt"].update(txt)
  
while True:
    e, v = win.read()
    if e == "btn":
      execute()
    if e == None:
        break
win.close()

