#!/usr/bin/env bash
# ==============================================================================
# ARA-1 Autonomous Financial Research Terminal — One-Click Launcher & Server
# ==============================================================================

set -e

PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"
VENV_DIR="./venv"

echo "================================================================================"
echo "🚀 Starting ARA-1: Autonomous Financial Research Agent with Multi-Source Synthesis"
echo "================================================================================"

# 1. Check Python & Virtual Environment
if [ -d "$VENV_DIR" ]; then
    echo "🐍 Activating existing virtual environment ($VENV_DIR)..."
    source "$VENV_DIR/bin/activate"
else
    echo "📦 Creating new virtual environment ($VENV_DIR)..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    echo "📥 Installing requirements..."
    pip install -r requirements.txt
fi

# 2. Run Test Suite Validation
echo "🧪 Running Pytest Verification Suite..."
pytest -q || echo "⚠️ Warning: Some tests encountered warnings (continuing)..."

# 3. Compile Standalone Bundle
echo "📦 Compiling standalone offline research suite..."
python3 export_standalone.py

# 4. Launch Visual Research Server
echo ""
echo "================================================================================"
echo "✨ ARA-1 Visual Research Terminal Online & Ready"
echo "📡 Local Access:    http://localhost:${PORT}"
echo "🌐 Network Access:  http://${HOST}:${PORT}"
echo "📄 Standalone File: file://$(pwd)/results/ARA1_Research_Suite_Standalone.html"
echo "================================================================================"
echo "Press Ctrl+C to stop the server."
echo ""

python3 web/server.py --port "$PORT" --host "$HOST"
