from pydantic import BaseModel
from typing import Optional


class Reportes(BaseModel):
    rep_id: Optional[int] = None
    rep_cli: int
    rep_asunto: str
    rep_observacion: str
    rep_fecha: str
    rep_hora: str
    

    class Config:
        orm_mode = True