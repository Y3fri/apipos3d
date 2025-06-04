from sqlalchemy import Column, Integer, DECIMAL, DATE,String, TIME,ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Venta(Base):
    __tablename__="venta"

    ven_id = Column(Integer, primary_key = True)
    ven_empresa =  Column(Integer, ForeignKey("empresa.emp_id"), nullable=False)
    ven_transacciones = Column(Integer, ForeignKey("transacciones.tra_id"), nullable=False)
    ven_pago = Column(Integer, ForeignKey("metodo_pago.pag_id"), nullable=False)
    ven_usuario = Column(Integer, ForeignKey("sso_usuario.usu_id"), nullable=False)    
    ven_fecha = Column(DATE)
    ven_hora = Column(TIME) 
    ven_total =  Column(DECIMAL(10, 0))    
    ven_cliente_contado = Column(String(80))
    ven_dinero_recibido = Column(DECIMAL(10, 0))
    ven_cambio = Column(DECIMAL(10, 0))
    ven_descuento = Column(DECIMAL(10, 0))    

    empresa = relationship("Empresa", back_populates="venta")
    transacciones = relationship("Transacciones", back_populates="venta")
    metodo_pago = relationship("Metodo_pago", back_populates="venta")
    sso_usuario = relationship("Sso_usuario", back_populates="venta")
    pedido = relationship("Pedido", back_populates="venta")
