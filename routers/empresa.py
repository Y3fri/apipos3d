from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.empresa import Empresa
from fastapi.encoders import jsonable_encoder
from service.empresa_service import EmpresaService
from schemas.empresa import Empresa


empresa_router = APIRouter()


@empresa_router.get('/empresa/{empresa_id}',tags=['Empresa'], response_model=Empresa,dependencies=[Depends(JWTBearer())])
def get_empresas(empresa_id):
        db = Session()
        try:
                result = EmpresaService(db).get_empresa(empresa_id)
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener la empresa: {str(e)}"}, status_code=500)
        finally:
                db.close()


