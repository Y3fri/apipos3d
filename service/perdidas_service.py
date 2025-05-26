from models.producto import Producto  as ProductoModel
from decimal import Decimal,ROUND_DOWN
from models.reportes import Reportes
from schemas.perdidas import Perdidas
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models.perdidas import Perdidas as PerdidasModel
from datetime import datetime,timedelta
from models.sso_usuario import Sso_usuario
import pytz

bogota_timezone = pytz.timezone("America/Bogota")


class PerdidasService():

    def __init__(self,db) -> None:
        self.db = db    

    def get_perdidas(self, perdidas_emp: int):        
        result = self.db.query(PerdidasModel).filter(PerdidasModel.per_empresa == perdidas_emp).all()

        perdidas_list=[
            {
                "per_id": perdidas.per_id,
                "per_empresa": perdidas.per_empresa,
                "per_producto": perdidas.per_producto,
                "per_fecha": perdidas.per_fecha,
                "per_cantidad": perdidas.per_cantidad,  
                "per_total": perdidas.per_total,
                "nombre_producto": perdidas.producto.pro_nombre                
            }
            for perdidas in result
        ]
        return perdidas_list
    

    def get_perdidas_fecha(self, perdidas_emp: int,filtro_fecha: str):        
        fecha_actual = datetime.now(bogota_timezone).date()

        # Manejo del filtro de fechas
        if filtro_fecha == "hoy":
            fecha_inicio = fecha_actual
            fecha_fin = fecha_actual
        elif filtro_fecha == "ayer":
            fecha_inicio = fecha_actual - timedelta(days=1)
            fecha_fin = fecha_actual - timedelta(days=1)
        elif filtro_fecha == "semana":
            fecha_inicio = fecha_actual - timedelta(weeks=1)
            fecha_fin = fecha_actual
        elif filtro_fecha == "mes":
            fecha_inicio = fecha_actual - timedelta(days=30)
            fecha_fin = fecha_actual
        elif filtro_fecha == "año":
            fecha_inicio = fecha_actual - timedelta(days=365)
            fecha_fin = fecha_actual
        else:
            raise ValueError("Filtro de fecha no válido. Opciones: hoy, ayer, semana, mes, año.")

        # Crear la consulta base con el rango de fechas
        query = self.db.query(PerdidasModel).filter(
            PerdidasModel.per_empresa == perdidas_emp,
            PerdidasModel.per_fecha >= fecha_inicio,
            PerdidasModel.per_fecha <= fecha_fin
        )
        
        result = query.all()


        perdidas_list=[
            {
                "per_id": perdidas.per_id,
                "per_empresa": perdidas.per_empresa,
                "per_producto": perdidas.per_producto,
                "per_fecha": perdidas.per_fecha,
                "per_cantidad": perdidas.per_cantidad,  
                "per_total": perdidas.per_total,
                "nombre_producto": perdidas.producto.pro_nombre                
            }
            for perdidas in result
        ]
        return perdidas_list
    
    def agregar_perdidas(self, perdidas: Perdidas, usu_id: int):
        try:            
            # Validaciones iniciales (se mantienen igual)
            if not perdidas.per_empresa or not perdidas.per_producto:
                raise ValueError("Faltan campos requeridos para la pérdida")
            
            result = self.db.query(ProductoModel).filter(ProductoModel.pro_id == perdidas.per_producto).first()
            if not result:
                raise ValueError(f"No se encontró un producto con ID {perdidas.per_producto}")

            if result.pro_empresa != perdidas.per_empresa:
                raise ValueError(
                    f"El producto con ID {perdidas.per_producto} no pertenece a la empresa con ID {perdidas.per_empresa}"
                )

            # Obtener información del usuario/cliente
            usuario = self.db.query(Sso_usuario).filter(Sso_usuario.usu_id == usu_id).first()
            if not usuario:
                raise ValueError(f"No se encontró el usuario con ID {usu_id}")
            
            nombre_cliente = usuario.usu_nombre  # Obtenemos el nombre del cliente

            # Resto del procesamiento (se mantiene igual)
            cantidad_perdidas = Decimal(perdidas.per_cantidad).quantize(Decimal('0.001'), rounding=ROUND_DOWN)
            cantidad_producto = Decimal(result.pro_cantidad).quantize(Decimal('0.001'), rounding=ROUND_DOWN)

            if cantidad_perdidas > cantidad_producto:
                raise ValueError(
                    f"La cantidad de pérdidas ({perdidas.per_cantidad}) no puede ser mayor que la cantidad disponible del producto ({result.pro_cantidad})"
                )
            elif cantidad_perdidas == cantidad_producto:
                result.pro_cantidad = 0
            else:
                result.pro_cantidad -= cantidad_perdidas

            per_total = Decimal(result.pro_precio_original) * cantidad_perdidas

            # Crear registro de pérdida
            new_perdidas = PerdidasModel(
                per_empresa=perdidas.per_empresa,
                per_producto=perdidas.per_producto,
                per_fecha=datetime.now(bogota_timezone).date(),
                per_cantidad=cantidad_perdidas,
                per_total=per_total,
            )
            self.db.add(new_perdidas)
            self.db.flush()

            # Crear reporte asociado (ahora incluyendo el nombre del cliente)
            observacion = (f"El usuario {nombre_cliente} registró pérdida del producto {result.pro_nombre} \n "
                        f"cantidad: {cantidad_perdidas} unidades\nTotal: ${per_total:,.2f}")
            
            new_reporte = Reportes(
                rep_cli=usu_id,
                rep_asunto=f"Registro de pérdida por {nombre_cliente}",
                rep_observacion=observacion,
                rep_fecha=datetime.now(bogota_timezone).date(),
                rep_hora=datetime.now(bogota_timezone).time(),
            )
            self.db.add(new_reporte)

            self.db.commit()
            return {"message": "Pérdida registrada y reporte generado correctamente"}

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error en la base de datos: {str(e)}")
            raise ValueError(f"Error al interactuar con la base de datos: {str(e)}")

        except ValueError as ve:
            self.db.rollback()
            print(f"Error: {str(ve)}")
            raise ValueError(str(ve))