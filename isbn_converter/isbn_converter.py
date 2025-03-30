# ===== フォルダ内アイコン対応 最終版 isbn_converter.py（ランチャー） =====

import requests
import os
import subprocess
import sys
import FreeSimpleGUI as fsg

fsg.theme("SystemDefault1")
fsg.set_options(font=("Segoe UI", 10))

APP_DIR = "app"
APP_NAME = "isbn_gui.exe"
APP_PATH = os.path.join(APP_DIR, APP_NAME)
ICON_PATH = os.path.join(APP_DIR, "isbn_icon.ico")

GITHUB_USER = "Tomoro256"
GITHUB_REPO = "isbn-converter-gui"

def get_local_version():
    version_path = os.path.join(APP_DIR, "version.txt")
    try:
        with open(version_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "0.0.0"

LOCAL_VERSION = get_local_version()

def get_latest_release():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["tag_name"], data["assets"][0]["browser_download_url"]
        else:
            show_error_popup(f"GitHub API エラー: {response.status_code}")
    except requests.exceptions.ConnectionError:
        show_error_popup("インターネットに接続されていません。\nネットワークを確認してください。")
    except Exception as e:
        show_error_popup(f"アップデート確認エラー: {e}")
    return None, None

def download_new_version(url, filename, latest_version):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        r = requests.get(url, stream=True)
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        version_txt_path = os.path.join(os.path.dirname(filename), "version.txt")
        with open(version_txt_path, "w", encoding="utf-8") as vf:
            vf.write(latest_version.lstrip("v"))
        return True
    except Exception as e:
        show_error_popup(f"ダウンロード失敗: {e}")
        return False

def show_error_popup(message):
    layout = [
        [fsg.Text(message, justification='center')],
        [fsg.Push(), fsg.Button("OK", size=(10, 1), pad=(0, 10)), fsg.Push()]
    ]
    fsg.Window("アップデートエラー", layout, element_justification='center', finalize=True,
               keep_on_top=True, location=(None, None), icon=ICON_PATH).read(close=True)

def show_info_popup(message):
    layout = [
        [fsg.Text(message, justification='center')],
        [fsg.Push(), fsg.Button("OK", size=(10, 1), pad=(0, 10)), fsg.Push()]
    ]
    fsg.Window("アップデート", layout, element_justification='center', finalize=True,
               keep_on_top=True, location=(None, None), icon=ICON_PATH).read(close=True)

def main():
    latest_version, download_url = get_latest_release()

    if latest_version and latest_version != f"v{LOCAL_VERSION}":
        message = f"新しいバージョン {latest_version} をダウンロード中…"
        success = download_new_version(download_url, APP_PATH, latest_version)
        if success:
            message += "\nアップデート完了！"
            show_info_popup(message)
        else:
            return

    if os.path.exists(APP_PATH):
        subprocess.Popen([APP_PATH])
    else:
        show_error_popup(f"{APP_PATH} が見つかりません。起動できませんでした。")

if __name__ == "__main__":
    main()
