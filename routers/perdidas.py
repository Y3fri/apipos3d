from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.perdidas import Perdidas
from fastapi.encoders import jsonable_encoder
from service.perdidas_service import PerdidasService
from schemas.perdidas import Perdidas


perdidas_router = APIRouter()


@perdidas_router.get('/perdidas/{perdidas_emp}',tags=['Perdidas'], response_model=Perdidas,dependencies=[Depends(JWTBearer())])
def get_perdidass(perdidas_emp):
        db = Session()
        try:
                result = PerdidasService(db).get_perdidas(perdidas_emp)
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener la perdidas: {str(e)}"}, status_code=500)
        finally:
                db.close()

@perdidas_router.get('/perdidas/{perdidas_emp}/{filtro_fecha}',tags=['Perdidas'], response_model=Perdidas,dependencies=[Depends(JWTBearer())])
def get_perdidass(perdidas_emp, filtro_fecha):
        db = Session()
        try:
                result = PerdidasService(db).get_perdidas_fecha(perdidas_emp,filtro_fecha)
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener la perdidas: {str(e)}"}, status_code=500)
        finally:
                db.close()
    
@perdidas_router.post('/perdidas', tags=['Perdidas'], response_model=dict, dependencies=[Depends(JWTBearer())])
def agregar_perdidas(perdidas: Perdidas, usu_id: int ) -> dict:
    db = Session()
    try:
        PerdidasService(db).agregar_perdidas(perdidas, usu_id)
        return JSONResponse(content={"message": "Se han insertado los datos correctamente"}, status_code=200)
    except ValueError as ve:
        print(f"Error: {str(ve)}")
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return JSONResponse(content={"error": "Ocurrió un error inesperado"}, status_code=500)
