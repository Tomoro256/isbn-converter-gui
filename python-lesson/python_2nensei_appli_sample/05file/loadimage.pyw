import PySimpleGUI as sg
from PIL import Image
import io
sg.theme("DarkBrown3")

layout = [[sg.B(" ファイルを開く ", k="btn1"), sg.T(k="txt")],
          [sg.Im(k="img")]]
win = sg.Window("画像ファイルを表示", layout, size=(320,380))

def loadimage():
    loadname = sg.popup_get_file("画像ファイルを選択してください。")
    if not loadname:
        return
    try:
        img = Image.open(loadname)
        img.thumbnail((300,300))
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        win["img"].update(data=bio.getvalue())
        win["txt"].update(loadname)
    except:
        win["img"].update()
        win["txt"].update("失敗しました。")

while True:
    e, v = win.read()
    if e == "btn1":
      loadimage()
    if e == None:
        break
win.close()
