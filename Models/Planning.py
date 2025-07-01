from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Planning(Base):
    __tablename__ = "Planning"

    ID_Planning = Column(Integer, primary_key=True, index=True)
    Date_De_Publication = Column(Date, nullable=False)

    ID_Publication = Column(Integer, ForeignKey("Publication.ID_Publication"), nullable=False)

    publication = relationship("Publication", back_populates="planning")
