#!/usr/bin/env bash
# ─── NeuralPath Backend Launcher ───────────────────────────────────────────
set -e
cd "$(dirname "$0")"

echo ""
echo "  ███╗   ██╗███████╗██╗   ██╗██████╗  █████╗ ██╗      "
echo "  ████╗  ██║██╔════╝██║   ██║██╔══██╗██╔══██╗██║      "
echo "  ██╔██╗ ██║█████╗  ██║   ██║██████╔╝███████║██║      "
echo "  ██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██╔══██║██║      "
echo "  ██║ ╚████║███████╗╚██████╔╝██║  ██║██║  ██║███████╗ "
echo "  ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ "
echo ""
echo "  AI Career Intelligence — Backend v2.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 not found. Please install Python 3.10+."
  exit 1
fi

# Install deps if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo "📦 Installing dependencies..."
  pip install -r requirements.txt
fi

echo ""
echo "🚀 Starting backend at http://localhost:8000"
echo "📖 Swagger UI:  http://localhost:8000/api/docs"
echo "📘 ReDoc:       http://localhost:8000/api/redoc"
echo ""
echo "  Press Ctrl+C to stop."
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
