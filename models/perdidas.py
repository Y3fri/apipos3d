from sqlalchemy import Column, Integer, DECIMAL, DATE,String, TIME,ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Perdidas(Base):
    __tablename__="perdidas"

    per_id = Column(Integer, primary_key = True)
    per_producto = Column(Integer, ForeignKey("producto.pro_id"), nullable=False)    
    per_empresa=  Column(Integer, ForeignKey("empresa.emp_id"), nullable=False)
    per_fecha=  Column(DATE)
    per_cantidad = Column(DECIMAL(10, 3))
    per_total = Column(DECIMAL(10, 3))
        
    producto = relationship("Producto", back_populates="perdidas")
    empresa = relationship("Empresa", back_populates="perdidas")    
    