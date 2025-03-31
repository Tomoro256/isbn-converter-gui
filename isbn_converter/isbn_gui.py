
import FreeSimpleGUI as fsg
import os
import sqlite3
from datetime import datetime, timedelta
import shutil

__version__ = "0.0.19"
ICON_PATH = os.path.join(os.path.dirname(__file__), "app", "isbn_icon.ico")
DB_PATH = r"G:\マイドライブ\ISBN履歴共有\data.db"
LOGS_DIR = "logs"

log_db_path = None


# --- SQLiteデータベースに接続する関数 ---
def get_connection():
    return sqlite3.connect(DB_PATH)


# --- ログイン履歴を login_logs テーブルに記録 ---
def record_login(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS login_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("INSERT INTO login_logs (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


# --- ISBN10 を ISBN13 に変換する関数 ---
def convert_isbn(isbn10: str) -> str:
    isbn10 = isbn10.strip().replace("-", "")
    if len(isbn10) != 10:
        raise ValueError(f"{isbn10} は10桁のISBNではありません")
    if not isbn10.startswith("4"):
        raise ValueError(f"{isbn10} は4で始まるISBNではありません")
    core = isbn10[:9]
    prefix = "978"
    digits_str = prefix + core
    digits = [int(ch) for ch in digits_str]
    total = sum(d if i % 2 == 0 else d * 3 for i, d in enumerate(digits))
    check_digit = (10 - (total % 10)) % 10
    return digits_str + str(check_digit)


# --- 複数のISBNを変換し、DBに保存 ---
def convert_isbn_list(isbn_list, user_id, is_admin):
    db_path = DB_PATH if is_admin else log_db_path
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    converted = []
    errors = []
    for isbn in isbn_list:
        try:
            isbn13 = convert_isbn(isbn)
            converted.append(isbn13)
            cur.execute("INSERT INTO conversions (user_id, isbn10, isbn13) VALUES (?, ?, ?)", (user_id, isbn, isbn13))
        except Exception as e:
            errors.append(str(e))
    conn.commit()
    conn.close()
    return converted, errors


# --- ログイン画面（ユーザー名/パスワードの入力GUI） ---
def show_login():

# --- GUIのレイアウト（画面構成） ---
    layout = [
        [fsg.Text("ユーザー名")],
        [fsg.Input(key="USER")],
        [fsg.Text("パスワード")],
        [fsg.Input(key="PASS", password_char="*")],
        [fsg.Button("ログイン"), fsg.Button("キャンセル")]
    ]
    win = fsg.Window("ログイン", layout, modal=True, icon=ICON_PATH)
    conn = get_connection()
    cur = conn.cursor()


# --- メインイベントループ（ボタンイベント処理） ---
    while True:
        event, values = win.read()
        if event in (fsg.WIN_CLOSED, "キャンセル"):
            win.close()
            return None, None
        username = values["USER"]
        password = values["PASS"]
        cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        if row:
            win.close()
            record_login(row[0])
            return row[0], username
        else:
            fsg.popup_error("ユーザー名またはパスワードが正しくありません", icon=ICON_PATH)


# --- 管理者用の変換履歴閲覧ウィンドウ ---
def show_admin_window():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT conversions.created_at, users.username, conversions.isbn10, conversions.isbn13
                   FROM conversions JOIN users ON conversions.user_id = users.id
                   ORDER BY conversions.created_at DESC""")
    
    from datetime import datetime, timedelta  # ファイル上部で1回だけでOK

    records = cur.fetchall()
    conn.close()

    headings = ["日時", "ユーザー名", "10桁ISBN", "13桁ISBN"]
    data = [
        [
            (datetime.fromisoformat(row[0]) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S"),
            row[1], row[2], row[3]
        ]
        for row in records
    ]


# --- GUIのレイアウト（画面構成） ---
    layout = [
        [fsg.Table(values=data, headings=headings, auto_size_columns=False, col_widths=[20, 12, 15, 15],
                   justification="left", num_rows=20, expand_x=True, expand_y=True)],
        [fsg.Button("閉じる", key="CLOSE")]
    ]
    win = fsg.Window("変換履歴（管理者専用）", layout, modal=True, icon=ICON_PATH, resizable=True)

# --- メインイベントループ（ボタンイベント処理） ---
    while True:
        ev, _ = win.read()
        if ev in (fsg.WIN_CLOSED, "CLOSE"):
            break
    win.close()


# --- 新規ユーザーを追加するGUI ---
def add_user_window():

# --- GUIのレイアウト（画面構成） ---
    layout = [
        [fsg.Text("新しいユーザー名")], [fsg.Input(key="NEW_USER")],
        [fsg.Text("パスワード")], [fsg.Input(key="NEW_PASS", password_char="*")],
        [fsg.Button("追加"), fsg.Button("キャンセル")]
    ]
    win = fsg.Window("ユーザー追加", layout, modal=True, icon=ICON_PATH)

# --- メインイベントループ（ボタンイベント処理） ---
    while True:
        ev, val = win.read()
        if ev in (fsg.WIN_CLOSED, "キャンセル"):
            break
        if ev == "追加":
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (val["NEW_USER"], val["NEW_PASS"]))
                conn.commit()
                fsg.popup("ユーザー追加成功", icon=ICON_PATH)
                break
            except sqlite3.IntegrityError:
                fsg.popup_error("そのユーザー名は既に存在します", icon=ICON_PATH)
            finally:
                conn.close()
    win.close()


# --- パスワード変更画面 ---
def change_password_window(username):

# --- GUIのレイアウト（画面構成） ---
    layout = [
        [fsg.Text("新しいパスワード")], [fsg.Input(key="NEW_PASS", password_char="*")],
        [fsg.Button("変更"), fsg.Button("キャンセル")]
    ]
    win = fsg.Window("パスワード変更", layout, modal=True, icon=ICON_PATH)

# --- メインイベントループ（ボタンイベント処理） ---
    while True:
        ev, val = win.read()
        if ev in (fsg.WIN_CLOSED, "キャンセル"):
            break
        if ev == "変更":
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET password=? WHERE username=?", (val["NEW_PASS"], username))
            conn.commit()
            conn.close()
            fsg.popup("パスワード変更完了", icon=ICON_PATH)
            break
    win.close()

# --- 管理者用：ログイン履歴をGUI表示する関数 ---
def show_login_logs_window():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT login_logs.login_at, users.username
        FROM login_logs
        JOIN users ON login_logs.user_id = users.id
        ORDER BY login_logs.login_at DESC
    """)
    records = cur.fetchall()
    conn.close()

    jst_records = [
        [
            (datetime.fromisoformat(r[0]) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S"),r[1]
        ]
        for r in records
    ]

    layout = [
        [fsg.Table(
            values=jst_records,
            headings=["ログイン日時", "ユーザー名"],
            auto_size_columns=False,
            col_widths=[25, 15],
            justification="left",
            num_rows=20
        )],
        [fsg.Button("閉じる", key="CLOSE")]
    ]
    win = fsg.Window("ログイン履歴", layout, modal=True, icon=ICON_PATH, resizable=True)
    while True:
        ev, _ = win.read()
        if ev in (fsg.WIN_CLOSED, "CLOSE"):
            break
    win.close()

# --- 管理者用：ユーザー管理画面（一覧・編集・削除） ---
def show_user_management_window():
    def load_users():
        cur.execute("SELECT id, username FROM users ORDER BY id")
        return cur.fetchall()

    conn = get_connection()
    cur = conn.cursor()

    users = load_users()
    user_list = [f"{u[0]}: {u[1]}" for u in users]

    layout = [
        [fsg.Listbox(user_list, size=(30, 10), key="USERLIST", enable_events=True)],
        [fsg.Button("パスワード変更"), fsg.Button("削除"), fsg.Button("閉じる")]
    ]
    win = fsg.Window("ユーザー管理", layout, modal=True, icon=ICON_PATH)

    while True:
        ev, val = win.read()
        if ev in (fsg.WIN_CLOSED, "閉じる"):
            break
        if ev in ("パスワード変更", "削除") and val["USERLIST"]:
            uid, uname = val["USERLIST"][0].split(": ")
            uid = int(uid)
            if ev == "削除":
                if uname == "admin":
                    fsg.popup_error("adminは削除できません", icon=ICON_PATH)
                    continue
                cur.execute("DELETE FROM users WHERE id=?", (uid,))
                conn.commit()
                fsg.popup("削除しました", icon=ICON_PATH)
            elif ev == "パスワード変更":
                pw = fsg.popup_get_text(f"{uname} の新しいパスワードを入力", password_char="*", icon=ICON_PATH)
                if pw:
                    cur.execute("UPDATE users SET password=? WHERE id=?", (pw, uid))
                    conn.commit()
                    fsg.popup("変更しました", icon=ICON_PATH)
            users = load_users()
            win["USERLIST"].update(values=[f"{u[0]}: {u[1]}" for u in users])

    conn.close()
    win.close()


# ---------- GUI ----------
fsg.theme("SystemDefault1")
fsg.set_options(font=("Segoe UI", 10))

user_id, username = show_login()
if user_id is None:
    exit()

is_admin = (username == "admin")

# --- 管理者ログイン時に Googleドライブ内 logs/*.db を data.db に統合 ---
if is_admin:
    def merge_logs_from_gdrive():
        GDRIVE_LOG_PATH = r"G:\マイドライブ\ISBN履歴共有\logs"
        if not os.path.exists(GDRIVE_LOG_PATH):
            return
        conn = get_connection()
        cur = conn.cursor()
        merged = 0
        for file in os.listdir(GDRIVE_LOG_PATH):
            if file.endswith(".db"):
                path = os.path.join(GDRIVE_LOG_PATH, file)
                try:
                    log_conn = sqlite3.connect(path)
                    log_cur = log_conn.cursor()
                    log_cur.execute("SELECT user_id, isbn10, isbn13, created_at FROM conversions")
                    rows = log_cur.fetchall()
                    log_conn.close()
                    for row in rows:
                        cur.execute("INSERT INTO conversions (user_id, isbn10, isbn13, created_at) VALUES (?, ?, ?, ?)", row)
                    os.remove(path)
                    merged += 1
                except Exception as e:
                    print(f"{file} の統合に失敗: {e}")
        conn.commit()
        conn.close()
        print(f"{merged} 件のログを Googleドライブから統合しました。")

    merge_logs_from_gdrive()

if not is_admin:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    log_db_path = os.path.join(LOGS_DIR, f"{username}_{timestamp}.db")
    conn = sqlite3.connect(log_db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            isbn10 TEXT NOT NULL,
            isbn13 TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# --- GUIのレイアウト（画面構成） ---
layout = [
    [fsg.Text(f"ISBN変換アプリ v{__version__}", font=("Segoe UI", 14, "bold"), justification="center", expand_x=True)],
    [
        fsg.Column([[fsg.Text("10桁ISBN")], [fsg.Multiline(key="INPUT", size=(22, 10))]]),
        fsg.Column([[fsg.Text("13桁ISBN")], [fsg.Multiline(key="OUTPUT", size=(22, 10), disabled=True)]]),
        fsg.Column([[fsg.Text("エラー")], [fsg.Multiline(key="ERROR", size=(38, 10), disabled=True, text_color="red")]]),
    ],
    [fsg.HorizontalSeparator()],
    [
        fsg.Push(),
        fsg.Button("ファイル読み込み", key="LOAD"),
        fsg.Button("変換開始", key="CONVERT"),
        fsg.Button("CSV出力", key="SAVE"),
        fsg.Button("クリア", key="CLEAR"),
        fsg.Button("終了", key="EXIT")
    ]
]

if is_admin:
    layout[-1].insert(-2, fsg.Button("管理画面", key="ADMIN"))
    layout[-1].insert(-2, fsg.Button("ユーザー追加", key="ADDUSER"))
    layout[-1].insert(-2, fsg.Button("ログイン履歴", key="LOGS"))
    layout[-1].insert(-2, fsg.Button("ユーザー管理", key="USERMGR"))

layout[-1].insert(-2, fsg.Button("パスワード変更", key="CHANGEPW"))

window = fsg.Window(f"ISBN変換アプリ v{__version__}", layout, resizable=False, icon=ICON_PATH)


# --- メインイベントループ（ボタンイベント処理） ---
while True:
    event, values = window.read()
    if event in (fsg.WIN_CLOSED, "EXIT"):
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
        converted, errors = convert_isbn_list(isbn_list, user_id, is_admin)
        window["OUTPUT"].update("\n".join(converted))
        window["ERROR"].update("\n".join(errors))

    elif event == "SAVE":
        filename = fsg.filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for line in values["OUTPUT"].splitlines():
                        f.write(line + "\n")
                fsg.popup("保存しました", icon=ICON_PATH)
            except Exception as ex:
                fsg.popup_error(f"保存エラー: {ex}")

    elif event == "CLEAR":
        window["INPUT"].update("")
        window["OUTPUT"].update("")
        window["ERROR"].update("")

    elif event == "ADMIN":
        show_admin_window()

    elif event == "ADDUSER":
        add_user_window()

    elif event == "LOGS":
        show_login_logs_window()

    elif event == "USERMGR":
        show_user_management_window()

    elif event == "CHANGEPW":
        change_password_window(username)

window.close()

# --- 一般ユーザーのログをGoogleドライブに送信 ---
if not is_admin and log_db_path:
    try:
        GDRIVE_LOG_PATH = r"G:\マイドライブ\ISBN履歴共有\logs"
        if not os.path.exists(GDRIVE_LOG_PATH):
            os.makedirs(GDRIVE_LOG_PATH)
        dest = os.path.join(GDRIVE_LOG_PATH, os.path.basename(log_db_path))
        shutil.copy2(log_db_path, dest)
        print(f"ログをGoogleドライブに送信しました：{dest}")
    except Exception as e:
        print(f"Googleドライブ送信エラー: {e}")


