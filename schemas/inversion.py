from datetime import date
from pydantic import BaseModel
from typing import Optional
from schemas.producto import Producto
from schemas.empresa import Empresa


class Inversion(BaseModel):
    inv_id: Optional[int] = None    
    inv_empresa: int
    inv_producto:int
    inv_fecha: date    
    inv_cantidad: float
    inv_precio_original_unitario: float
    inv_precio_base_unitario: float  
    inv_total: float  

    class Config:
        orm_mode = True