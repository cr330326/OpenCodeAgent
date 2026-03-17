# 多Agent可视化平台 - 前端

React前端项目，使用 TypeScript + ReactFlow + Zustand + Ant Design

## 快速开始

### 安装依赖
```bash
cd frontend
npm install
```

### 启动开发服务器
```bash
npm start
```

### 构建生产版本
```bash
npm run build
```

## 项目结构

```
frontend/
├── src/
│   ├── components/
│   │   ├── Canvas/          # Agent编排画布
│   │   ├── Trace/           # 追踪可视化
│   │   ├── Monitor/         # 实时监控
│   │   └── Debugger/      # 调试工具
│   ├── hooks/             # 自定义Hooks
│   ├── stores/            # Zustand状态管理
│   ├── services/          # API客户端
│   └── utils/            # 工具函数
└── package.json
```

## 技术栈

- **React 18** - 前端框架
- **TypeScript** - 类型安全
- **ReactFlow** - 流程画布
- **Zustand** - 状态管理
- **Ant Design** - UI组件库
- **Axios** - HTTP客户端
- **Socket.io** - WebSocket客户端
- **Recharts** - 图表库

## 功能模块

### 1. Agent编排画布 (Canvas)
- 拖拽式节点编辑
- 连线管理
- 参数配置
- 实时预览

### 2. 追踪可视化 (Trace)
- 时间线视图
- 拓扑图视图
- 消息流图
- 详情面板

### 3. 实时监控 (Monitor)
- 性能指标
- Token消耗
- 成功率统计
- 错误追踪

### 4. 调试工具 (Debugger)
- Agent执行器
- 输入/输出查看
- 断点调试
- 变量检查

## 开发指南

### 添加新组件
1. 在 `src/components/` 下创建新目录
2. 创建组件文件 (PascalCase.tsx)
3. 在 App.tsx 中引入并使用

### 添加新的API调用
1. 在 `src/services/api.ts` 中添加接口定义
2. 使用 axios 进行HTTP请求
3. 处理错误和 loading 状态

### 添加新的状态
1. 在 `src/stores/` 中创建新的store
2. 使用 zustand 的 create 方法
3. 在组件中通过 hooks 使用

## 稡块说明

### WebSocket连接
```typescript
import { useWebSocket } from './hooks/useWebSocket';

// 自动连接到后端
// 接收实时更新
```

### API调用
```typescript
import { agentApi } from './services/api';

// 执行Agent
const result = await agentApi.execute({...});
// 获取追踪数据
const traces = await agentApi.getSessionTraces(sessionId);
```

### 状态管理
```typescript
import { useAgentStore } from './stores/agentStore';

// 访问状态
const { traces, isLoading } = useAgentStore();
// 更新状态
addTrace(newTrace);
```

## 待实现功能

- [ ] 前端项目完善
- [ ] 更多样式图表
- [ ] Agent配置持久化
- [ ] 工作流保存/加载
- [ ] 用户设置
- [ ] 主题切换

## 注意事项

1. **API地址配置**
   - 开发环境: http://localhost:8000
   - 生产环境: 需要配置 REACT_APP_API_URL

2. **WebSocket地址配置**
   - 开发环境: ws://localhost:8000
   - 生产环境: 需要配置 REACT_APP_WS_URL

3. **跨域配置**
   - 后端已配置CORS
   - 允许 localhost:3000 访问

4. **性能优化**
   - 大量节点时使用虚拟滚动
   - 长时间线使用分页
   - 频繁更新使用防抖
