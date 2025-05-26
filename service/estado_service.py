from models.estado import Estado  as EstadoModel

class EstadoService():

    def __init__(self,db) -> None:
        self.db = db

    def get_estado(self):
        result=self.db.query(EstadoModel).all()
        return result  