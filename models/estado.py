from config.database import Base
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship

class Estado(Base):
    __tablename__="estado"

    est_id = Column(Integer, primary_key = True)
    est_nombre=Column(String(30))    
    
    categoria = relationship("Categoria", back_populates="estado")
    producto = relationship("Producto", back_populates="estado")