#!/bin/bash

echo "🚀 Starting Multi-Agent Visualization Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if not exists
if [ ! -f backend/.env ]; then
    echo "📝 Creating .env file..."
    cp backend/.env.example backend/.env
fi

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check if backend is healthy
echo "🔍 Checking backend health..."
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend is healthy!"
else
    echo "⚠️  Backend might still be starting. Check logs: docker-compose logs backend"
fi

echo ""
echo "🎉 Platform is starting!"
echo ""
echo "📍 Services:"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo ""
echo "📝 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart: docker-compose restart"
