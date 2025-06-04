from sqlalchemy import Column, Integer, DECIMAL, DATE,String, TIME,ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Gastos(Base):
    __tablename__="gastos"

    gas_id = Column(Integer, primary_key = True)    
    gas_empresa=  Column(Integer, ForeignKey("empresa.emp_id"), nullable=False)
    gas_fecha=  Column(DATE)
    gas_proveedor = Column(String(200))
    gas_concepto = Column(String(1000))
    gas_valor = Column(DECIMAL(10,0))
    gas_unidades = Column(Integer)
    
                
    empresa = relationship("Empresa", back_populates="gastos")    
    