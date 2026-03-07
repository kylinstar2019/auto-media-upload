@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   Social Auto Upload GUI 构建脚本
echo ========================================
echo.

echo [1/6] 生成应用图标...
python generate_icon.py
echo.

echo [2/6] 构建前端...
cd sau_frontend
call npm install
call npm run build
cd ..
echo.

echo [3/6] 初始化数据库...
python db\createTable.py
echo.

echo [4/6] 清理旧构建...
if exist dist\SocialAutoUpload rmdir /s /q dist\SocialAutoUpload
if exist build rmdir /s /q build
echo.

echo [5/6] 打包应用 (这可能需要几分钟)...
pyinstaller sau_gui.spec --clean
echo.

echo [6/6] 复制额外资源...
if not exist "dist\SocialAutoUpload\db" mkdir "dist\SocialAutoUpload\db"
if not exist "dist\SocialAutoUpload\cookiesFile" mkdir "dist\SocialAutoUpload\cookiesFile"
if not exist "dist\SocialAutoUpload\videoFile" mkdir "dist\SocialAutoUpload\videoFile"
if not exist "dist\SocialAutoUpload\videos" mkdir "dist\SocialAutoUpload\videos"
if not exist "dist\SocialAutoUpload\logs" mkdir "dist\SocialAutoUpload\logs"
if not exist "dist\SocialAutoUpload\media" mkdir "dist\SocialAutoUpload\media"

if exist db\database.db copy /Y "db\database.db" "dist\SocialAutoUpload\db\database.db"
copy /Y conf.example.py dist\SocialAutoUpload\conf.py

echo.
echo ========================================
echo   构建完成!
echo   输出目录: dist\SocialAutoUpload\
echo   运行: dist\SocialAutoUpload\SocialAutoUpload.exe
echo ========================================
pause
