echo "Attente du démarrage de MySQL..."
sleep 10

echo "Migration Alembic..."
alembic upgrade head

echo "Lancement de l'application..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
