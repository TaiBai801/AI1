# AI联谊匹配系统 - 快速启动指南

## 环境要求

- Python 3.8+
- Node.js 16+
- Windows / macOS / Linux

## 快速启动

### 1. 启动后端服务

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端服务将在 http://localhost:8000 启动

API文档：http://localhost:8000/docs

### 2. 启动前端服务

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 启动

### 3. 访问应用

打开浏览器访问 http://localhost:3000

## 功能说明

### 用户端

1. **首页** - 查看活动统计和介绍
2. **问卷填写** - 完成20道MBTI人格测试题
3. **结果查看** - 查看人格分析报告

### 管理端

1. **概览统计** - 查看报名人数、匹配率、人格类型分布
2. **参与者管理** - 查看、删除参与者信息
3. **匹配管理** - 执行AI匹配算法，查看匹配结果

## 匹配算法说明

### 人格分类模型

系统采用简化版MBTI模型，4维度8类型：

| 维度 | 类型A | 类型B |
|------|-------|-------|
| 能量来源 | E(外向) | I(内向) |
| 信息获取 | S(实感) | N(直觉) |
| 决策方式 | T(思考) | F(情感) |
| 生活方式 | J(判断) | P(感知) |

### 匹配分数计算

匹配分数 = 人格类型相似度(40%) + 兴趣标签匹配度(40%) + 最佳类型组合(20%)

### 匹配模式

1. **同好匹配** - 相似人格类型优先配对
2. **互补匹配** - 差异人格类型优先配对

### 最优配对算法

使用 NetworkX 的最大权匹配算法，确保：
- 全局最优配对
- 每人只配一人
- 无重复、无遗漏

## 数据存储

数据存储在 SQLite 数据库中 (`backend/matchmaking.db`)

## 打包为EXE（可选）

### 后端打包

```bash
cd backend
pip install pyinstaller
pyinstaller --onefile --add-data "matchmaking.db;." main.py
```

### 前端打包

```bash
cd frontend
npm run build
```

打包后的文件在 `frontend/dist` 目录

## 生产部署

### 使用Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["python", "main.py"]
```

### 使用Gunicorn

```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 常见问题

### 1. 后端启动失败

检查端口8000是否被占用：
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

### 2. 前端无法连接后端

检查 `frontend/vite.config.js` 中的代理配置：
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

### 3. 数据库权限错误

确保有写入权限，或修改 `database.py` 中的数据库路径。

## 技术栈

- **后端**: Python + FastAPI + SQLAlchemy + NetworkX
- **前端**: Vue 3 + Vite + Element Plus
- **数据库**: SQLite

## 扩展建议

1. **添加用户认证** - 使用JWT保护管理端
2. **邮件通知** - 匹配完成后发送邮件通知
3. **批量导入** - 支持Excel批量导入参与者
4. **实时通信** - 使用WebSocket实现实时匹配结果推送
5. **数据导出** - 支持导出匹配结果为Excel/PDF
