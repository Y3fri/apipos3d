from pydantic import BaseModel
from typing import Optional
from schemas.empresa import Empresa
from schemas.rol import Rol

class Sso_usuario(BaseModel):
        usu_id: Optional[int]=None
        usu_empresa: int        
        usu_documento:str
        usu_nombre:str   
        usu_apellido:str
        usu_correo:str
        usu_nickname:str
        usu_clave:str                
        
        