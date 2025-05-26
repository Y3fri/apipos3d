from sqlalchemy import Column, Integer, DECIMAL, DATE,String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Inversion(Base):
    __tablename__ = "inversion"

    inv_id = Column(Integer, primary_key=True, autoincrement=True)
    inv_empresa =  Column(Integer, ForeignKey("empresa.emp_id"), nullable=False)
    inv_producto = Column(Integer, ForeignKey("producto.pro_id"), nullable=False)
    inv_fecha = Column(DATE)  
    inv_cantidad = Column(DECIMAL(10, 3))
    inv_precio_original_unitario = Column(DECIMAL(10, 3))
    inv_precio_base_unitario = Column(DECIMAL(10, 3))
    inv_total = Column(DECIMAL(10, 3))    
        
    empresa = relationship("Empresa", back_populates="inversion")
    producto = relationship("Producto", back_populates="inversion")
    
