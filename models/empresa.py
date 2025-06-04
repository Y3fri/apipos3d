from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Empresa(Base):
    __tablename__ = "empresa"

    emp_id = Column(Integer, primary_key=True)
    emp_municipio = Column(String(80))
    emp_razon_social = Column(String(80))
    emp_propietario = Column(String(80))
    emp_nit = Column(String(20))
    emp_email = Column(String(80))
    emp_telefono = Column(String(50))
    emp_direccion = Column(String(50))
    emp_logo = Column(String(500))
    
    sso_usuario = relationship("Sso_usuario", back_populates="empresa")
    producto = relationship("Producto", back_populates="empresa")
    inversion = relationship("Inversion", back_populates="empresa")
    venta = relationship("Venta", back_populates="empresa")
    perdidas = relationship("Perdidas", back_populates="empresa")
    gastos = relationship("Gastos", back_populates="empresa")