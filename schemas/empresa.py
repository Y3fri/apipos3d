from pydantic import BaseModel
from typing import Optional


class Empresa(BaseModel):
        emp_id: Optional[int]=None
        emp_municipio:str
        emp_razon_social:str
        emp_propietario:str
        emp_nit:str
        emp_email:str
        emp_telefono:str
        emp_direccion:str
        emp_logo:str
        

