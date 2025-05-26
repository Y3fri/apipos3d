from models.inversion import Inversion as InversionModel
from models.producto import Producto  as ProductoModel
from schemas.producto import Producto
from schemas.inversion import Inversion
from sqlalchemy.exc import SQLAlchemyError
from models.sso_usuario import Sso_usuario
from models.reportes import Reportes
from decimal import Decimal
from datetime import datetime
import pytz

bogota_timezone = pytz.timezone("America/Bogota")


class ProductoService():

    def __init__(self,db) -> None:
        self.db = db
    

    def get_producto(self, pro_empresa: int):      
        result = self.db.query(ProductoModel).filter(ProductoModel.pro_estado== 1, ProductoModel.pro_empresa == pro_empresa).all()
        producto = [
            {
                "pro_id": producto.pro_id,                
                "pro_estado": producto.pro_estado,
                "pro_categoria": producto.pro_categoria,
                "pro_medida": producto.pro_medida,
                "pro_empresa": producto.pro_empresa,
                "pro_idbarras": producto.pro_idbarras,
                "pro_nombre": producto.pro_nombre,                
                "pro_cantidad": producto.pro_cantidad,
                "pro_precio_original": producto.pro_precio_original, 
                "pro_precio_base": producto.pro_precio_base,
                "pro_foto": producto.pro_foto,
                "pro_codigo": producto.pro_codigo,
                "nombre_estado": producto.estado.est_nombre,                
                "nombre_categoria": producto.categoria.cat_nombre,
                "nombre_medida": producto.medidas.med_nombre,
            }
            for producto in result
        ]
        return producto
    
    def get_producto_cantidad(self, pro_empresa: int):      
        result = self.db.query(ProductoModel).filter(ProductoModel.pro_estado== 1, ProductoModel.pro_empresa == pro_empresa, ProductoModel.pro_cantidad > 0).all()
                
        producto = [
            {
                "pro_id": producto.pro_id,                                                
                "pro_nombre": producto.pro_nombre,     
                "pro_cantidad": producto.pro_cantidad,           
            }
            for producto in result
        ]
        return producto
    
    def get_producto_cantidad_codigo(self, pro_empresa: int):      
        result = self.db.query(ProductoModel).filter(ProductoModel.pro_estado== 1, 
                                                     ProductoModel.pro_empresa == pro_empresa, 
                                                     ProductoModel.pro_cantidad > 0,
                                                     ProductoModel.pro_codigo.isnot(None)
                                                    ).all()
                
        producto = [
            {
                "pro_id": producto.pro_id,                                                                 
                "pro_codigo": producto.pro_codigo,              
            }
            for producto in result
        ]
        return producto
    
    def get_producto_id(self, pro_id: int):      
        result = self.db.query(ProductoModel).filter(ProductoModel.pro_id== pro_id).all()
        producto = [
            {
                "pro_id": producto.pro_id,                
                "pro_estado": producto.pro_estado,
                "pro_categoria": producto.pro_categoria,
                "pro_medida": producto.pro_medida,
                "pro_empresa": producto.pro_empresa,
                "pro_idbarras": producto.pro_idbarras,
                "pro_nombre": producto.pro_nombre,                
                "pro_cantidad": producto.pro_cantidad,
                "pro_precio_original": producto.pro_precio_original, 
                "pro_precio_base": producto.pro_precio_base,
                "pro_foto": producto.pro_foto,
                "pro_codigo": producto.pro_codigo,
                "nombre_estado": producto.estado.est_nombre,                
                "nombre_categoria": producto.categoria.cat_nombre,
                "nombre_medida": producto.medidas.med_nombre,
            }
            for producto in result
        ]
        return producto
    
    def get_producto_idbarras(self, pro_empresa: int, idbarras: int):      
        result = self.db.query(ProductoModel).filter(ProductoModel.pro_estado== 1, ProductoModel.pro_empresa == pro_empresa,ProductoModel.pro_idbarras == idbarras).all()
        
        if not result or all(producto.pro_cantidad <= 0 for producto in result):
            return {"mensaje": "No hay stock disponible para este producto."}

        producto = [
            {
                "pro_id": producto.pro_id,                
                "pro_estado": producto.pro_estado,
                "pro_categoria": producto.pro_categoria,
                "pro_medida": producto.pro_medida,
                "pro_empresa": producto.pro_empresa,
                "pro_idbarras": producto.pro_idbarras,
                "pro_nombre": producto.pro_nombre,                
                "pro_cantidad": producto.pro_cantidad,
                "pro_precio_original": producto.pro_precio_original, 
                "pro_precio_base": producto.pro_precio_base,
                "pro_foto": producto.pro_foto,
                "pro_codigo": producto.pro_codigo,
                "nombre_estado": producto.estado.est_nombre,                
                "nombre_categoria": producto.categoria.cat_nombre,
                "nombre_medida": producto.medidas.med_nombre,
            }
            for producto in result if producto.pro_cantidad > 0 
        ]
        return producto
    
    
    
    
    def get_productoTodo(self):      
        result = self.db.query(ProductoModel).all()
        producto_list = [
            {
                "pro_id": producto.pro_id,                
                "pro_estado": producto.pro_estado,
                "pro_categoria": producto.pro_categoria,
                "pro_medida": producto.pro_medida,
                "pro_empresa": producto.pro_empresa,
                "pro_idbarras": producto.pro_idbarras,
                "pro_nombre": producto.pro_nombre,                
                "pro_cantidad": producto.pro_cantidad,
                "pro_precio_original": producto.pro_precio_original, 
                "pro_precio_base": producto.pro_precio_base,
                "pro_foto": producto.pro_foto,
                "pro_codigo": producto.pro_codigo,
                "nombre_estado": producto.estado.est_nombre,                
                "nombre_categoria": producto.categoria.cat_nombre,  
                "nombre_medida": producto.medidas.med_nombre,              
            }
            for producto in result
        ]
        return producto_list



    def create_producto_inversion(self, producto: Producto, usu_id: int):
        try:            
            # Validaciones de producto existente
            existing_producto = (
                self.db.query(ProductoModel)
                .filter(
                    ProductoModel.pro_empresa == producto.pro_empresa,
                    ProductoModel.pro_idbarras == producto.pro_idbarras,
                    ProductoModel.pro_idbarras.isnot(None),
                    ProductoModel.pro_idbarras != ""
                )
                .first()
            )
            if existing_producto:
                raise ValueError(
                    f"El ID de barras '{producto.pro_idbarras}' ya está registrado en tu empresa."
                )

            existing_producto_nombre = (
                self.db.query(ProductoModel)
                .filter(
                    ProductoModel.pro_empresa == producto.pro_empresa,
                    ProductoModel.pro_nombre == producto.pro_nombre,
                )
                .first()
            )
            if existing_producto_nombre:
                raise ValueError(
                    f"El nombre del producto '{producto.pro_nombre}' ya está registrado en tu empresa."
                )
            
            existing_producto_codigo = (
                self.db.query(ProductoModel)
                .filter(
                    ProductoModel.pro_empresa == producto.pro_empresa,
                    ProductoModel.pro_codigo == producto.pro_codigo,
                    ProductoModel.pro_codigo.isnot(None),
                    ProductoModel.pro_codigo != ""
                )
                .first()
            )

            if existing_producto_codigo:
                raise ValueError(
                    f"El código del producto '{producto.pro_codigo}' ya está registrado en tu empresa."
                )
            
            # Obtener información del usuario/cliente
            usuario = self.db.query(Sso_usuario).filter(Sso_usuario.usu_id == usu_id).first()
            if not usuario:
                raise ValueError(f"No se encontró el usuario con ID {usu_id}")
            
            nombre_cliente = usuario.usu_nombre  # Obtenemos el nombre del cliente

            # Crear nuevo producto
            new_producto = ProductoModel(
                pro_estado=producto.pro_estado,
                pro_categoria=producto.pro_categoria,
                pro_medida=producto.pro_medida,
                pro_empresa=producto.pro_empresa,
                pro_idbarras=producto.pro_idbarras,
                pro_nombre=producto.pro_nombre,
                pro_cantidad=producto.pro_cantidad,
                pro_precio_original=producto.pro_precio_original,
                pro_precio_base=producto.pro_precio_base,
                pro_foto=producto.pro_foto,
                pro_codigo=producto.pro_codigo,
            )
            self.db.add(new_producto)
            self.db.flush()

            # Calcular total de inversión
            inv_total = Decimal(producto.pro_precio_original) * Decimal(producto.pro_cantidad)
            
            # Crear registro de inversión
            new_inversion = InversionModel(
                inv_empresa=producto.pro_empresa,
                inv_producto=new_producto.pro_id,
                inv_fecha=datetime.now(bogota_timezone).date(),
                inv_cantidad=producto.pro_cantidad,
                inv_precio_original_unitario=producto.pro_precio_original,
                inv_precio_base_unitario=producto.pro_precio_base,
                inv_total=inv_total
            )
            self.db.add(new_inversion)

            # Crear reporte/observación
            observacion = (
                f"El usuario {nombre_cliente} agregó un nuevo producto {producto.pro_nombre} "
                f"con una inversión de ${producto.pro_precio_original:,.2f} "
                f"(precio original), ${producto.pro_precio_base:,.2f} (precio base) y "
                f"una cantidad de {producto.pro_cantidad}. Inversión total: ${inv_total:,.2f}"
            )
            
            new_reporte = Reportes(
                rep_cli=usu_id,
                rep_asunto=f"Registro de nuevo producto por {nombre_cliente}",
                rep_observacion=observacion,
                rep_fecha=datetime.now(bogota_timezone).date(),
                rep_hora=datetime.now(bogota_timezone).time(),
            )
            self.db.add(new_reporte)

            self.db.commit()
            return {"message": "Producto creado, inversión registrada y reporte generado correctamente"}

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error en la base de datos: {str(e)}")
            raise ValueError(f"Error al interactuar con la base de datos: {str(e)}")

        except ValueError as ve:
            self.db.rollback()
            print(f"Error: {str(ve)}")
            raise ValueError(str(ve))

    
    def agregar_inversion(self, inversion: Inversion, usu_id: int):
        try:
            # Verificar que los campos importantes no sean None
            if not inversion.inv_empresa or not inversion.inv_producto:
                raise ValueError("Faltan campos requeridos para la inversión.")
            
            # Obtener información del usuario/cliente
            usuario = self.db.query(Sso_usuario).filter(Sso_usuario.usu_id == usu_id).first()
            if not usuario:
                raise ValueError(f"No se encontró el usuario con ID {usu_id}")
            
            nombre_cliente = usuario.usu_nombre  # Obtenemos el nombre del cliente

            new_inversion = InversionModel(
                inv_empresa=inversion.inv_empresa,
                inv_producto=inversion.inv_producto,
                inv_fecha=datetime.now(bogota_timezone).date(),
                inv_cantidad=Decimal(inversion.inv_cantidad),
                inv_precio_original_unitario=Decimal(inversion.inv_precio_original_unitario),
                inv_precio_base_unitario=Decimal(inversion.inv_precio_base_unitario),
                inv_total=Decimal(inversion.inv_precio_original_unitario) * Decimal(inversion.inv_cantidad),
            )
            self.db.add(new_inversion)
            self.db.flush()

            # Buscar el producto relacionado
            producto = self.db.query(ProductoModel).filter(ProductoModel.pro_id == inversion.inv_producto).first()
            if not producto:
                self.db.delete(new_inversion)
                self.db.commit()
                raise ValueError(f"No se encontró un producto con ID {inversion.inv_producto}.")

            # Validar que el producto pertenece a la empresa indicada
            if producto.pro_empresa != inversion.inv_empresa:
                self.db.delete(new_inversion)
                self.db.commit()
                raise ValueError(
                    f"El producto con ID {inversion.inv_producto} no pertenece a la empresa con ID {inversion.inv_empresa}."
                )

            # Actualizar el producto
            producto.pro_cantidad += Decimal(inversion.inv_cantidad)
            producto.pro_precio_original = Decimal(inversion.inv_precio_original_unitario)
            producto.pro_precio_base = Decimal(inversion.inv_precio_base_unitario)

            # Crear reporte/observación
            observacion = (
                f"El usuario {nombre_cliente} añadió una inversión al producto {producto.pro_nombre}. \n"
                f"Cantidad añadida: {inversion.inv_cantidad} unidades.\n "
                f"Precio original unitario: ${Decimal(inversion.inv_precio_original_unitario):,.2f}, \n"
                f"Precio base unitario: ${Decimal(inversion.inv_precio_base_unitario):,.2f}.\n "
                f"Total de la inversión: ${new_inversion.inv_total:,.2f}"
            )
            
            new_reporte = Reportes(
                rep_cli=usu_id,
                rep_asunto=f"Inversión añadida por {nombre_cliente}",
                rep_observacion=observacion,
                rep_fecha=datetime.now(bogota_timezone).date(),
                rep_hora=datetime.now(bogota_timezone).time(),
            )
            self.db.add(new_reporte)

            self.db.commit()
            return {
                "message": "Inversión registrada, producto actualizado y reporte generado correctamente",
                "inversion_id": new_inversion.inv_id
            }

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error en la base de datos: {str(e)}")
            raise ValueError(f"Error al interactuar con la base de datos: {str(e)}")

        except ValueError as ve:
            self.db.rollback()
            print(f"Error: {str(ve)}")
            raise ValueError(str(ve))

    def agregar_inversion_nombre(self, inversion: Inversion, nombre: str, usu_id: int):
        try:   
            if not inversion.inv_empresa:
                raise ValueError("Faltan campos requeridos para la inversión.")

            origen = Decimal(inversion.inv_precio_base_unitario) - (Decimal(inversion.inv_precio_base_unitario) * Decimal(0.20))

            # Buscar el producto en la base de datos
            producto = self.db.query(ProductoModel).filter(
                ProductoModel.pro_nombre == nombre,
                ProductoModel.pro_empresa == inversion.inv_empresa
            ).first()

            if not producto:
                # Crear nuevo producto si no existe
                new_producto = ProductoModel(
                    pro_estado=1,
                    pro_categoria=1,
                    pro_medida=1,
                    pro_empresa=inversion.inv_empresa,
                    pro_idbarras="",
                    pro_nombre=nombre,
                    pro_cantidad=Decimal(inversion.inv_cantidad),
                    pro_precio_original=origen,
                    pro_precio_base=Decimal(inversion.inv_precio_base_unitario),
                    pro_foto="1Anohayfoto.png",
                    pro_codigo="",
                )
                self.db.add(new_producto)
                self.db.flush()
                producto_id = new_producto.pro_id
            else:
                producto.pro_cantidad += Decimal(inversion.inv_cantidad)
                producto.pro_precio_original = origen
                producto.pro_precio_base = Decimal(inversion.inv_precio_base_unitario)
                producto_id = producto.pro_id

            # Crear registro de inversión
            new_inversion = InversionModel(
                inv_empresa=inversion.inv_empresa,
                inv_producto=producto_id,
                inv_fecha=datetime.now(bogota_timezone).date(),
                inv_cantidad=Decimal(inversion.inv_cantidad),
                inv_precio_original_unitario=origen,
                inv_precio_base_unitario=Decimal(inversion.inv_precio_base_unitario),
                inv_total=origen * Decimal(inversion.inv_cantidad),
            )
            self.db.add(new_inversion)

            # =============================================
            # SOLO ESTO ES NUEVO (COMO EN TUS OTROS MÉTODOS)
            usuario = self.db.query(Sso_usuario).filter(Sso_usuario.usu_id == usu_id).first()
            nombre_cliente = usuario.usu_nombre if usuario else str(usu_id)
            
            observacion = f"El usuario {nombre_cliente} registró inversión en producto por nombre de {nombre}, cantidad {inversion.inv_cantidad}, precio base ${Decimal(inversion.inv_precio_base_unitario):,.2f} y total de inversión ${new_inversion.inv_total:,.2f}"
            
            new_reporte = Reportes(
                rep_cli=usu_id,
                rep_asunto=f"Registro de inversión por nombre {nombre_cliente}",
                rep_observacion=observacion,
                rep_fecha=datetime.now(bogota_timezone).date(),
                rep_hora=datetime.now(bogota_timezone).time(),
            )
            self.db.add(new_reporte)
            # =============================================

            self.db.commit()
            return producto_id

        except SQLAlchemyError as e:
            self.db.rollback()            
            raise ValueError(f"Error al interactuar con la base de datos: {str(e)}")

        except ValueError as ve:
            self.db.rollback()            
            raise ValueError(str(ve))

        
    def update_producto(self, id: int, producto: Producto, usu_id: int):
        try:
            # Obtener información del usuario
            usuario = self.db.query(Sso_usuario).filter(Sso_usuario.usu_id == usu_id).first()
            if not usuario:
                raise ValueError(f"No se encontró el usuario con ID {usu_id}")
            nombre_cliente = usuario.usu_nombre

            # Obtener el producto existente
            result = self.db.query(ProductoModel).filter(ProductoModel.pro_id == id).first()
            if not result:
                raise ValueError(f"El producto con ID '{id}' no existe.")

            # Guardar los valores anteriores para el reporte
            valores_anteriores = {
                'nombre': result.pro_nombre,
                'cantidad': result.pro_cantidad,
                'precio_original': result.pro_precio_original,
                'precio_base': result.pro_precio_base,
                'estado': result.pro_estado,
                'codigo': result.pro_codigo,
                'idbarras': result.pro_idbarras
            }

            cantidad_anterior = result.pro_cantidad
            cambios = [] 
            
            if producto.pro_idbarras and producto.pro_idbarras != result.pro_idbarras:
                existing = self.db.query(ProductoModel).filter(
                    ProductoModel.pro_empresa == producto.pro_empresa,
                    ProductoModel.pro_idbarras == producto.pro_idbarras,
                    ProductoModel.pro_id != id
                ).first()
                if existing:
                    raise ValueError(f"El ID de barras '{producto.pro_idbarras}' ya está registrado.")
                cambios.append(f"ID de barras: {result.pro_idbarras} → {producto.pro_idbarras}")

            # Verificar nombre
            if producto.pro_nombre and producto.pro_nombre != result.pro_nombre:
                existing = self.db.query(ProductoModel).filter(
                    ProductoModel.pro_empresa == producto.pro_empresa,
                    ProductoModel.pro_nombre == producto.pro_nombre,
                    ProductoModel.pro_id != id
                ).first()
                if existing:
                    raise ValueError(f"El nombre '{producto.pro_nombre}' ya está registrado.")
                cambios.append(f"Nombre: {result.pro_nombre} → {producto.pro_nombre}")

            # Verificar código
            if producto.pro_codigo and producto.pro_codigo != result.pro_codigo:
                existing = self.db.query(ProductoModel).filter(
                    ProductoModel.pro_empresa == producto.pro_empresa,
                    ProductoModel.pro_codigo == producto.pro_codigo,
                    ProductoModel.pro_id != id
                ).first()
                if existing:
                    raise ValueError(f"El código '{producto.pro_codigo}' ya está registrado.")
                cambios.append(f"Código: {result.pro_codigo} → {producto.pro_codigo}")

            # Calcular diferencia de cantidad
            diferencia = Decimal(producto.pro_cantidad) - cantidad_anterior
            if diferencia != 0:
                cambios.append(f"Cantidad: {cantidad_anterior} → {producto.pro_cantidad} ({'+' if diferencia > 0 else ''}{diferencia})")

            # Verificar cambios en precios
            if producto.pro_precio_original != result.pro_precio_original:
                cambios.append(f"Precio original: {result.pro_precio_original} → {producto.pro_precio_original}")
            
            if producto.pro_precio_base != result.pro_precio_base:
                cambios.append(f"Precio base: {result.pro_precio_base} → {producto.pro_precio_base}")

            # Manejo de inversiones (código existente)
            if diferencia != 0:
                inversiones = self.db.query(InversionModel).filter(
                    InversionModel.inv_producto == id
                ).order_by(InversionModel.inv_id.desc()).all()

                if diferencia < 0:
                    cantidad_a_eliminar = abs(diferencia)
                    for inv in inversiones:
                        if cantidad_a_eliminar <= 0:
                            break
                        if inv.inv_cantidad <= cantidad_a_eliminar:
                            self.db.delete(inv)
                            cantidad_a_eliminar -= inv.inv_cantidad
                        else:
                            inv.inv_cantidad -= cantidad_a_eliminar
                            inv.inv_total = inv.inv_precio_original_unitario * inv.inv_cantidad
                            cantidad_a_eliminar = 0
                else:
                    nueva_inversion = InversionModel(
                        inv_producto=id,
                        inv_cantidad=diferencia,
                        inv_precio_original_unitario=producto.pro_precio_original,
                        inv_total=producto.pro_precio_original * diferencia,
                        inv_fecha=datetime.now(bogota_timezone).date()
                    )
                    self.db.add(nueva_inversion)
                    cambios.append(f"Nueva inversión registrada: +{diferencia} unidades")

            # Actualizar producto
            result.pro_estado = producto.pro_estado
            result.pro_categoria = producto.pro_categoria
            result.pro_medida = producto.pro_medida
            result.pro_idbarras = producto.pro_idbarras
            result.pro_nombre = producto.pro_nombre
            result.pro_cantidad = producto.pro_cantidad
            result.pro_precio_original = producto.pro_precio_original
            result.pro_precio_base = producto.pro_precio_base
            result.pro_foto = producto.pro_foto
            result.pro_codigo = producto.pro_codigo

            # Generar reporte detallado
            observacion = (
                f"El usuario {nombre_cliente} actualizó el producto {valores_anteriores['nombre']}.\n"
                f"Cambios realizados:\n- " + "\n- ".join(cambios) + "\n"
                f"Estado actual: {producto.pro_cantidad} unidades, "
                f"Precio original: {producto.pro_precio_original}, "
                f"Precio base: {producto.pro_precio_base}"
            )

            new_reporte = Reportes(
                rep_cli=usu_id,
                rep_asunto=f"Actualización de un producto por {nombre_cliente}",
                rep_observacion=observacion,
                rep_fecha=datetime.now(bogota_timezone).date(),
                rep_hora=datetime.now(bogota_timezone).time(),                
            )
            self.db.add(new_reporte)

            self.db.commit()
            return {"message": "Producto actualizado correctamente", "cambios": cambios}

        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error en la base de datos: {str(e)}")

        except ValueError as ve:
            self.db.rollback()
            raise ValueError(str(ve))