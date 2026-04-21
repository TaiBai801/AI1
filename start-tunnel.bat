@echo off
chcp 65001 >nul
echo ==========================================
echo   AI联谊匹配系统 - Cloudflare Tunnel启动脚本
echo ==========================================
echo.

REM 检查 cloudflared 是否存在
if not exist "cloudflared.exe" (
    echo [错误] 未找到 cloudflared.exe
    echo.
    echo 请按以下步骤操作：
    echo 1. 访问 https://github.com/cloudflare/cloudflared/releases/latest
    echo 2. 下载 cloudflared-windows-amd64.exe
    echo 3. 将下载的文件重命名为 cloudflared.exe
    echo 4. 把 cloudflared.exe 放到这个文件夹
    echo.
    echo 或者使用手机热点方案（最简单）：
    echo - 手机开热点，电脑和其他设备都连上
    echo - 访问 http://[电脑IP]:3000
    pause
    exit /b 1
)

echo [1/3] 检查服务状态...

REM 检查后端服务
curl -s http://localhost:8000/ >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 后端服务未启动，正在启动...
    start "后端服务" cmd /c "cd backend && python main.py"
    timeout /t 3 /nobreak >nul
)

REM 检查前端服务
curl -s http://localhost:3000/ >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 前端服务未启动，正在启动...
    start "前端服务" cmd /c "cd frontend && npm run dev"
    timeout /t 5 /nobreak >nul
)

echo [2/3] 正在创建公网隧道...
echo.
echo ==========================================
echo   请等待，首次使用需要授权...
echo   会弹出一个网页，点击"Authorize"即可
echo ==========================================
echo.

REM 启动隧道
cloudflared.exe tunnel --url http://localhost:3000

pause
