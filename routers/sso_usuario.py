from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.sso_usuario import Sso_usuario
from fastapi.encoders import jsonable_encoder
from schemas.user_usu import User_usu
from service.sso_usuaio_service import Sso_usuarioService
from schemas.sso_usuario import Sso_usuario
from utils.jwt_manager import create_token
from schemas.sso_usuario import Sso_usuario


sso_usuario_router = APIRouter()


@sso_usuario_router.get('/sso_usuario',tags=['Usuario'], response_model=list[Sso_usuario],dependencies=[Depends(JWTBearer())])
def get_sso_usuario()-> List [Sso_usuario]:
        db = Session()
        try:
                result = Sso_usuarioService(db).get_sso_usuario()
                return JSONResponse(content= jsonable_encoder(result))
        except Exception as e:        
                return JSONResponse(content={"error": f"Error al obtener los usuarios: {str(e)}"}, status_code=500)
        finally:
                db.close()


@sso_usuario_router.post('/sso_usuario',tags=['Usuario'],response_model=dict,dependencies=[Depends(JWTBearer())])
def create_usuario(usuario:Sso_usuario)-> dict:
        db = Session()
        try:
                Sso_usuarioService(db).create_sso_usuario(usuario)
                return JSONResponse(content={"message":"Se han insertado los datos correctamente"}, status_code=200)
        except Exception as e:
                return JSONResponse(content={"error": f"Error al insertar los datos: {str(e)}"}, status_code=500)


@sso_usuario_router.put('/sso_usuario/{id}', tags=['Usuario'], response_model=dict,dependencies=[Depends(JWTBearer())])
def update_sso_usuario(id: int, sso_usuario: Sso_usuario) -> dict:
        db = Session()
        try:               
                Sso_usuarioService(db).update_sso_usuario(id, sso_usuario)
                return JSONResponse(content={"message": "usuario actualizado"})
        except Exception as e:                
                return JSONResponse(content={"error": f"Error al actualizar el usuario: {str(e)}"}, status_code=500)
        finally:
                db.close()



@sso_usuario_router.post('/login', tags=['Auth'])
def login(user: User_usu):    
        db = Session()
        try:
                result =Sso_usuarioService(db).authenticate_user(user.usu_nickname, user.usu_clave)
                if result:  
                        user_data = {
                            "usu_nickname": result.usu_nickname,                          
                            "usu_id": result.usu_id,                            
                            "Rol": result.usu_rol,
                            "usu_empresa": result.usu_empresa,                            
                        }            
                        token = create_token(user_data)                                          
                        return {"token": token,"Rol": result.usu_rol,"usuario":result,"empresa":result.empresa}
                else:
                        raise HTTPException(status_code=401, detail="Credenciales inválidas")
        except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        finally:
                db.close()


