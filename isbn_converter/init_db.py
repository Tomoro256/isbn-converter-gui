import sqlite3
import os

# Googleドライブの data.db のパス
DB_PATH = r"G:\マイドライブ\ISBN履歴共有\data.db"

def init_db():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # users テーブル作成
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # conversions テーブル作成
    cur.execute("DROP TABLE IF EXISTS conversions")
    cur.execute("""
        CREATE TABLE conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            isbn10 TEXT NOT NULL,
            isbn13 TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # 初期ユーザー追加（パスワードを pass1234 に設定）
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "pass1234"))
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user1", "pass1234"))

    conn.commit()
    conn.close()
    print(f"初期化完了: {DB_PATH}")

if __name__ == "__main__":
    init_db()
