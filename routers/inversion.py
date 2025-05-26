from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.inversion import Inversion
from fastapi.encoders import jsonable_encoder
from service.inversion_service import InversionService
from schemas.inversion import Inversion


inversion_router = APIRouter()


@inversion_router.get('/inversion/{inversion_emp}',tags=['Inversion'], response_model=Inversion,dependencies=[Depends(JWTBearer())])
def get_inversions(inversion_emp):
        db = Session()
        try:
                result = InversionService(db).get_inversion(inversion_emp)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener la inversion: {str(e)}"}, status_code=500)
        finally:
                db.close()

@inversion_router.get('/inversion/{inversion_emp}/{filtro_fecha}',tags=['Inversion'], response_model=Inversion,dependencies=[Depends(JWTBearer())])
def get_inversions_fecha(inversion_emp,filtro_fecha):
        db = Session()
        try:
                result = InversionService(db).get_inversion_fecha(inversion_emp, filtro_fecha)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener la inversion: {str(e)}"}, status_code=500)
        finally:
                db.close()

@inversion_router.get('/inversion_id/{inversion_emp}/{inv_id}',tags=['Inversion'], response_model=Inversion,dependencies=[Depends(JWTBearer())])
def get_inversions_id(inversion_emp,inv_id):
        db = Session()
        try:
                result = InversionService(db).get_inversion_id(inversion_emp, inv_id)
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener la inversion: {str(e)}"}, status_code=500)
        finally:
                db.close()