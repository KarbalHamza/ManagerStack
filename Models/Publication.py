from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Publication(Base):
    __tablename__ = "Publication"

    ID_Publication = Column(Integer, primary_key=True, index=True)
    description = Column(String(500), nullable=True)
    location = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    Date_De_Creation = Column(Date, nullable=False)
    Date_De_Plannification = Column(Date, nullable=True)
    ID_Profil = Column(Integer, ForeignKey("Profil.ID_Profil"), nullable=False)

    # Relations
    profil = relationship("Profil", back_populates="publications")
    medias = relationship("Media", back_populates="publication")
    planning = relationship("Planning", back_populates="publication", uselist=False)