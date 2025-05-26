from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.categoria import Categoria
from fastapi.encoders import jsonable_encoder
from schemas.categoria import Categoria
from service.categoria_service import CategoriaService


categoria_router = APIRouter()


@categoria_router.get('/categoria', tags=['Categoria'], response_model=list[Categoria],dependencies=[Depends(JWTBearer())])
def get_categoria() -> List[Categoria]:
        db = Session()
        try:
                result = CategoriaService(db).get_categoria()
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las categorias: {str(e)}"}, status_code=500)
        finally:
                db.close()



@categoria_router.get('/categoriaTodo', tags=['Categoria'], response_model=list[Categoria],dependencies=[Depends(JWTBearer())])
def get_categoriaTodo() -> List[Categoria]:
        db = Session()
        try:
                result = CategoriaService(db).get_categoriaTodo()
                return JSONResponse(content=jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener las categorias: {str(e)}"}, status_code=500)
        finally:
                db.close()



@categoria_router.post('/categoria', tags=['Categoria'], response_model=dict,dependencies=[Depends(JWTBearer())])
def create_categoria(categoria: Categoria) -> dict:
    db = Session()
    try:
        CategoriaService(db).create_categoria(categoria)
        return JSONResponse(content={"message": "Se han insertado los datos correctamente"}, status_code=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": f"Error al insertar los datos: {str(e)}"}, status_code=500)


@categoria_router.put('/categoria/{id}', tags=['Categoria'], response_model=dict,dependencies=[Depends(JWTBearer())])
def update_categoria(id: int, categoria: Categoria) -> dict:
        db = Session()
        try:             
                CategoriaService(db).update_categoria(id, categoria)
                return JSONResponse(content={"message": "Categoria actualizado"})
        except Exception as e:                
                return JSONResponse(content={"error": f"Error al actualizar el categoria: {str(e)}"}, status_code=500)
        finally:
                db.close()

