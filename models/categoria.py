from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Categoria(Base):
    __tablename__ = "categoria"

    cat_id = Column(Integer, primary_key=True, autoincrement=True)
    cat_estado = Column(Integer, ForeignKey("estado.est_id"), nullable=False)    
    cat_nombre = Column(String(120))
    
    estado = relationship("Estado", back_populates="categoria")
    producto = relationship("Producto", back_populates="categoria")
    