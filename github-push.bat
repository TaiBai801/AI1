@echo off
chcp 65001 >nul 2>&1

echo.
echo ========================================
echo   GitHub 登录与代码推送脚本
echo ========================================
echo.

echo [步骤 1/2] 登录 GitHub
echo 请按回车继续，浏览器会打开 GitHub 授权页面...
echo.
pause

"C:\Users\ASUS1\AppData\Local\GitHubCLI\Program Files\GitHub CLI\gh.exe" auth login -h github.com -p

if %errorlevel% neq 0 (
    echo.
    echo [错误] 登录失败，请重试
    pause
    exit /b 1
)

echo.
echo [步骤 2/2] 检查仓库
echo.

REM 设置仓库路径
set REPO_NAME=AI1
set USERNAME=TaiBai801

"C:\Users\ASUS1\AppData\Local\GitHubCLI\Program Files\GitHub CLI\gh.exe" repo view %USERNAME%/%REPO_NAME% 2>nul

if %errorlevel% neq 0 (
    echo 仓库不存在，正在创建...
    "C:\Users\ASUS1\AppData\Local\GitHubCLI\Program Files\GitHub CLI\gh.exe" repo create %REPO_NAME% --public --confirm
)

echo.
echo ========================================
echo   登录成功！现在开始推送代码...
echo ========================================
echo.

REM 切换到项目目录
cd /d "C:\Users\ASUS1\.qclaw\workspace\match-making-app"

REM 初始化 git（如果需要）
if not exist ".git" (
    git init
    git add .
    git commit -m "Initial commit: AI联谊匹配系统"
)

REM 设置远程仓库
git remote remove origin 2>nul
git remote add origin https://github.com/%USERNAME%/%REPO_NAME%.git

REM 推送代码
echo 正在推送代码到 GitHub...
git push -u origin master

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   推送成功！
    echo   仓库地址: https://github.com/%USERNAME%/%REPO_NAME%
    echo ========================================
) else (
    echo.
    echo [错误] 推送失败
)

echo.
pause