from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Profil(Base):
    __tablename__ = "Profil"

    ID_Profil = Column(Integer, primary_key=True, index=True)
    Nom_Profile = Column(String(255), nullable=False)
    Nombre_abonnes = Column(String(100), nullable=False)
    etat = Column(String(20), nullable=False)

    ID_Compte = Column(Integer, ForeignKey("Compte.ID_Compte"), nullable=False)

    compte = relationship("Compte", back_populates="profils")
    publications = relationship("Publication", back_populates="profil")
