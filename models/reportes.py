from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey,DATE,TIME
from sqlalchemy.orm import relationship
from config.database import Base

class Reportes(Base):
    __tablename__ = "reportes"

    rep_id = Column(Integer, primary_key=True, autoincrement=True)
    rep_cli = Column(Integer, ForeignKey("sso_usuario.usu_id"), nullable=False)          
    rep_asunto = Column(String(80))
    rep_observacion = Column(String(3000))  
    rep_fecha=  Column(DATE)
    rep_hora = Column(TIME)