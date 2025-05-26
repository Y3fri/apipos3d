from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException,Query
from fastapi.responses import FileResponse, JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.producto import Producto
from models.inversion import Inversion
from fastapi.encoders import jsonable_encoder
from schemas.producto import Producto
from schemas.inversion import Inversion
from service.producto_service import ProductoService

producto_router = APIRouter()


@producto_router.get('/producto/{pro_empresa}', tags=['Producto'], response_model=Producto,dependencies=[Depends(JWTBearer())])
def get_producto(pro_empresa):
        db = Session()
        try:
                result = ProductoService(db).get_producto(pro_empresa)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las productos: {str(e)}"}, status_code=500)
        finally:
                db.close()

@producto_router.get('/productoCant/{pro_empresa}', tags=['Producto'], response_model=Producto,dependencies=[Depends(JWTBearer())])
def get_producto_cantidad(pro_empresa):
        db = Session()
        try:
                result = ProductoService(db).get_producto_cantidad(pro_empresa)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las productos: {str(e)}"}, status_code=500)
        finally:
                db.close()  

@producto_router.get('/productoCantCodi/{pro_empresa}', tags=['Producto'], response_model=Producto,dependencies=[Depends(JWTBearer())])
def get_producto_cantidad_codigo(pro_empresa):
        db = Session()
        try:
                result = ProductoService(db).get_producto_cantidad_codigo(pro_empresa)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las productos: {str(e)}"}, status_code=500)
        finally:
                db.close()  

@producto_router.get('/productoId/{pro_id}', tags=['Producto'], response_model=Producto,dependencies=[Depends(JWTBearer())])
def get_producto_id(pro_id):
        db = Session()
        try:
                result = ProductoService(db).get_producto_id(pro_id)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las productos: {str(e)}"}, status_code=500)
        finally:
                db.close()              

@producto_router.get('/producto/{pro_empresa}/{idbarras}', tags=['Producto'], response_model=Producto,dependencies=[Depends(JWTBearer())])
def get_producto(pro_empresa, idbarras):
        db = Session()
        try:
                result = ProductoService(db).get_producto_idbarras(pro_empresa,idbarras)
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las productos: {str(e)}"}, status_code=500)
        finally:
                db.close()



@producto_router.get('/productoTodo', tags=['Producto'], response_model=list[Producto],dependencies=[Depends(JWTBearer())])
def get_productoTodo() -> List[Producto]:
        db = Session()
        try:
                result = ProductoService(db).get_productoTodo()
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las productos: {str(e)}"}, status_code=500)
        finally:
                db.close()


@producto_router.get("/empresas/{product_name}/file",tags=['Imagen'],dependencies=[Depends(JWTBearer())])
async def get_image(product_name: str):
    try:        
        product_folder_path = Path(f"empresas/{product_name}")
        file_name = f"{product_name}.jpeg"
        file_path = product_folder_path / file_name                
        if file_path.exists():
            return FileResponse(file_path, media_type="image/jpeg")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    
    
@producto_router.get("/images/{category}/{product_name}/file", tags=['Imagen'], dependencies=[Depends(JWTBearer())])
async def get_image(category: str, product_name: str):
    try:        
        base_folder = Path("images") / category
        file_path = base_folder / product_name
        
        # Depuración: imprimir el archivo y la ruta
        print(f"Buscando archivo en: {file_path}")
        
        # Verificar si el archivo existe
        if file_path.exists() and file_path.suffix[1:] in ["jpeg", "jpg", "png"]:
            return FileResponse(file_path, media_type=f"image/{file_path.suffix[1:]}")
        
        # Si no se encuentra, devolver 404
        raise HTTPException(status_code=404, detail="Image not found")    
    except Exception as e:
        # Log de errores adicionales
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@producto_router.get("/images/{category}/files", tags=['Imagen'], dependencies=[Depends(JWTBearer())])
async def get_images_in_category(category: str):
    try:
        # Definir la carpeta base
        base_folder = Path("images") / category
        
        # Verificar si la carpeta existe
        if not base_folder.exists() or not base_folder.is_dir():
            raise HTTPException(status_code=404, detail="Category not found")

        # Extensiones soportadas
        supported_extensions: List[str] = ["jpeg", "jpg", "png"]

        # Listar todos los archivos con las extensiones soportadas
        image_files = [
            str(file.name) for file in base_folder.iterdir()
            if file.suffix[1:] in supported_extensions and file.is_file()
        ]

        if not image_files:
            raise HTTPException(status_code=404, detail="No images found in the category")

        # Devolver la lista de archivos en formato JSON
        return JSONResponse(content={"images": image_files})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@producto_router.get("/images/{image_path:path}", tags=['Imagen'], dependencies=[Depends(JWTBearer())])
async def get_image(image_path: str):
    image_file = Path("images") / image_path
    if not image_file.exists() or not image_file.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_file)


@producto_router.post('/producto', tags=['Producto'], response_model=dict, dependencies=[Depends(JWTBearer())])
def create_producto_inversion(producto: Producto, usu_id : int) -> dict:
    db = Session()
    try:
        ProductoService(db).create_producto_inversion(producto,usu_id)
        return JSONResponse(content={"message": "Se han insertado los datos correctamente"}, status_code=200)
    except ValueError as ve:
        print(f"Error: {str(ve)}")
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return JSONResponse(content={"error": "Ocurrió un error inesperado"}, status_code=500)


@producto_router.post('/inversion', tags=['Inversion'], response_model=dict, dependencies=[Depends(JWTBearer())])
def agregar_inversion(inversion: Inversion, usu_id: int ) -> dict:
    db = Session()
    try:
        ProductoService(db).agregar_inversion(inversion,usu_id)
        return JSONResponse(content={"message": "Se han insertado los datos correctamente"}, status_code=200)
    except ValueError as ve:
        print(f"Error: {str(ve)}")
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return JSONResponse(content={"error": "Ocurrió un error inesperado"}, status_code=500)
    

@producto_router.post('/inversion/{nombre}', tags=['Inversion'], response_model=dict, dependencies=[Depends(JWTBearer())])
def agregar_inversion_nombre(inversion: Inversion, nombre: str, usu_id: int ) -> dict:
    db = Session()
    try:
        producto_id=ProductoService(db).agregar_inversion_nombre(inversion, nombre, usu_id)
        return JSONResponse(content={"message": "Se han insertado los datos correctamente","inv_producto": producto_id}, status_code=200)
    except ValueError as ve:
        print(f"Error: {str(ve)}")
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return JSONResponse(content={"error": "Ocurrió un error inesperado"}, status_code=500)
    

@producto_router.put('/producto/{id}', tags=['Producto'], response_model=dict,dependencies=[Depends(JWTBearer())])
def update_producto(id: int, producto: Producto, usu_id:int) -> dict:
        db = Session()
        try:             
                ProductoService(db).update_producto(id, producto, usu_id)
                return JSONResponse(content={"message": "Producto actualizado"})
        except Exception as e:                
                return JSONResponse(content={"error": f"Error al actualizar el producto: {str(e)}"}, status_code=500)
        finally:
                db.close()
