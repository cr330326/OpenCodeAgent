# Multi-Agent Visualization Platform

多AI Agent可视化Web平台，用于采集、展示和分析Agent执行结果。

## 功能特性

- ✅ Agent编排可视化（拖拽式流程设计）
- ✅ Agent通信链路实时追踪
- ✅ 执行结果采集与Hooks系统
- ✅ 实时监控与WebSocket推送
- ✅ 历史数据回放与分析
- ✅ 性能指标统计

## 技术栈

**后端:**
- FastAPI + Uvicorn
- LangChain (Agent框架)
- PostgreSQL (数据存储)
- Redis (缓存/实时通信)

**前端:**
- React 18 + TypeScript
- ReactFlow (流程画布)
- Zustand (状态管理)

## 快速开始

### 使用 Docker Compose（推荐）

1. 启动所有服务：
```bash
docker-compose up -d
```

2. 访问应用：
- API文档: http://localhost:8000/docs
- API地址: http://localhost:8000/api/v1
- 健康检查: http://localhost:8000/health

### 手动部署

#### 后端部署

1. 安装依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件配置数据库连接
```

3. 启动服务：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 文档

启动服务后访问 http://localhost:8000/docs 查看完整API文档。

### 主要端点

**Agent执行:**
- `POST /api/v1/agents/execute` - 执行Agent并追踪
- `WS /api/v1/agents/ws` - WebSocket实时通信

**追踪查询:**
- `GET /api/v1/traces/session/{session_id}` - 获取会话所有追踪
- `GET /api/v1/traces/{trace_id}` - 获取单个追踪详情
- `GET /api/v1/traces/metrics/{agent_id}` - 获取Agent性能指标

## 开发指南

详细开发指南请参考 [AGENTS.md](../AGENTS.md)

### 运行测试

```bash
cd backend
pytest
```

### 代码检查

```bash
ruff check app/
black app/ --check
mypy app/
```

## 项目结构

```
/backend
  /app
    /api          # FastAPI路由
    /models       # 数据模型
    /hooks        # Agent追踪Hooks
    /storage      # 数据存储层
    /services     # 业务逻辑
  /tests          # 测试文件

/frontend
  /src
    /components   # React组件
    /hooks        # 自定义Hooks
    /stores       # Zustand状态管理
    /services     # API客户端
```

## 环境要求

- Python 3.11+
- Node.js 18+ (前端)
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (推荐)

## 许可证

MIT License
