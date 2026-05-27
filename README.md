# 员工人事管理系统

一个基于B/S架构的员工人事管理系统，采用前后端分离的开发模式。

## 技术栈

### 前端
- Vue 3.5 - 渐进式JavaScript框架
- Vue Router 4.5 - 路由管理
- Element Plus 2.9 - UI组件库
- Axios 1.8 - HTTP客户端
- ECharts 5.6 - 数据可视化
- Vite 6.3 - 构建工具

### 后端
- Flask - Python Web框架
- Flask-SQLAlchemy - ORM框架
- Flask-JWT-Extended - JWT认证
- Flask-CORS - 跨域支持
- SQLite - 关系型数据库

## 功能模块

1. **数据看板** - 员工统计、部门分布、出勤率分析
2. **员工管理** - 员工信息的增删改查
3. **部门管理** - 部门信息维护、员工统计
4. **考勤管理** - 签到签退、请假申请与审批
5. **薪资管理** - 薪资设置与计算

## 项目结构

```
管理系统/
├── backend/                 # 后端代码
│   ├── app.py              # Flask应用入口
│   ├── config.py           # 配置文件
│   ├── extensions.py       # 扩展初始化
│   ├── models.py           # 数据模型
│   ├── seed.py             # 数据初始化
│   └── routes/             # 路由模块
│       ├── auth.py         # 认证路由
│       ├── employee.py     # 员工路由
│       ├── department.py   # 部门路由
│       ├── attendance.py   # 考勤路由
│       ├── salary.py       # 薪资路由
│       └── dashboard.py    # 数据看板路由
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/            # API接口
│   │   ├── router/         # 路由配置
│   │   ├── views/          # 页面组件
│   │   └── App.vue         # 根组件
│   └── package.json
└── README.md
```

## 快速开始

### 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 默认账户

- 管理员: admin / admin123
- 普通员工: employee / 123456

## 许可证

MIT License
