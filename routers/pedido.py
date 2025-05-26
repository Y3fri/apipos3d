from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from schemas.pedido import Pedido
from service.pedido_service import PedidoService

pedido_router = APIRouter()

@pedido_router.get('/pedido/{venta}', tags=['Pedido'], response_model=Pedido,dependencies=[Depends(JWTBearer())])
def get_pedido(venta):
        db = Session()
        try:
                result = PedidoService(db).get_pedido(venta)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener los pedidos: {str(e)}"}, status_code=500)
        finally:
                db.close()