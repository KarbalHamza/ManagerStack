from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 👇 Configuration de la base de données
DB_USER = "hamza"
DB_PASSWORD = "hamza123"
DB_HOST = "mysql"  
DB_PORT = "3306"
DB_NAME = "appdb"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# 👇 Création de l'engine SQLAlchemy (la "connexion")
engine = create_engine(DATABASE_URL)

# 👇 Session locale pour les requêtes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 👇 Classe de base pour les modèles (User, Product, etc.)
Base = declarative_base()
