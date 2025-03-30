@echo off
title ISBNコンバータ ビルドメニュー
cd /d "%~dp0"

echo.
echo ==============================
echo ISBNコンバータ ビルドメニュー
echo ==============================
echo [1] 本体のみビルド（isbn_gui.exe）
echo [2] ランチャーのみビルド（isbn_converter.exe）
echo [3] 両方ビルド
echo [4] 終了
echo ==============================
set /p CHOICE=番号を入力してください: 

if exist isbn_gui.spec del /q isbn_gui.spec
if exist isbn_converter.spec del /q isbn_converter.spec

if "%CHOICE%"=="1" goto build_gui
if "%CHOICE%"=="2" goto build_launcher
if "%CHOICE%"=="3" goto build_all
if "%CHOICE%"=="4" exit

:build_gui
echo.
echo === 本体 (isbn_gui.py) をビルド中 ===
pyinstaller --onefile --windowed --name "isbn_gui" --icon=app\isbn_icon.ico --add-data "app\isbn_icon.ico;app" isbn_gui.py
goto write_version

:build_launcher
echo.
echo === ランチャー (isbn_converter.py) をビルド中 ===
pyinstaller --onefile --windowed --name "isbn_converter" --icon=app\isbn_icon.ico --add-data "app\isbn_icon.ico;app" isbn_converter.py
goto finish

:build_all
echo.
echo === 本体 (isbn_gui.py) をビルド中 ===
pyinstaller --onefile --windowed --name "isbn_gui" --icon=app\isbn_icon.ico --add-data "app\isbn_icon.ico;app" isbn_gui.py
echo.
echo === ランチャー (isbn_converter.py) をビルド中 ===
pyinstaller --onefile --windowed --name "isbn_converter" --icon=app\isbn_icon.ico --add-data "app\isbn_icon.ico;app" isbn_converter.py
goto write_version

:write_version
echo.
echo isbn_gui.py からバージョン番号を抽出中...
powershell -Command "Get-Content isbn_gui.py | ForEach-Object { if ($_ -like '*__version__ =*') { ($_ -split '\"')[1] } } > app\\version.txt"

set /p VERSION=<app\version.txt
echo 抽出されたバージョン: [%VERSION%]

if "%VERSION%"=="" (
    echo ※ バージョン番号が取得できませんでした。__version__ が定義されているか確認してください。
    goto finish
)

goto compare_versions

:compare_versions
echo.
echo GitHub の最新リリースと比較しています...

for /f "delims=" %%i in ('gh release view --repo Tomoro256/isbn-converter-gui --json tagName -q ".tagName" 2^>nul') do set LATEST_TAG=%%i

if "%LATEST_TAG%"=="" (
    echo リリースがまだ存在しません。v%VERSION% を初回リリースとして作成します。
    goto github_release
)

set "LATEST_VER=%LATEST_TAG:v=%"
echo GitHub上の最新リリース: [%LATEST_VER%]

powershell -Command "try { if ([version]'%VERSION%' -gt [version]'%LATEST_VER%') { exit 0 } else { exit 1 } } catch { exit 0 }"

if %ERRORLEVEL%==0 (
    echo 現在のバージョン [%VERSION%] は新しいため、リリースを作成します。
    goto github_release
) else (
    echo [%VERSION%] は最新と同じか古いため、リリースをスキップします。
    goto git_push
)

:github_release
echo.
if not exist "app\isbn_gui.exe" echo  ファイルが見つかりません: app\isbn_gui.exe
if not exist "app\version.txt" echo  ファイルが見つかりません: app\version.txt

echo GitHub にリリースを作成しています...
gh release create v%VERSION% "app\isbn_gui.exe" "app\version.txt" --title "v%VERSION%" --notes "自動ビルドリリース" --repo Tomoro256/isbn-converter-gui
goto git_push

:git_push
echo.
set /p PUSHOK=GitHub にソースコードを push しますか？ (Y/N): 
if /I "%PUSHOK%"=="Y" goto do_push
goto finish

:do_push
git add .
git commit -m "バージョン %VERSION% をリリース"
git push
goto finish

:finish
echo.
echo ビルド完了！dist フォルダを開きます。
start dist
pause
exit
