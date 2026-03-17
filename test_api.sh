#!/bin/bash

echo "🧪 Testing Multi-Agent Visualization Platform API"
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000"

# Test 1: Health check
echo "1️⃣  Testing health endpoint..."
curl -s "$BASE_URL/health" | python3 -m json.tool || echo "❌ Health check failed"
echo ""

# Test 2: Root endpoint
echo "2️⃣  Testing root endpoint..."
curl -s "$BASE_URL/" | python3 -m json.tool || echo "❌ Root endpoint failed"
echo ""

# Test 3: Execute an agent
echo "3️⃣  Testing agent execution..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "test_agent_001",
    "agent_name": "TestAgent",
    "agent_type": "worker",
    "input_data": {"query": "test query"}
  }')

echo "$RESPONSE" | python3 -m json.tool || echo "❌ Agent execution failed"

# Extract session_id from response
SESSION_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('trace_id', ''))" 2>/dev/null)

if [ -n "$SESSION_ID" ]; then
  echo ""
  echo "4️⃣  Testing trace retrieval..."
  curl -s "$BASE_URL/api/v1/traces/$SESSION_ID" | python3 -m json.tool || echo "❌ Trace retrieval failed"
fi

echo ""
echo "✅ API testing completed!"
echo ""
echo "📖 Full API documentation: $BASE_URL/docs"
