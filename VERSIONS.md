# AI联谊匹配系统 - 双版本分离部署

## 版本说明

### 📱 用户端 (User Version)
**用途**: 供参与者填写问卷  
**访问地址**: http://localhost:3000  
**功能**:
- 查看活动介绍
- 填写基本信息（姓名、学号、性别）
- 完成20道MBTI人格测试
- 选择兴趣标签
- 查看人格分析结果

**特点**:
- 界面简洁，无管理功能
- 无敏感数据展示
- 适合公开访问

---

### 🔐 管理端 (Admin Version)
**用途**: 供组织者管理活动  
**访问地址**: http://localhost:3000/admin  
**登录密码**: `qsxcyy33`

**功能**:
- 概览统计（报名人数、匹配率、人格分布）
- 参与者管理（查看、删除）
- AI智能匹配（同好模式/互补模式）
- 匹配结果查看
- 重置匹配数据

**特点**:
- 密码保护
- 完整管理权限
- 仅组织者可用

---

## 快速启动

### 方式一：一键启动（推荐）

```bash
# Windows
start.bat

# Linux/Mac
bash start.sh
```

然后访问：
- 用户端: http://localhost:3000
- 管理端: http://localhost:3000/admin (密码: qsxcyy33)

### 方式二：手动启动

```bash
# 终端1: 启动后端
cd backend
python main.py

# 终端2: 启动前端
cd frontend
npm run dev
```

---

## 文件说明

### 用户端文件
- `frontend/public/index-simple.html` - 简化版首页
- `frontend/public/quiz-simple.html` - 简化版问卷页（纯HTML，无需构建）

### 管理端文件
- `frontend/src/views/AdminView.vue` - 管理后台页面
- `frontend/src/components/AdminLogin.vue` - 登录验证组件

---

## 生产部署

### 方案1: 分离部署（推荐）

#### 用户端部署
```bash
cd frontend
# 构建生产版本
npm run build

# 部署 dist/ 目录到用户端服务器
# 只暴露首页和问卷功能
```

#### 管理端部署
```bash
# 使用相同构建，但配置反向代理
# 管理端路径 /admin 添加IP白名单或VPN限制
```

### 方案2: 单服务器部署

在同一服务器上运行，通过路径区分：
- `/` - 用户端
- `/admin` - 管理端（需密码）

---

## 使用流程

### 组织者

1. **活动前准备**
   - 访问 http://localhost:3000/admin
   - 输入密码: qsxcyy33
   - 查看系统状态

2. **活动期间**
   - 监控报名人数
   - 查看人格类型分布

3. **活动结束**
   - 点击"开始AI匹配"
   - 选择匹配模式（同好/互补）
   - 查看匹配结果
   - 导出结果用于活动

### 参与者

1. 访问 http://localhost:3000
2. 点击"开始问卷"
3. 填写姓名、学号、性别
4. 完成20道MBTI测试题
5. 选择兴趣标签
6. 提交后查看人格分析
7. 等待组织者公布匹配结果

---

## 安全建议

1. **生产环境**
   - 修改默认密码 `qsxcyy33`
   - 添加HTTPS支持
   - 配置防火墙限制管理端访问IP

2. **数据保护**
   - 定期备份数据库
   - 敏感数据加密存储
   - 活动结束后清理数据

3. **访问控制**
   - 用户端公开访问
   - 管理端限制内网或VPN
   - 添加操作日志记录

---

## 技术栈

- **后端**: Python + FastAPI + SQLite
- **前端**: Vue 3 + Vite + Element Plus
- **算法**: NetworkX 最大权匹配
- **人格模型**: MBTI 16型人格

---

## 问题反馈

如有问题请联系技术支持。
