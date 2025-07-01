from sqlalchemy import Column, Integer, String
from database import Base  

class User(Base):
    __tablename__ = "users"

    ID_User = Column(Integer, primary_key=True, index=True)
    Nom = Column(String(100), nullable=False)
    Prenom = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    motDePasse = Column(String(255), nullable=False)
