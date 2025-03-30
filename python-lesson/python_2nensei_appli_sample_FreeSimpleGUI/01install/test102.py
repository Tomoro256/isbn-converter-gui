import FreeSimpleGUI as sg

layout = [[sg.T(k="txt")],
          [sg.B("実行", k="btn")]]
win = sg.Window("こんにちはテスト", layout, size=(200,100))

def execute():
    win["txt"].update("こんにちは。")

while True:
    e, v = win.read()
    if e == "btn":
        execute()
    if e == None:
        break
win.close()
