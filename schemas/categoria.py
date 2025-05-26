from pydantic import BaseModel
from typing import Optional
from schemas.estado import Estado

class Categoria(BaseModel):
    cat_id: Optional[int]=None
    cat_estado:int
    cat_nombre:str
    

    class Config:
        orm_mode = True
