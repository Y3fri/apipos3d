from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.transacciones import Transacciones
from fastapi.encoders import jsonable_encoder
from service.transacciones_service import TransaccionesService
from schemas.transacciones import Transacciones


transacciones_router = APIRouter()


@transacciones_router.get('/transacciones',tags=['Transacciones'], response_model=list[Transacciones],dependencies=[Depends(JWTBearer())])
def get_transacciones()-> List [Transacciones]:
        db = Session()
        try:
                result = TransaccionesService(db).get_transacciones()
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener los transacciones: {str(e)}"}, status_code=500)
        finally:
                db.close()
