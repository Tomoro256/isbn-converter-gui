import PySimpleGUI as sg

loadname = sg.popup_get_file("テキストファイルを選択してください。")
print(loadname)