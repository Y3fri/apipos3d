from pydantic import BaseModel
from typing import Optional
from schemas.estado import Estado
from schemas.categoria import Categoria
from schemas.medidas import Medidas
from schemas.empresa import Empresa


class Producto(BaseModel):
    pro_id: Optional[int] = None
    pro_estado: int
    pro_categoria: int
    pro_medida: int
    pro_empresa: int
    pro_idbarras: str
    pro_nombre: str
    pro_cantidad: float
    pro_precio_original: float
    pro_precio_base: float
    pro_foto: str            
    pro_codigo:str

    class Config:
        orm_mode = True