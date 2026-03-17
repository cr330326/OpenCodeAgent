#!/bin/bash

echo "🚀 Starting Backend Development Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    exit 1
fi

# Create virtual environment if not exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
else
    cd backend
    source venv/bin/activate
    cd ..
fi

# Set environment variables
export DATABASE_URL="sqlite:///./agent_viz.db"
export REDIS_URL="redis://localhost:6379/0"
export API_HOST="0.0.0.0"
export API_PORT="8000"
export CORS_ORIGINS='["http://localhost:3000"]'

echo ""
echo "📍 Starting server at http://localhost:8000"
echo "📖 API Docs will be available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start the server
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
