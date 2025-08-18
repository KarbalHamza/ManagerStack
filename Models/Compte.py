from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Compte(Base):
    __tablename__ = "Compte"

    ID_Compte = Column(Integer, primary_key=True, index=True)
    Nom_Compte = Column(String(255), nullable=False)
    Type_De_Compte = Column(String(255), nullable=False)
    ID_User = Column(Integer, ForeignKey("users.ID_User"), nullable=False)

    user = relationship("User", back_populates="comptes")