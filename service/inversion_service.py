from models.inversion import Inversion as InversionModel
from datetime import datetime,timedelta
import pytz

bogota_timezone = pytz.timezone("America/Bogota")

class InversionService():

    def __init__(self,db) -> None:
        self.db = db

    def get_inversion(self, inversion_emp: int):        
        result = self.db.query(InversionModel).filter(InversionModel.inv_empresa == inversion_emp).all()
        inversion_list=[
            {
                "inv_id": inversion.inv_id,
                "inv_empresa": inversion.inv_empresa,
                "inv_producto": inversion.inv_producto,
                "inv_fecha": inversion.inv_fecha,
                "inv_cantidad": inversion.inv_cantidad,
                "inv_precio_original_unitario": inversion.inv_precio_original_unitario,
                "inv_precio_base_unitario": inversion.inv_precio_base_unitario,
                "inv_total": inversion.inv_total,
                "nombre_producto": inversion.producto.pro_nombre,                
            }
            for inversion in result
        ]
        return inversion_list    

    def get_inversion_fecha(self, inversion_emp: int, filtro_fecha: str):
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
        query = self.db.query(InversionModel).filter(
            InversionModel.inv_empresa == inversion_emp,
            InversionModel.inv_fecha >= fecha_inicio,
            InversionModel.inv_fecha <= fecha_fin
        )

        # Ejecutar la consulta
        result = query.all()

        # Formatear los resultados en una lista
        inversion_list = [
            {
                "inv_id": inversion.inv_id,
                "inv_empresa": inversion.inv_empresa,
                "inv_producto": inversion.inv_producto,
                "inv_fecha": inversion.inv_fecha,
                "inv_cantidad": inversion.inv_cantidad,
                "inv_precio_original_unitario": inversion.inv_precio_original_unitario,
                "inv_precio_base_unitario": inversion.inv_precio_base_unitario,
                "inv_total": inversion.inv_total,
                "nombre_producto": inversion.producto.pro_nombre,
            }
            for inversion in result
        ]
        
        return inversion_list     

    def get_inversion_id(self, inversion_emp: int,inv_id: int):        
        result = self.db.query(InversionModel).filter(InversionModel.inv_empresa == inversion_emp, InversionModel.inv_id==inv_id).all()

        inversion_list=[
            {
                "inv_id": inversion.inv_id,
                "inv_empresa": inversion.inv_empresa,
                "inv_producto": inversion.inv_producto,
                "inv_fecha": inversion.inv_fecha,
                "inv_cantidad": inversion.inv_cantidad,
                "inv_precio_original_unitario": inversion.inv_precio_original_unitario,
                "inv_precio_base_unitario": inversion.inv_precio_base_unitario,
                "inv_total": inversion.inv_total,
                "nombre_producto": inversion.producto.pro_nombre,
                "medida_producto": inversion.producto.medidas.med_nombre if inversion.producto.medidas else None,                
                "empresa_nombre": inversion.empresa.emp_razon_social,
            }
            for inversion in result
        ]
        return inversion_list
    