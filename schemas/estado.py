from pydantic import BaseModel
from typing import Optional


class Estado(BaseModel):
        est_id: Optional[int]=None
        est_nombre:str        
