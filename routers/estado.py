from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.estado import Estado
from fastapi.encoders import jsonable_encoder
from service.estado_service import EstadoService
from schemas.estado import Estado


estado_router = APIRouter()


@estado_router.get('/estado',tags=['Estado'], response_model=list[Estado],dependencies=[Depends(JWTBearer())])
def get_estado()-> List [Estado]:
        db = Session()
        try:
                result = EstadoService(db).get_estado()
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener los estados: {str(e)}"}, status_code=500)
        finally:
                db.close()

