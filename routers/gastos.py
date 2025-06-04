from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.gastos import Gastos
from fastapi.encoders import jsonable_encoder
from service.gastos_service import GastosService
from schemas.gastos import Gastos


gastos_router = APIRouter()


@gastos_router.get('/gastos/{gastos_emp}/{filtro_fecha}',tags=['Gastos'], response_model=Gastos,dependencies=[Depends(JWTBearer())])
def get_gastoss(gastos_emp, filtro_fecha):
        db = Session()
        try:
                result = GastosService(db).get_gastos_fecha(gastos_emp, filtro_fecha)
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener la gastos: {str(e)}"}, status_code=500)
        finally:
                db.close()
    
@gastos_router.post('/gastos', tags=['Gastos'], response_model=dict, dependencies=[Depends(JWTBearer())])
def agregar_gastos(gastos: Gastos, usu_id: int ) -> dict:
    db = Session()
    try:
        GastosService(db).agregar_gastos(gastos, usu_id)
        return JSONResponse(content={"message": "Se han insertado los datos correctamente"}, status_code=200)
    except ValueError as ve:
        print(f"Error: {str(ve)}")
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return JSONResponse(content={"error": "Ocurrió un error inesperado"}, status_code=500)
