#!/bin/bash

echo "修复后端代码错误..."

# 修复 models/__init__.py 的循环导入问题
# 文件内容已经是正确的，不需要从自己导入

# 检查并修复其他导入问题
echo "检查导入路径..."

# 验证后端是否能启动
cd backend
python3 -c "import sys; sys.path.insert(0, '.'); from app.models import AgentTrace; print('✅ Import successful')" 2>&1 || echo "❌ Import failed: $error"

# 如果失败，echo "需要检查Python路径"
