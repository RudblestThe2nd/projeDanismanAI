#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "========================================"
echo "  ProjeDanışmanAI - Başlatılıyor..."
echo "========================================"

# --- BACKEND ---
echo "[1/2] Backend hazırlanıyor..."
cd "$BACKEND_DIR"

# pyenv / venv / sistem Python'unu otomatik bul
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    PIP_CMD="pip"
    UVICORN_CMD="uvicorn"
elif [ -f "$HOME/.pyenv/shims/python" ]; then
    export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init -)" 2>/dev/null
    PIP_CMD="pip"
    UVICORN_CMD="uvicorn"
else
    PIP_CMD="pip3"
    UVICORN_CMD="python3 -m uvicorn"
fi

# Eksik Python paketlerini kur
if [ -f "requirements.txt" ]; then
    echo "    Python bağımlılıkları kontrol ediliyor..."
    $PIP_CMD install -q -r requirements.txt
fi

echo "    Backend başlatılıyor (port 8000)..."
$UVICORN_CMD main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "    Backend PID: $BACKEND_PID"

# Backend'in ayağa kalkması için bekle
sleep 3

# --- FRONTEND ---
echo "[2/2] Frontend hazırlanıyor..."
cd "$FRONTEND_DIR"

# Eksik node_modules'u kur
if [ ! -d "node_modules" ]; then
    echo "    npm bağımlılıkları kuruluyor..."
    npm install
fi

# node_modules/.bin/vite izin sorununu önle
chmod +x node_modules/.bin/vite 2>/dev/null

echo "    Frontend başlatılıyor (port 5173)..."
npm run dev &
FRONTEND_PID=$!
echo "    Frontend PID: $FRONTEND_PID"

echo ""
echo "========================================"
echo "  Uygulama hazır!"
echo "  Backend : http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "========================================"
echo ""
echo "Kapatmak için Ctrl+C'ye basın..."

# İki process'i de bekle; Ctrl+C gelince ikisini de öldür
trap "echo 'Kapatılıyor...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM
wait $BACKEND_PID $FRONTEND_PID
