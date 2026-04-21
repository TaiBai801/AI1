@echo off
chcp 65001 >nul
echo ========================================
echo    AI联谊匹配系统 - 启动脚本
echo ========================================
echo.

:: 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

:: 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Node.js，请先安装Node.js 16+
    pause
    exit /b 1
)

echo [1/4] 正在安装后端依赖...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 后端依赖安装失败
    pause
    exit /b 1
)

echo [2/4] 正在启动后端服务...
start "后端服务" cmd /k "python main.py"
cd ..

echo [3/4] 正在安装前端依赖...
cd frontend
npm install
if errorlevel 1 (
    echo [错误] 前端依赖安装失败
    pause
    exit /b 1
)

echo [4/4] 正在启动前端服务...
start "前端服务" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo    服务启动成功！
echo ========================================
echo.
echo 后端API: http://localhost:8000
echo 前端页面: http://localhost:3000
echo API文档: http://localhost:8000/docs
echo.
echo 按任意键打开浏览器...
pause >nul

start http://localhost:3000
