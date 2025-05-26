from config.database import Base
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship

class Metodo_pago(Base):
    __tablename__="metodo_pago"

    pag_id = Column(Integer, primary_key = True)
    pag_nombre=Column(String(80))    

    venta = relationship("Venta", back_populates="metodo_pago")