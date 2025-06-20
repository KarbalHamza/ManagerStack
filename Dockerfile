# 1. Utilise une image de base avec Python
FROM python:3.11-slim

# 2. Crée un dossier dans le conteneur pour ton app
WORKDIR /app

# 3. Copie les fichiers requirements.txt dans le conteneur
COPY requirements.txt .

# 4. Installe les bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie le reste des fichiers (comme main.py) dans le conteneur
COPY . .

# 6. Commande à exécuter quand le conteneur démarre
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
