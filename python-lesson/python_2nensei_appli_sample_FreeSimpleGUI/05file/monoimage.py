import FreeSimpleGUI as sg
from PIL import Image
import io
sg.theme("DarkBrown3")

layout = [[sg.B(" ファイルを開く ", k="btn1"),sg.T(k="txt")],
          [sg.B(" ファイルを保存 ", k="btn2")],
          [sg.Im(k="img")]]
win = sg.Window("モノクロ画像に変換", layout, size=(320,400))

def loadimage():
    global img
    loadname = sg.popup_get_file("画像ファイルを選択してください。")
    if not loadname:
        return
    try:
        img = Image.open(loadname).convert("L")
        img2 = img.copy()
        img2.thumbnail((300,300))
        bio = io.BytesIO()
        img2.save(bio, format="PNG")
        win["img"].update(data=bio.getvalue())
        win["txt"].update(loadname)
    except:
        win["img"].update()
        win["txt"].update("失敗しました。")

img = None
def saveimage():
    if img == None:
      return
    savename = sg.popup_get_file("png画像名をつけて保存してください。", save_as=True)
    if not savename:
        sg.PopupTimed("png画像名を入力してください。")
        return
    if savename.endswith(".png") == False:
        savename = savename + ".png"
    try:
        img.save(savename)
        win["txt"].update(savename+"を保存しました。")
    except:
        win["txt"].update("失敗しました。")

while True:
    e, v = win.read()
    if e == "btn1":
      loadimage()
    if e == "btn2":
      saveimage()
    if e == None:
        break
win.close()
