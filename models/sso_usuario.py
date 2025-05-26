from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Sso_usuario(Base):
    __tablename__ = "sso_usuario"

    usu_id = Column(Integer, primary_key=True, autoincrement=True)
    usu_empresa = Column(Integer, ForeignKey("empresa.emp_id"), nullable=False)
    usu_rol = Column(Integer, ForeignKey("rol.rol_id"), nullable=False)       
    usu_documento = Column(String(20))
    usu_nombre = Column(String(50))
    usu_apellido = Column(String(50))
    usu_correo = Column(String(50))
    usu_nickname = Column(String(50), unique=True, index=True)
    usu_clave = Column(String(255))        


    empresa = relationship("Empresa", back_populates="sso_usuario")
    venta = relationship("Venta", back_populates="sso_usuario")