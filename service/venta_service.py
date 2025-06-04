from sqlalchemy.orm import Session
from models.venta import Venta as VentaModel
from models.pedido import Pedido as PedidoModel
from models.producto import Producto as ProductoModel
from schemas.venta import Venta
from schemas.pedido import Pedido
from models.reportes import Reportes
from models.sso_usuario import Sso_usuario
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
import pytz
from sqlalchemy.sql import func
from decimal import Decimal,ROUND_HALF_UP


bogota_timezone = pytz.timezone("America/Bogota")

class VentaService:
    def __init__(self, db: Session):
        self.db = db


    def get_venta(self):      
        fecha_actual = datetime.now(bogota_timezone).date()        
        result = (
            self.db.query(VentaModel)
            .filter(VentaModel.ven_fecha == fecha_actual)
            .all()
        )
        venta_list = [
            {
                "ven_id": venta.ven_id,                
                "ven_empresa": venta.ven_empresa,
                "ven_transacciones": venta.ven_transacciones,
                "ven_pago": venta.ven_pago,
                "ven_usuario": venta.ven_usuario,
                "ven_fecha": venta.ven_fecha,
                "ven_hora": venta.ven_hora,                
                "ven_total": venta.ven_total,                
                "ven_cliente_contado": venta.ven_cliente_contado,
                "ven_dinero_recibido": venta.ven_dinero_recibido,
                "ven_cambio": venta.ven_cambio,
                "ven_descuento": venta.ven_descuento,                
                "nombre_tansaccion": venta.transacciones.tra_nombre,                
                "nombre_pago": venta.metodo_pago.pag_nombre,                  
            }
            for venta in result
        ]
        return venta_list

    def get_venta_date_transaccion(self, venta_emp, filtro_fecha, filtro_transaccion):
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
        query = self.db.query(VentaModel).filter(
            VentaModel.ven_empresa == venta_emp,
            VentaModel.ven_fecha >= fecha_inicio, 
            VentaModel.ven_fecha <= fecha_fin
        )

        # Manejo del filtro de tipo de transacción
        if filtro_transaccion == "Contado":
            query = query.filter(VentaModel.ven_transacciones == 1)
        elif filtro_transaccion == "Credito":
            query = query.filter(VentaModel.ven_transacciones == 2)
        elif filtro_transaccion != "Todo":
            raise ValueError("Filtro de transacción no válido. Opciones: Todo, Contado, Crédito.")

        # Ejecutar la consulta
        result = query.all()

        # Formatear los resultados en una lista
        venta_list = [
            {
                "ven_id": venta.ven_id,
                "ven_empresa": venta.ven_empresa,
                "ven_transacciones": venta.ven_transacciones,
                "ven_pago": venta.ven_pago,
                "ven_usuario": venta.ven_usuario,
                "ven_fecha": venta.ven_fecha,
                "ven_hora": venta.ven_hora,
                "ven_total": venta.ven_total,                
                "ven_cliente_contado": venta.ven_cliente_contado,
                "ven_dinero_recibido": venta.ven_dinero_recibido,
                "ven_cambio": venta.ven_cambio,
                "ven_descuento": venta.ven_descuento,                
                "nombre_tansaccion": venta.transacciones.tra_nombre,
                "nombre_pago": venta.metodo_pago.pag_nombre,
            }
            for venta in result
        ]

        return venta_list


    def create_venta(self, venta: Venta, pedidos: list[Pedido], usu_id: int):
        try:
            # Obtener información del usuario
            usuario = self.db.query(Sso_usuario).filter(Sso_usuario.usu_id == usu_id).first()
            if not usuario:
                raise ValueError(f"No se encontró el usuario con ID {usu_id}")
            nombre_vendedor = usuario.usu_nombre

            current_datetime = datetime.now(bogota_timezone)
            current_date = current_datetime.date()
            current_time = current_datetime.time().replace(microsecond=0)
            
            # Validar inventario y preparar datos para el reporte
            productos_info = []
            for pedido in pedidos:
                producto = self.db.query(ProductoModel).filter(ProductoModel.pro_id == pedido.ped_producto).first()
                if producto is None:
                    raise ValueError(f"El producto con ID {pedido.ped_producto} no existe.")
                
                cantidad_producto = Decimal(str(producto.pro_cantidad)).quantize(Decimal('0.000'))
                cantidad_pedido = Decimal(str(pedido.ped_cantidad)).quantize(Decimal('0.000'))

                if cantidad_producto < cantidad_pedido:
                    raise ValueError(f"No hay suficiente cantidad de {producto.pro_nombre}. Quedan {producto.pro_cantidad} unidades.")
                
                # Calcular precio unitario convirtiendo explícitamente a Decimal
                subtotal = Decimal(str(pedido.ped_preTotal)).quantize(Decimal('0.00'))
                precio_unitario = subtotal / cantidad_pedido if cantidad_pedido > 0 else Decimal('0.00')
                
                productos_info.append({
                    'id': producto.pro_id,
                    'nombre': producto.pro_nombre,
                    'cantidad': float(cantidad_pedido),
                    'precio': float(precio_unitario),
                    'subtotal': float(subtotal)
                })
            
            # Crear venta
            new_venta = VentaModel(
                ven_empresa=venta.ven_empresa,
                ven_transacciones=venta.ven_transacciones,
                ven_pago=venta.ven_pago,
                ven_usuario=venta.ven_usuario,
                ven_fecha=current_date,
                ven_hora=current_time,
                ven_total=Decimal(str(venta.ven_total)).quantize(Decimal('0.00')),                
                ven_cliente_contado=venta.ven_cliente_contado,
                ven_dinero_recibido=Decimal(str(venta.ven_dinero_recibido)).quantize(Decimal('0.00')),
                ven_cambio=Decimal(str(venta.ven_cambio)).quantize(Decimal('0.00')),
                ven_descuento=Decimal(str(venta.ven_descuento)).quantize(Decimal('0.00')),                
            )
            self.db.add(new_venta)
            self.db.flush()

            # Procesar pedidos y actualizar inventario
            for pedido in pedidos:
                producto = self.db.query(ProductoModel).filter(ProductoModel.pro_id == pedido.ped_producto).first()
                producto.pro_cantidad -= Decimal(str(pedido.ped_cantidad)).quantize(Decimal('0.000'))
                
                new_pedido = PedidoModel(
                    ped_venta=new_venta.ven_id,
                    ped_producto=pedido.ped_producto,
                    ped_cantidad=pedido.ped_cantidad,
                    ped_preTotal=Decimal(str(pedido.ped_preTotal)).quantize(Decimal('0.00')),
                )
                self.db.add(new_pedido)

            # Generar reporte detallado
            tipo_venta = ""
            cliente_info = ""
            
            if venta.ven_transacciones == 1:
                tipo_venta = "CONTADO"
                cliente_info = f"Cliente: {venta.ven_cliente_contado if venta.ven_cliente_contado else 'No especificado'}"
            elif venta.ven_transacciones == 2:
                tipo_venta = "CREDITO"
                cliente_info = f"Client: {venta.ven_cliente_contado if venta.ven_cliente_contado else 'No especificado'}"           
            
            detalles_productos = "\n".join(
                [f"- {p['nombre']}: {p['cantidad']} x ${p['precio']:,.2f} = ${p['subtotal']:,.2f}" 
                for p in productos_info]
            )

            observacion = (                
                f"Fecha: {current_date} Hora: {current_time}\n"                
                f"{cliente_info}\n"
                f"Total: ${new_venta.ven_total:,.2f}\n"
                f"Descuento: ${new_venta.ven_descuento:,.2f}\n"                
                f"Dinero recibido: ${new_venta.ven_dinero_recibido:,.2f}\n"
                f"Cambio: ${new_venta.ven_cambio:,.2f}\n"
                f"PRODUCTOS VENDIDOS:\n{detalles_productos}"
            )

            new_reporte = Reportes(
                rep_cli=usu_id,
                rep_asunto=f"Venta hecha por {nombre_vendedor}",
                rep_observacion=observacion,
                rep_fecha=current_date,
                rep_hora=current_time,                
            )
            self.db.add(new_reporte)

            self.db.commit()
            return {
                "success": True,
                "venta_id": new_venta.ven_id,
                "message": f"Venta {tipo_venta.lower()} registrada correctamente"
            }

        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error en la base de datos: {str(e)}")
        except ValueError as ve:
            self.db.rollback()
            raise ValueError(str(ve))


    def update_venta(self, id: int, venta: Venta, usu_id: int):
        try:
            # Obtener información del usuario y la venta original
            usuario = self.db.query(Sso_usuario).filter(Sso_usuario.usu_id == usu_id).first()
            if not usuario:
                raise ValueError(f"No se encontró el usuario con ID {usu_id}")
            nombre_vendedor = usuario.usu_nombre

            venta_original = self.db.query(VentaModel).filter(VentaModel.ven_id == id).first()
            if not venta_original:
                raise ValueError(f"No se encontró la venta con ID {id}")

            current_datetime = datetime.now(bogota_timezone)
            current_date = current_datetime.date()
            current_time = current_datetime.time().replace(microsecond=0)

            # Guardar datos originales para el reporte
            fecha_original = venta_original.ven_fecha
            hora_original = venta_original.ven_hora
            cliente_nombre = venta_original.ven_cliente_contado or "Cliente no especificado"

            # Actualizar la venta
            venta_original.ven_empresa = venta.ven_empresa
            venta_original.ven_transacciones = 1 
            venta_original.ven_pago = venta.ven_pago
            venta_original.ven_usuario = venta.ven_usuario
            venta_original.ven_fecha = current_date
            venta_original.ven_hora = current_time
            venta_original.ven_total = venta.ven_total
            venta_original.ven_dinero_recibido = venta.ven_total
            venta_original.ven_cambio = venta.ven_cambio
            venta_original.ven_descuento = venta.ven_descuento

            # Crear reporte detallado
            observacion = (
                f"El día {current_date} a las {current_time} El cliente efectuó un pago en efectivo por un monto total de ${venta.ven_dinero_recibido:,.2f}, el vendedor {nombre_vendedor} "
                f"recibió un abono del credito del cliente {cliente_nombre} por la compra realizada de un monto total de ${venta.ven_total:,.2f}.\n"
                f"el {fecha_original} a las {hora_original}.\n"
                f"las fechas se actualizan al dia {current_date} a las {current_time}.\n"                            
            )

            new_reporte = Reportes(
                rep_cli=usu_id,
                rep_asunto=f"Abono recibido de {cliente_nombre}",
                rep_observacion=observacion,
                rep_fecha=current_date,
                rep_hora=current_time
            )
            self.db.add(new_reporte)

            self.db.commit()

            return {
                "success": True,
                "message": "Pago registrado correctamente",
                "venta_id": id,
                "cliente": cliente_nombre,
                "vendedor": nombre_vendedor,
                "total": float(venta.ven_total)
            }

        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al registrar el pago: {str(e)}")