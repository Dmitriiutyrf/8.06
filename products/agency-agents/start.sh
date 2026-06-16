#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================"
echo "       AGENCY AGENTS: DIGITAL FACTORY EDITION"
echo "========================================================"
echo ""

echo "[1] Checking Python..."
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is not installed!"
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "[2] Installing necessary libraries (Streamlit)..."
pip3 install -q -r requirements.txt

echo "[3] Launching the Explorer..."
echo "The app will open in your browser shortly."
echo ""
streamlit run app.py
