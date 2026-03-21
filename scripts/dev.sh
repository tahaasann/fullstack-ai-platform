#!/bin/bash
# Start both frontend and backend development servers

echo "🚀 Eğitim Platformu başlatılıyor..."

# Start backend
echo "📦 Backend başlatılıyor (FastAPI - port 8000)..."
cd "$(dirname "$0")/../backend"
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "🎨 Frontend başlatılıyor (Vite - port 5173)..."
cd "$(dirname "$0")/../frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Platform çalışıyor!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Durdurmak için Ctrl+C"

# Wait for both processes
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
