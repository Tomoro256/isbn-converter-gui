import FreeSimpleGUI as sg
from pathlib import Path
import chardet 
sg.theme("DarkBrown3")

layout = [[sg.B(" ファイルを開く ", k="btn1"), sg.T(k="txt1")],
          [sg.B(" ファイルを保存 ", k="btn2")],
          [sg.ML(k="txt2", font=(None,14), size=(80,15))]]
win = sg.Window("テキストファイルの保存", layout, resizable=True)

loadname = None
enc = "UTF-8"
def loadtext():
    global loadname, enc
    loadname = sg.popup_get_file("テキストファイルを選択してください。")
    if not loadname:
        return
    with open(loadname, "rb") as f:
        b = f.read()
        enc = chardet.detect(b)["encoding"]
        p = Path(loadname)
        txt = p.read_text(encoding = enc)
        win["txt1"].update(loadname)
        win["txt2"].update(txt)

def savetext():
    global loadname, enc
    savename = sg.popup_get_file("名前をつけて保存してください。",
                              default_path = loadname, save_as=True)
    if not savename:
        sg.PopupTimed("ファイル名を入力してください。")
        return
    if savename.find(".") == -1:
        savename = savename + ".txt"
    p = Path(savename)
    p.write_text(v["txt2"], encoding=enc)
    win["txt1"].update(savename)
    loadname = savename

while True:
    e, v = win.read()
    if e == "btn1":
        loadtext()
    if e == "btn2":
        savetext()
    if e == None:
        break
win.close()
