from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.medidas import Medidas
from fastapi.encoders import jsonable_encoder
from service.medidas_service import MedidasService
from schemas.medidas import Medidas


medidas_router = APIRouter()


@medidas_router.get('/medidas',tags=['Medidas'], response_model=list[Medidas],dependencies=[Depends(JWTBearer())])
def get_medidas()-> List [Medidas]:
        db = Session()
        try:
                result = MedidasService(db).get_medidas()
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener los medidas: {str(e)}"}, status_code=500)
        finally:
                db.close()
