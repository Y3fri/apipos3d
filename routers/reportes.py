from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from schemas.reportes import Reportes
from service.reportes_service import ReportesService

reportes_router = APIRouter()

@reportes_router.get('/reportes/{fecha}', tags=['Reportes'], response_model=Reportes,dependencies=[Depends(JWTBearer())])
def get_reportes(fecha):
        db = Session()
        try:
                result = ReportesService(db).get_reportes(fecha)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener los reportess: {str(e)}"}, status_code=500)
        finally:
                db.close()