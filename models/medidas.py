from config.database import Base
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship

class Medidas(Base):
    __tablename__="medidas"

    med_id = Column(Integer, primary_key = True)
    med_nombre=Column(String(80))    

    producto = relationship("Producto", back_populates="medidas")