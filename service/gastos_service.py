from models.producto import Producto  as ProductoModel
from decimal import Decimal,ROUND_DOWN
from models.reportes import Reportes
from schemas.gastos import Gastos
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models.gastos import Gastos as GastosModel
from datetime import datetime,timedelta
from models.sso_usuario import Sso_usuario
import pytz

bogota_timezone = pytz.timezone("America/Bogota")


class GastosService():

    def __init__(self,db) -> None:
        self.db = db    

    def get_gastos_fecha(self, gastos_emp: int,filtro_fecha: str):        
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
        query = self.db.query(GastosModel).filter(
            GastosModel.gas_empresa == gastos_emp,
            GastosModel.gas_fecha >= fecha_inicio,
            GastosModel.gas_fecha <= fecha_fin
        )
        
        result = query.all()


        gastos_list=[
            {
                "gas_id": gastos.gas_id,
                "gas_empresa": gastos.gas_empresa,                
                "gas_fecha": gastos.gas_fecha,
                "gas_proveedor": gastos.gas_proveedor,
                "gas_concepto": gastos.gas_concepto,
                "gas_valor": gastos.gas_valor,
                "gas_unidades": gastos.gas_unidades,              
            }
            for gastos in result
        ]
        return gastos_list
    
    def agregar_gastos(self, gastos: Gastos, usu_id: int):
        try:                 

            # Obtener información del usuario/cliente
            usuario = self.db.query(Sso_usuario).filter(Sso_usuario.usu_id == usu_id).first()
            if not usuario:
                raise ValueError(f"No se encontró el usuario con ID {usu_id}")
            
            nombre_cliente = usuario.usu_nombre  # Obtenemos el nombre del cliente

            # Resto del procesamiento (se mantiene igual)
            cantidad_gastos = Decimal(gastos.gas_unidades).quantize(Decimal('0.001'), rounding=ROUND_DOWN)                              

            # Crear registro de pérdida
            new_gastos = GastosModel(
                gas_empresa=gastos.gas_empresa,                                
                gas_fecha=datetime.now(bogota_timezone).date(),
                gas_proveedor=gastos.gas_proveedor,
                gas_concepto=gastos.gas_concepto,
                gas_valor=Decimal(gastos.gas_valor).quantize(Decimal('0.01'), rounding=ROUND_DOWN),
                gas_unidades=cantidad_gastos,
            )
            self.db.add(new_gastos)
            self.db.flush()

            # Crear reporte asociado (ahora incluyendo el nombre del cliente)
            observacion = (f"El usuario {nombre_cliente} registro un gasto de {gastos.gas_concepto} \n "
                        f"cantidad: {cantidad_gastos} unidades\nTotal: ${gastos.gas_valor:,.2f}")
            
            new_reporte = Reportes(
                rep_cli=usu_id,
                rep_asunto=f"Registra un gasto por {nombre_cliente}",
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