from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from schemas.venta import Venta
from schemas.pedido import Pedido
from service.venta_service import VentaService

venta_router = APIRouter()

@venta_router.get('/ventaDia/', tags=['Venta'], response_model=Venta,dependencies=[Depends(JWTBearer())])
def get_venta():
        db = Session()
        try:
                result = VentaService(db).get_venta()
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las ventas: {str(e)}"}, status_code=500)
        finally:
                db.close()


@venta_router.get('/ventaFechaTrans/{venta_emp}/{fecha}/{transaccion}', tags=['Venta'], response_model=Venta,dependencies=[Depends(JWTBearer())])
def get_venta(venta_emp,fecha,transaccion):
        db = Session()
        try:
                result = VentaService(db).get_venta_date_transaccion(venta_emp,fecha,transaccion)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las ventas: {str(e)}"}, status_code=500)
        finally:
                db.close()

@venta_router.get('/ventaFia', tags=['Venta'], response_model=Venta,dependencies=[Depends(JWTBearer())])
def get_fiado():
        db = Session()
        try:
                result = VentaService(db).get_fiado()
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las ventas: {str(e)}"}, status_code=500)
        finally:
                db.close()
                
@venta_router.get('/ventaFia/{nombre}', tags=['Venta'], response_model=Venta,dependencies=[Depends(JWTBearer())])
def get_fiado_cliente(nombre):
        db = Session()
        try:
                result = VentaService(db).get_fiado_cliente(nombre)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las ventas: {str(e)}"}, status_code=500)
        finally:
                db.close()

@venta_router.put('/ventas/fiado/{nombre_cliente}', tags=['Venta'], response_model=dict, dependencies=[Depends(JWTBearer())])
def update_ventas_fiado(nombre_cliente: str, usu_id:int) -> dict:
    db = Session()
    try:
        # Llamar al servicio para actualizar todas las ventas fiadas de un cliente
        resultado = VentaService(db).update_fiado(nombre_cliente,usu_id)
        return JSONResponse(content=resultado)
    except Exception as e:
        return JSONResponse(content={"error": f"Error al actualizar las ventas: {str(e)}"}, status_code=500)
    finally:
        db.close()


@venta_router.post('/venta', tags=['Venta'], response_model=dict,dependencies=[Depends(JWTBearer())])
def create_venta(venta: Venta, pedidos: list[Pedido], usu_id:int) -> dict:
    db = Session()
    try:
        VentaService(db).create_venta(venta, pedidos,usu_id)
        return JSONResponse(content={"message": "Venta creada correctamente"}, status_code=200)
    except ValueError as ve:
        print(f"Error: {str(ve)}")
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return JSONResponse(content={"error": "Ocurrió un error inesperado"}, status_code=500)

@venta_router.put('/venta/{id}', tags=['Venta'], response_model=dict,dependencies=[Depends(JWTBearer())])
def update_venta(id: int, venta: Venta, usu_id:int) -> dict:
        db = Session()
        try:             
                VentaService(db).update_venta(id, venta, usu_id)
                return JSONResponse(content={"message": "Venta actualizado"})
        except Exception as e:                
                return JSONResponse(content={"error": f"Error al actualizar el venta: {str(e)}"}, status_code=500)
        finally:
                db.close()