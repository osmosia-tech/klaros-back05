#!/bin/bash

echo "🚀 Pulling latest changes..."
git pull origin main

echo "🔄 Restarting Gunicorn..."
sudo systemctl restart gunicorn
