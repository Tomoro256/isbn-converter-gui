import PySimpleGUI as sg

choices = sg.theme_list()

layout = [[sg.T("どのテーマを表示しますか？")],
        [sg.Listbox(choices, size=(20, 16), font=("Arial",12),
          k="COLLIST", enable_events=True)]]
win = sg.Window("テーマ選択アプリ", layout)

def execute():
    tname = v["COLLIST"][0]
    sg.theme(tname)
    sg.popup_get_text("テーマカラー名", 
          font=(None,14), size=(40,80), default_text=tname)

while True:
    e, v = win.read()
    if e == "COLLIST":
        execute()
    if e == None:
        break
win.close()
