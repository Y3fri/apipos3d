from pydantic import BaseModel
from datetime import date,time
from typing import Optional
from schemas.producto import Producto
from schemas.venta import Venta

class Pedido(BaseModel):
    
        
    ped_id : Optional[int]=None
    ped_venta : int
    ped_producto : int
    ped_preTotal : float
    ped_cantidad : float
    