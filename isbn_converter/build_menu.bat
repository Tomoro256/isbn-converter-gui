@echo off
title ISBN�R���o�[�^ �r���h���j���[
cd /d "%~dp0"

echo.
echo ==============================
echo ISBN�R���o�[�^ �r���h���j���[
echo ==============================
echo [1] �{�̂̂݃r���h�iisbn_gui.exe�j
echo [2] �����`���[�̂݃r���h�iisbn_converter.exe�j
echo [3] �����r���h
echo [4] �I��
echo ==============================
set /p CHOICE=�ԍ�����͂��Ă�������: 

if exist isbn_gui.spec del /q isbn_gui.spec
if exist isbn_converter.spec del /q isbn_converter.spec

if "%CHOICE%"=="1" goto build_gui
if "%CHOICE%"=="2" goto build_launcher
if "%CHOICE%"=="3" goto build_all
if "%CHOICE%"=="4" exit

:build_gui
echo.
echo === �{�� (isbn_gui.py) ���r���h�� ===
pyinstaller --onefile --windowed --name "isbn_gui" --icon=app\isbn_icon.ico --add-data "app\isbn_icon.ico;app" isbn_gui.py
goto write_version

:build_launcher
echo.
echo === �����`���[ (isbn_converter.py) ���r���h�� ===
pyinstaller --onefile --windowed --name "isbn_converter" --icon=app\isbn_icon.ico --add-data "app\isbn_icon.ico;app" isbn_converter.py
goto finish

:build_all
echo.
echo === �{�� (isbn_gui.py) ���r���h�� ===
pyinstaller --onefile --windowed --name "isbn_gui" --icon=app\isbn_icon.ico --add-data "app\isbn_icon.ico;app" isbn_gui.py
echo.
echo === �����`���[ (isbn_converter.py) ���r���h�� ===
pyinstaller --onefile --windowed --name "isbn_converter" --icon=app\isbn_icon.ico --add-data "app\isbn_icon.ico;app" isbn_converter.py
goto write_version

:write_version
echo.
echo isbn_gui.py ����o�[�W�����ԍ��𒊏o��...
powershell -Command "Get-Content isbn_gui.py | ForEach-Object { if ($_ -like '*__version__ =*') { ($_ -split '\"')[1] } } > app\\version.txt"

set /p VERSION=<app\version.txt
echo ���o���ꂽ�o�[�W����: [%VERSION%]

if "%VERSION%"=="" (
    echo �� �o�[�W�����ԍ����擾�ł��܂���ł����B__version__ ����`����Ă��邩�m�F���Ă��������B
    goto finish
)

goto compare_versions

:compare_versions
echo.
echo GitHub �̍ŐV�����[�X�Ɣ�r���Ă��܂�...

for /f "delims=" %%i in ('gh release view --repo Tomoro256/isbn-converter-gui --json tagName -q ".tagName" 2^>nul') do set LATEST_TAG=%%i

if "%LATEST_TAG%"=="" (
    echo �����[�X���܂����݂��܂���Bv%VERSION% �����񃊃��[�X�Ƃ��č쐬���܂�.

    REM �� ������ dist\app �Ƀt�@�C��������
    if not exist dist\app mkdir dist\app
    copy /Y dist\isbn_gui.exe dist\app\
    copy /Y app\version.txt dist\app\

    goto github_release
)

set "LATEST_VER=%LATEST_TAG:v=%"
echo GitHub��̍ŐV�����[�X: [%LATEST_VER%]

powershell -Command "try { if ([version]'%VERSION%' -gt [version]'%LATEST_VER%') { exit 0 } else { exit 1 } } catch { exit 0 }"

if %ERRORLEVEL%==0 (
    echo ���݂̃o�[�W���� [%VERSION%] �͐V�������߁A�����[�X���쐬���܂�.

    REM �� ������ dist\app �Ƀt�@�C��������
    if not exist dist\app mkdir dist\app
    copy /Y dist\isbn_gui.exe dist\app\
    copy /Y app\version.txt dist\app\

    goto github_release
) else (
    echo [%VERSION%] �͍ŐV�Ɠ������Â����߁A�����[�X���X�L�b�v���܂��B
    goto git_push
)

:github_release
echo.
if not exist "dist\app\isbn_gui.exe" echo  �t�@�C����������܂���: dist\app\isbn_gui.exe
if not exist "dist\app\version.txt" echo  �t�@�C����������܂���: dist\app\version.txt

echo GitHub �Ƀ����[�X���쐬���Ă��܂�...
gh release create v%VERSION% "dist\app\isbn_gui.exe" "dist\app\version.txt" --title "v%VERSION%" --notes "�����r���h�����[�X" --repo Tomoro256/isbn-converter-gui
goto git_push

:git_push
echo.
set /p PUSHOK=GitHub �Ƀ\�[�X�R�[�h�� push ���܂����H (Y/N): 
if /I "%PUSHOK%"=="Y" goto do_push
goto zip_package

:do_push
git add .
git commit -m "�o�[�W���� %VERSION% �������[�X"
git push
goto zip_package

:zip_package
echo.
echo �z�z�p�t�H���_���쐬��...

if not exist dist\app mkdir dist\app
copy /Y dist\isbn_gui.exe dist\app\
copy /Y app\version.txt dist\app\
copy /Y app\isbn_icon.ico dist\app\

echo.
echo ZIP�t�@�C�����쐬��...

cd dist
if exist isbn_converter.zip del /q isbn_converter.zip
powershell -Command "Compress-Archive -Path 'isbn_converter.exe','app' -DestinationPath 'isbn_converter.zip'"

echo.
echo ZIP�쐬�����Bdist\app ���폜���܂�...
rmdir /s /q app

echo.
echo �쐬����: isbn_converter.zip
start .
cd ..
pause
exit
