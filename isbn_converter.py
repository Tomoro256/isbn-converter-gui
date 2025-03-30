import FreeSimpleGUI as fsg

fsg.theme("SystemDefault1")
fsg.set_options(font=("Segoe UI", 10))

def convert_isbn(isbn10: str) -> str:
    isbn10 = isbn10.strip()
    isbn10 = isbn10.replace("-", "")  # ← ハイフンを削除

    if len(isbn10) != 10:
        raise ValueError(f"{isbn10}は10桁のISBNではありません")
    if not isbn10.startswith("4"):
        raise ValueError(f"{isbn10}は4で始まるISBNではありません")
    
    core = isbn10[:9]
    prefix = "978"
    digits_str = prefix + core
    try:
        digits = [int(ch) for ch in digits_str]
    except ValueError:
        raise ValueError(f"{isbn10}に数字以外の文字が含まれています")
    
    total = sum(d if i % 2 == 0 else d * 3 for i, d in enumerate(digits))
    check_digit = (10 - (total % 10)) % 10
    return digits_str + str(check_digit)


def convert_isbn_list(isbn_list):
    converted = []
    errors = []
    for isbn in isbn_list:
        isbn = isbn.strip()
        if isbn == "":
            continue
        try:
            converted.append(convert_isbn(isbn))
        except ValueError as e:
            errors.append(str(e))
    return converted, errors

# 📐 整然としたミニマルな縦ラベル＋欄の配置
# レイアウト定義部分（更新済）
layout = [
    [fsg.Text("ISBN変換ツール", font=("Segoe UI", 14, "bold"), justification="center", expand_x=True)],

    [
        fsg.Column([
            [fsg.Text("10桁ISBN", justification="left")],
            [fsg.Multiline(key="INPUT", size=(22, 10), border_width=1)],
        ], element_justification="left", pad=(5, 5)),

        fsg.Column([
            [fsg.Text("13桁ISBN", justification="left")],
            [fsg.Multiline(key="OUTPUT", size=(22, 10), disabled=True, border_width=1)],  # 👈 同じ幅に修正
        ], element_justification="left", pad=(5, 5)),

        fsg.Column([
            [fsg.Text("エラー", justification="left")],
            [fsg.Multiline(key="ERROR", size=(38, 10), disabled=True, text_color="#cc0000", border_width=1)],  # 👈 幅広く修正
        ], element_justification="left", pad=(5, 5)),
    ],


    [fsg.HorizontalSeparator(pad=(5, 10))],

    # 操作ボタン
    [
        fsg.Push(),
        fsg.Button("ファイル読み込み", key="LOAD", size=(14, 1)),
        fsg.Button("変換開始", key="CONVERT", size=(10, 1)),
        fsg.Button("CSV出力", key="SAVE", size=(10, 1)),
        fsg.Button("クリア", key="CLEAR", size=(8, 1)),
        fsg.Button("終了", key="EXIT", size=(8, 1))
    ]
]

window = fsg.Window("ISBN変換アプリ（ミニマルUI）", layout, resizable=False, element_padding=(8, 6))

while True:
    event, values = window.read()
    if event in (None, "EXIT"):
        break

    if event == "LOAD":
        filename = fsg.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = f.read()
                window["INPUT"].update(data)
            except Exception as ex:
                fsg.popup_error(f"ファイル読み込みエラー: {ex}")

    elif event == "CONVERT":
        isbn_list = values["INPUT"].splitlines()
        converted, error_msgs = convert_isbn_list(isbn_list)
        window["OUTPUT"].update("\n".join(converted))
        window["ERROR"].update("\n".join(error_msgs))

    elif event == "SAVE":
        filename = fsg.filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for line in values["OUTPUT"].splitlines():
                        f.write(line + "\n")
                fsg.popup("CSVファイルに保存しました。")
            except Exception as ex:
                fsg.popup_error(f"ファイル保存エラー: {ex}")

    elif event == "CLEAR":
        window["INPUT"].update("")
        window["OUTPUT"].update("")
        window["ERROR"].update("")

window.close()
