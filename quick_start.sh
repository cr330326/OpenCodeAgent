#!/bin/bash

echo "🚀 Quick Start - Multi-Agent Visualization Platform"
echo "===================================================="

cd backend

# Create minimal requirements
cat > requirements_minimal.txt <<EOF
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
python-dotenv==1.0.0
EOF

# Install minimal dependencies
echo "📦 Installing minimal dependencies..."
pip install -q -r requirements_minimal.txt 2>&1 | tail -3

# Set environment variables
export DATABASE_URL="sqlite:///./agent_viz.db"
export API_HOST="0.0.0.0"
export API_PORT="8000"
export CORS_ORIGINS='["http://localhost:3000"]'

echo ""
echo "✅ Starting server at http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
