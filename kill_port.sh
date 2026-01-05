#!/bin/bash
# Kill process using port 8000

PORT=${1:-8000}
PID=$(lsof -ti:$PORT)

if [ -z "$PID" ]; then
    echo "✅ Port $PORT is free (no process found)"
else
    echo "🔍 Found process $PID using port $PORT"
    echo "🛑 Killing process..."
    kill $PID
    sleep 1
    if lsof -ti:$PORT > /dev/null 2>&1; then
        echo "⚠️  Process still running, force killing..."
        kill -9 $PID
    fi
    echo "✅ Port $PORT is now free"
fi

