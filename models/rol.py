from config.database import Base
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship

class Rol(Base):
    __tablename__="rol"

    rol_id = Column(Integer, primary_key = True)
    rol_nombre=Column(String(45))    

    sso_usuarios = relationship("Sso_usuario", back_populates="rol")