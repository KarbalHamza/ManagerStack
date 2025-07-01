from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ComptePlateforme(Base):
    __tablename__ = "ComptePlateforme"

    ID_Compte = Column(Integer, ForeignKey("Compte.ID_Compte"), primary_key=True)
    ID_Plateforme = Column(Integer, ForeignKey("Plateforme.ID_Plateforme"), primary_key=True)

    compte = relationship("Compte", back_populates="plateformes")
    plateforme = relationship("Plateforme", back_populates="comptes")
