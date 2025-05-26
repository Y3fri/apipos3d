from pydantic import BaseModel
from datetime import date,time
from typing import Optional
from schemas.empresa import Empresa
from schemas.transacciones import Transacciones
from schemas.metodo_pago import Metodo_pago
from schemas.sso_usuario import Sso_usuario

class Venta(BaseModel):
    
        
    ven_id : Optional[int]=None
    ven_empresa : int
    ven_transacciones : int
    ven_pago : int
    ven_usuario : int
    ven_fecha : date
    ven_hora :time
    ven_total :float
    ven_cliente_fia :str
    ven_cliente_contado :str
    ven_dinero_recibido : float
    ven_cambio : float
    ven_descuento :float
    