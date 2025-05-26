import base64
from pathlib import Path
from sqlalchemy import func
from models.categoria import Categoria as CategoriaModel
from schemas.categoria import Categoria

class CategoriaService():

    def __init__(self,db) -> None:
        self.db = db

   
    def get_categoria(self):      
        result = self.db.query(CategoriaModel).filter(CategoriaModel.cat_estado== 1).all()
        categoria_list = [
            {
                "cat_id": categoria.cat_id,
                "cat_estado": categoria.cat_estado,
                "cat_nombre": categoria.cat_nombre,                
                "nombre_estado": categoria.estado.est_nombre,                
            }
            for categoria in result
        ]
        return categoria_list
    
    def get_categoriaTodo(self):      
        result = self.db.query(CategoriaModel).all()
        categoria_list = [
            {
                "cat_estado": categoria.cat_estado,
                "cat_nombre": categoria.cat_nombre,                
                "nombre_estado": categoria.estado.est_nombre,                 
            }
            for categoria in result
        ]
        return categoria_list



    def create_categoria(self, categoria: Categoria):          
        try:                        
            new_categoria = CategoriaModel(
                cat_estado=categoria.cat_estado,
                cat_nombre=categoria.cat_nombre,                              
            )
            self.db.add(new_categoria)
            self.db.commit()

        except Exception as e:         
            print(f"Error en la inserción: {str(e)}")
            self.db.rollback()
            raise
    
    def update_categoria(self, id: int, categoria: Categoria):
        result = self.db.query(CategoriaModel).filter(CategoriaModel.cat_id == id).first()        
        result.cat_estado = categoria.cat_estado                
        result.cat_nombre = categoria.cat_nombre
        self.db.commit()
        return
    