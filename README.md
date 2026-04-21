# AI标签匹配联谊程序 - MBTI式人格匹配系统

## 项目概述

基于问卷的MBTI式人格分类与智能匹配系统，支持500人规模的两两最优配对。

## 核心特性

- **人格问卷系统**：20题MBTI式问卷，4维度8类型人格分类
- **智能匹配算法**：基于人格类型相似度+兴趣标签权重
- **最优配对引擎**：带权重的最大匹配算法，确保全局最优
- **管理后台**：参与者管理、匹配结果查看、数据导出

## 技术栈

- **前端**：Vue 3 + Vite + Element Plus
- **后端**：Python + FastAPI + SQLite
- **匹配算法**：NetworkX 最大权匹配

## 快速启动

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 人格分类模型

| 维度 | 类型A | 类型B |
|------|-------|-------|
| 能量来源 | E(外向) | I(内向) |
| 信息获取 | S(实感) | N(直觉) |
| 决策方式 | T(思考) | F(情感) |
| 生活方式 | J(判断) | P(感知) |

共16种人格类型组合。

## 匹配规则

1. **同好匹配**：相似人格类型优先配对
2. **互补匹配**：差异人格类型优先配对
3. **兴趣权重**：自定义兴趣标签权重
4. **全局最优**：确保整体匹配分数最高

## API文档

启动后端后访问：http://localhost:8000/docs

## 项目结构

```
match-making-app/
├── backend/           # Python后端
│   ├── main.py       # FastAPI主程序
│   ├── database.py   # 数据库模型
│   ├── matching.py   # 匹配算法
│   └── requirements.txt
├── frontend/          # Vue3前端
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   ├── components/ # 可复用组件
│   │   ├── stores/   # Pinia状态管理
│   │   └── utils/    # 工具函数
│   └── package.json
└── README.md
```
