import FreeSimpleGUI as sg
sg.theme("DarkBrown3")

layout = [[sg.T("1行1列目"), sg.T("1行2列目")],
          [sg.T("2行1列目"), sg.T("2行2列目")],
          [sg.T("3行1列目"), sg.B("ボタン")]]
win = sg.Window("要素レイアウトテスト", layout,
                font=(None,14), size=(200,120))

e, v = win.read()
win.close()