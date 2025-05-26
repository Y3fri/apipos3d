import secrets
from fastapi import HTTPException
from sqlalchemy import func
from models.sso_usuario import Sso_usuario  as Sso_usuarioModule
from sqlalchemy.orm import Session
from utils.hash import hash_sha256_then_md5_then_sha1_and_sha512
from schemas.sso_usuario import Sso_usuario
from datetime import datetime, timedelta
import pytz

from utils.jwt_manager import create_token, validate_token

local_timezone = pytz.timezone('America/Bogota')

class Sso_usuarioService():

    def __init__(self, db: Session) -> None:
        self.db = db
        
    def get_sso_usuario(self):      
        result = self.db.query(Sso_usuarioModule).all()
        sso_usuario_list = [
            {
                "usu_id": sso_usuario.usu_id,
                "usu_empresa": sso_usuario.usu_empresa,                              
                "usu_documento": sso_usuario.usu_documento ,
                "usu_nombre": sso_usuario.usu_nombre ,
                "usu_apellido": sso_usuario.usu_apellido ,
                "usu_correo": sso_usuario.usu_correo ,
                "usu_nickname": sso_usuario.usu_nickname ,
                "usu_clave": sso_usuario.usu_clave ,                
                "nombre_empresa": sso_usuario.empresa.emp_razon_social,   
                            
            }
            for sso_usuario in result
        ]
        return sso_usuario_list

    
    def create_sso_usuario(self, sso_usuario: Sso_usuario):
        existing_user = self.db.query(Sso_usuarioModule).filter_by(usu_nickname=sso_usuario.usu_nickname).first()
        existing_user_by_correo = self.db.query(Sso_usuarioModule).filter_by(usu_correo=sso_usuario.usu_correo).first()

        if existing_user:
            raise ValueError("El nickname ya está en uso. Por favor, elige otro.")
        if existing_user_by_correo:
            raise ValueError("El correo electrónico ya está registrado. Por favor, usa otro correo.")
        
        new_sso_usuario = Sso_usuarioModule(
            usu_empresa = sso_usuario.usu_empresa,            
            usu_documento = sso_usuario.usu_documento,
            usu_nombre = sso_usuario.usu_nombre,
            usu_apellido = sso_usuario.usu_apellido,
            usu_correo = sso_usuario.usu_correo,
            usu_nickname = sso_usuario.usu_nickname,
            usu_clave = hash_sha256_then_md5_then_sha1_and_sha512(sso_usuario.usu_clave),
        )
        self.db.add(new_sso_usuario)
        self.db.commit()    
        return "Usuario creado exitosamente"
    
    def update_sso_usuario(self, id: int, sso_usuario: Sso_usuario):
        result = self.db.query(Sso_usuarioModule).filter(Sso_usuarioModule.usu_id == id).first()
        result.usu_empresa = sso_usuario.usu_empresa        
        result.usu_documento = sso_usuario.usu_documento
        result.usu_nombre = sso_usuario.usu_nombre
        result.usu_apellido = sso_usuario.usu_apellido
        result.usu_correo = sso_usuario.usu_correo
        result.usu_nickname = sso_usuario.usu_nickname
        result.usu_clave = sso_usuario.usu_clave        
        self.db.commit()
        return

    def authenticate_user(self, nickname: str, clave: str):   
        password = hash_sha256_then_md5_then_sha1_and_sha512(clave)
        user = self.db.query(Sso_usuarioModule).filter(Sso_usuarioModule.usu_nickname == nickname, Sso_usuarioModule.usu_clave == password).first()                   
        return user
