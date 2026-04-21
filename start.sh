#!/bin/bash

echo "========================================"
echo "   AI联谊匹配系统 - 启动脚本"
echo "========================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "[错误] 未找到Node.js，请先安装Node.js 16+"
    exit 1
fi

echo "[1/4] 正在安装后端依赖..."
cd backend
pip3 install -r requirements.txt || {
    echo "[错误] 后端依赖安装失败"
    exit 1
}

echo "[2/4] 正在启动后端服务..."
python3 main.py &
BACKEND_PID=$!
cd ..

echo "[3/4] 正在安装前端依赖..."
cd frontend
npm install || {
    echo "[错误] 前端依赖安装失败"
    kill $BACKEND_PID
    exit 1
}

echo "[4/4] 正在启动前端服务..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "   服务启动成功！"
echo "========================================"
echo ""
echo "后端API: http://localhost:8000"
echo "前端页面: http://localhost:3000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按Ctrl+C停止所有服务"

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
