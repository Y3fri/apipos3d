from pydantic import BaseModel
from typing import Optional


class Metodo_pago(BaseModel):
        pag_id: Optional[int]=None
        pag_nombre:str        
