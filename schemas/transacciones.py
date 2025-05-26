from pydantic import BaseModel
from typing import Optional


class Transacciones(BaseModel):
        tra_id: Optional[int]=None
        tra_nombre:str        
