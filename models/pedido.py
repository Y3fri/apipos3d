from sqlalchemy import Column, Integer, DECIMAL, DATE,String, TIME,ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Pedido(Base):
    __tablename__="pedido"

    ped_id = Column(Integer, primary_key = True)
    ped_venta=  Column(Integer, ForeignKey("venta.ven_id"), nullable=False)
    ped_producto = Column(Integer, ForeignKey("producto.pro_id"), nullable=False)    
    ped_preTotal= Column(DECIMAL(10, 3))
    ped_cantidad = Column(DECIMAL(10, 3))
    

    venta = relationship("Venta", back_populates="pedido")    
    producto = relationship("Producto", back_populates="pedido")
    