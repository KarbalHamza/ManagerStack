#!/usr/bin/env bash
set -euo pipefail

echo "Attente du démarrage de MySQL..."
sleep 10

if command -v alembic >/dev/null 2>&1 && [ -f "alembic.ini" ]; then
  echo "Migration Alembic..."
  alembic upgrade head || echo "Alembic non configuré, on continue..."
fi

echo "Lancement de l'application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
