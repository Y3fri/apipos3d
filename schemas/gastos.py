from pydantic import BaseModel
from datetime import date,time
from typing import Optional
from schemas.producto import Producto
from schemas.venta import Venta

class Gastos(BaseModel):
    
        
    gas_id : Optional[int]=None    
    gas_empresa : int
    gas_fecha : date
    gas_proveedor: str
    gas_concepto : str
    gas_valor: float
    gas_unidades: int
    