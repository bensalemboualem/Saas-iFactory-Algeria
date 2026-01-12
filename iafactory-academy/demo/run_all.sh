#!/bin/bash
# ============================================
# IAFactory Academy - Lancement Complet
# ============================================

echo ""
echo "============================================"
echo " IAFactory Academy - Lancement Complet"
echo "============================================"
echo ""

# Aller dans le repertoire demo
cd "$(dirname "$0")"

echo "[1/4] Demarrage Demo Generique (port 8502)..."
python -m streamlit run minister_demo_generic.py --server.port 8502 &
sleep 3

echo "[2/4] Demarrage Demo BBC (port 8503)..."
python -m streamlit run minister_demo_bbc.py --server.port 8503 &
sleep 3

echo "[3/4] Demarrage Chatbot RAG (port 8504)..."
python -m streamlit run chatbot_rag.py --server.port 8504 &
sleep 3

echo "[4/4] Demarrage AnythingLLM (port 3001)..."
cd anythingllm
docker-compose up -d
cd ..
sleep 5

echo ""
echo "============================================"
echo " APPLICATIONS LANCEES"
echo "============================================"
echo ""
echo " Demo Generique : http://localhost:8502"
echo " Demo BBC       : http://localhost:8503"
echo " Chatbot RAG    : http://localhost:8504"
echo " AnythingLLM    : http://localhost:3001"
echo ""
echo "============================================"
echo ""

# Ouvrir le navigateur (Linux)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8503
# Ouvrir le navigateur (macOS)
elif command -v open &> /dev/null; then
    open http://localhost:8503
fi

echo "Appuyez sur Ctrl+C pour arreter tous les services..."
wait
