from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.metodo_pago import Metodo_pago
from fastapi.encoders import jsonable_encoder
from service.metodo_pago_service import Metodo_pagoService
from schemas.metodo_pago import Metodo_pago


metodo_pago_router = APIRouter()


@metodo_pago_router.get('/metodo_pago',tags=['Metodo_pago'], response_model=list[Metodo_pago],dependencies=[Depends(JWTBearer())])
def get_metodo_pago()-> List [Metodo_pago]:
        db = Session()
        try:
                result = Metodo_pagoService(db).get_metodo_pago()
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener los metodo_pago: {str(e)}"}, status_code=500)
        finally:
                db.close()
