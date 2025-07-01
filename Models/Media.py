from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Media(Base):
    __tablename__ = "Media"

    ID_Media = Column(Integer, primary_key=True, index=True)
    Type = Column(String(50), nullable=False)

    ID_Publication = Column(Integer, ForeignKey("Publication.ID_Publication"), nullable=False)

    publication = relationship("Publication", back_populates="medias")
