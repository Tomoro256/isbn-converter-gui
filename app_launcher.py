import requests
import os
import subprocess
import time

APP_NAME = "isbn_converter.exe"
LOCAL_VERSION = "0.0.1"  # ローカルのバージョン
GITHUB_USER = "Tomoro256"
GITHUB_REPO = "isbn-converter-gui"

def get_latest_release():
    url = f"https://github.com/Tomoro256/isbn-converter-gui/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["tag_name"], data["assets"][0]["browser_download_url"]
    except Exception as e:
        print("アップデート確認エラー:", e)
    return None, None

def download_new_version(url, filename):
    try:
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
    if latest_version and latest_version != f"v{LOCAL_VERSION}":
        print(f"新しいバージョン {latest_version} が見つかりました。更新します...")
        success = download_new_version(download_url, APP_NAME)
        if success:
            print("更新完了。アプリを起動します。")
        else:
            print("更新に失敗しました。")
    else:
        print("最新バージョンです。")

    # アプリ本体を起動
    if os.path.exists(APP_NAME):
        subprocess.Popen([APP_NAME])
    else:
        print(f"{APP_NAME} が見つかりません")

if __name__ == "__main__":
    main()
