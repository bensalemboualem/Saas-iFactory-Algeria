#!/bin/bash
# IA Factory Video Operator - Deployment Script
# Deploy to VPS with systemd

set -e

# Configuration
APP_NAME="iafactory-operator"
APP_DIR="/opt/iafactory-operator"
VENV_DIR="$APP_DIR/venv"
USER="www-data"
PORT=8085

echo "🚀 Deploying IA Factory Video Operator..."

# Create directory
sudo mkdir -p $APP_DIR
sudo chown -R $USER:$USER $APP_DIR

# Copy files
echo "📁 Copying files..."
sudo cp -r . $APP_DIR/

# Create virtual environment
echo "🐍 Setting up Python environment..."
cd $APP_DIR
sudo -u $USER python3.12 -m venv $VENV_DIR
sudo -u $USER $VENV_DIR/bin/pip install --upgrade pip
sudo -u $USER $VENV_DIR/bin/pip install -r requirements.txt

# Create systemd service for API
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/iafactory-operator.service > /dev/null <<EOF
[Unit]
Description=IA Factory Video Operator API
After=network.target redis.service

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="PYTHONPATH=$APP_DIR"
EnvironmentFile=$APP_DIR/.env
ExecStart=$VENV_DIR/bin/uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Worker
sudo tee /etc/systemd/system/iafactory-worker.service > /dev/null <<EOF
[Unit]
Description=IA Factory Video Operator Worker
After=network.target redis.service iafactory-operator.service

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="PYTHONPATH=$APP_DIR"
EnvironmentFile=$APP_DIR/.env
ExecStart=$VENV_DIR/bin/python worker/worker.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable and start services
echo "🔄 Starting services..."
sudo systemctl enable iafactory-operator iafactory-worker
sudo systemctl restart iafactory-operator iafactory-worker

# Check status
echo "✅ Deployment complete!"
sudo systemctl status iafactory-operator --no-pager
sudo systemctl status iafactory-worker --no-pager

echo ""
echo "🌐 API available at: http://localhost:$PORT/operator/health"
echo "📚 Docs available at: http://localhost:$PORT/operator/docs"
