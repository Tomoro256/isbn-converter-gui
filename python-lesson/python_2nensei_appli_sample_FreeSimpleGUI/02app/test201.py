import FreeSimpleGUI as sg

layout = [[sg.Input("フタバ")],
          [sg.Button("実行")],
          [sg.Text("こんにちは")]]
window = sg.Window("テスト", layout)

event, values = window.read()
window.close()
