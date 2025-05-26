from pydantic import BaseModel
from typing import Optional


class Medidas(BaseModel):
        med_id: Optional[int]=None
        med_nombre:str        
