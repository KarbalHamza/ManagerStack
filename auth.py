from datetime import datetime, timedelta
from jose import JWTError, jwt

# 🔐 Clé secrète à garder secrète
SECRET_KEY = "DimaRaja" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ➕ Créer un token JWT
def create_token(user_id: int):
    # 1. La date d’expiration = maintenant + 30 minutes
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # 2. Les infos qu’on met dans le token
    infos = {
        "sub": str(user_id),  # sub = subject = l'utilisateur
        "exp": expiration     # exp = expiration
    }

    # 3. On crée le token (chiffré)
    token = jwt.encode(infos, SECRET_KEY, algorithm=ALGORITHM)

    # 4. On le retourne
    return token
