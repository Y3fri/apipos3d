from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Producto(Base):
    __tablename__ = "producto"

    pro_id = Column(Integer, primary_key=True, autoincrement=True)
    pro_estado = Column(Integer, ForeignKey("estado.est_id"), nullable=False)
    pro_categoria = Column(Integer, ForeignKey("categoria.cat_id"), nullable=False)
    pro_medida = Column(Integer, ForeignKey("medidas.med_id"), nullable=False)
    pro_empresa = Column(Integer, ForeignKey("empresa.emp_id"), nullable=False)
    pro_idbarras = Column(String(15))
    pro_nombre = Column(String(50))    
    pro_cantidad =  Column(DECIMAL(10, 3))
    pro_precio_original = Column(DECIMAL(10, 3))
    pro_precio_base = Column(DECIMAL(10, 3))
    pro_foto = Column(String(500))
    pro_codigo = Column(String(5))
        
    estado = relationship("Estado", back_populates="producto")
    categoria = relationship("Categoria", back_populates="producto")
    medidas = relationship("Medidas", back_populates="producto")
    empresa= relationship("Empresa", back_populates="producto")
    inversion = relationship("Inversion", back_populates="producto")
    pedido = relationship("Pedido", back_populates="producto")
    perdidas = relationship("Perdidas", back_populates="producto")
    
