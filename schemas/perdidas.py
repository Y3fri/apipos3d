from pydantic import BaseModel
from datetime import date,time
from typing import Optional
from schemas.producto import Producto
from schemas.venta import Venta

class Perdidas(BaseModel):
    
        
    per_id : Optional[int]=None    
    per_producto : int
    per_empresa : int
    per_fecha : date
    per_cantidad : float
    per_total: float
    