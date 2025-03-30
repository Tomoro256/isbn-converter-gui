import FreeSimpleGUI as sg
sg.theme("DarkBrown3")

layout = [[sg.T("テキスト")],
          [sg.I("入力欄")],
          [sg.ML("複数行テキスト 1行目\n2行目", size=(30,3))],
          [sg.Im("futaba.png")]]
win = sg.Window("入力欄テスト", layout,
                font=(None,14), size=(300,240))

e, v = win.read()
win.close()
