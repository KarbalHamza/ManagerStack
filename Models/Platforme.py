from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Plateforme(Base):
    __tablename__ = "Plateforme"

    ID_Plateforme = Column(Integer, primary_key=True, index=True)
    Nom = Column(String(100), nullable=False)

    comptes = relationship("ComptePlateforme", back_populates="plateforme")