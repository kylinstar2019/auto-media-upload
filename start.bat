@echo off
chcp 65001 >nul 2>&1
TITLE Social Auto Upload - 一键启动

color 0A

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

echo.
echo ================================================================
echo        Social Auto Upload - 多平台社交媒体自动上传工具
echo ================================================================
echo.

echo [1/5] 检查必要文件夹...

if not exist "%ROOT_DIR%videoFile" (
    echo      创建 videoFile 文件夹...
    mkdir "%ROOT_DIR%videoFile"
)

if not exist "%ROOT_DIR%cookiesFile" (
    echo      创建 cookiesFile 文件夹...
    mkdir "%ROOT_DIR%cookiesFile"
)

if not exist "%ROOT_DIR%logs" (
    echo      创建 logs 文件夹...
    mkdir "%ROOT_DIR%logs"
)

echo      [OK] 文件夹检查完成

echo.
echo [2/5] 检查数据库...

if not exist "%ROOT_DIR%db\database.db" (
    echo      初始化数据库...
    cd /d "%ROOT_DIR%db"
    python createTable.py
    cd /d "%ROOT_DIR%"
    echo      [OK] 数据库初始化完成
) else (
    echo      [OK] 数据库已存在
)

echo.
echo [3/5] 检查配置文件...

if not exist "%ROOT_DIR%conf.py" (
    if exist "%ROOT_DIR%conf.example.py" (
        echo      从 conf.example.py 创建 conf.py...
        copy "%ROOT_DIR%conf.example.py" "%ROOT_DIR%conf.py" >nul
        echo      [OK] 配置文件已创建
        echo.
        echo      [!] 请编辑 conf.py 配置 LOCAL_CHROME_PATH
        echo      [!] 例如: LOCAL_CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        echo.
    ) else (
        echo      [ERROR] 找不到 conf.example.py
        pause
        exit /b 1
    )
) else (
    echo      [OK] 配置文件已存在
)

echo.
echo [4/5] 检查前端依赖...

if not exist "%ROOT_DIR%sau_frontend\node_modules" (
    echo      安装前端依赖，请稍候...
    cd /d "%ROOT_DIR%sau_frontend"
    call npm install
    cd /d "%ROOT_DIR%"
    echo      [OK] 前端依赖安装完成
) else (
    echo      [OK] 前端依赖已存在
)

echo.
echo [5/5] 启动服务...
echo.

echo      启动后端服务 (端口 5409)...
start "SAU Backend" cmd /k "cd /d %ROOT_DIR% && python sau_backend.py"

echo      等待后端启动...
timeout /t 3 /nobreak >nul

echo      启动前端服务 (端口 5173)...
start "SAU Frontend" cmd /k "cd /d %ROOT_DIR%sau_frontend && npm run dev"

echo      等待前端启动...
timeout /t 5 /nobreak >nul

echo.
echo ================================================================
echo                      启动完成!
echo ================================================================
echo.
echo   后端服务: http://localhost:5409
echo   前端界面: http://localhost:5173
echo.
echo   提示:
echo   - 两个新窗口已打开，请勿关闭
echo   - 在浏览器中打开前端界面即可使用
echo   - 关闭此窗口不影响服务运行
echo.
echo ================================================================
echo.

set /p OPEN_BROWSER="是否打开浏览器? (Y/N): "
if /i "%OPEN_BROWSER%"=="Y" (
    start http://localhost:5173
)

echo.
echo 按任意键关闭此窗口...
pause >nul
