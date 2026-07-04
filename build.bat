@echo off
title Building MoodSpace_Wallpaper.exe

echo.
echo ============================================
echo   Building MoodSpace_Wallpaper...
echo ============================================
echo.

REM Clean previous build/dist folders
if exist build (
    echo Removing old build folder...
    rmdir /s /q build
)
if exist dist (
    echo Removing old dist folder...
    rmdir /s /q dist
)

if exist MoodSpace_Wallpaper.spec (
    echo Removing old spec file...
    del MoodSpace_Wallpaper.spec
)

echo Running PyInstaller...
py gen_version.py
pyinstaller --onefile --noconsole --name MoodSpace_Wallpaper main.py --hidden-import requests --hidden-import packaging --icon=resources/butzy.ico --add-data "resources/butzy.ico;resources"

echo.
echo Copying settings.json and config folder to dist...
copy /Y .\resources\settings_template.json dist\settings.json
xcopy config dist\config\ /E /I /Y

echo.
echo ============================================
echo   Build completed!
echo   Your file is here: dist\MoodSpace_Wallpaper.exe
echo   Config files have been copied next to the EXE.
echo ============================================
echo.