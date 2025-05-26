from config.database import Base
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship

class Transacciones(Base):
    __tablename__="transacciones"

    tra_id = Column(Integer, primary_key = True)
    tra_nombre=Column(String(80))    

    venta = relationship("Venta", back_populates="transacciones")