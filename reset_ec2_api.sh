#!/bin/bash

echo "=== [1] Stop du service osmosia ==="
sudo systemctl stop osmosia.service

echo "=== [2] Kill de tous les Gunicorn ==="
sudo pkill -f gunicorn

echo "=== [3] Vérification du port 5000 ==="
sudo lsof -i :5000

echo "=== [4] Pause 2s pour bien libérer ==="
sleep 2

echo "=== [5] Restart du service ==="
sudo systemctl start osmosia.service

echo "=== [6] Status final ==="
sudo systemctl status osmosia.service
