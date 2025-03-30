import requests
import os
import subprocess
import sys

APP_DIR = "app"
APP_NAME = "isbn_gui.exe"  # 👈 本体の新しい名前
APP_PATH = os.path.join(APP_DIR, APP_NAME)

GITHUB_USER = "Tomoro256"
GITHUB_REPO = "isbn-converter-gui"

def get_local_version():
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        version_path = os.path.join(base_path, "app", "version.txt")
        with open(version_path, "r") as f:
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
            print(f"GitHub API エラー: {response.status_code}")
    except Exception as e:
        print("アップデート確認エラー:", e)
    return None, None

def download_new_version(url, filename):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        r = requests.get(url, stream=True)
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print("ダウンロード失敗:", e)
        return False

def main():
    print("アップデート確認中...")
    latest_version, download_url = get_latest_release()
    print("取得したバージョン:", latest_version)

    needs_update = False

    if not os.path.exists(APP_PATH):
        print(f"{APP_PATH} が存在しません。ダウンロードします。")
        needs_update = True
    elif latest_version and latest_version != f"v{LOCAL_VERSION}":
        print(f"新しいバージョン {latest_version} が見つかりました。更新します...")
        needs_update = True
    else:
        print("最新バージョンです。")

    if needs_update and download_url:
        success = download_new_version(download_url, APP_PATH)
        if success:
            print("ダウンロード完了。アプリを起動します。")
        else:
            print("ダウンロードに失敗しました。")

    if os.path.exists(APP_PATH):
        subprocess.Popen([APP_PATH])
    else:
        print(f"{APP_PATH} が見つかりません。起動できませんでした。")

if __name__ == "__main__":
    main()
