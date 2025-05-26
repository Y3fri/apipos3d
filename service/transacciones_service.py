from models.transacciones import Transacciones  as TransaccionesModel

class TransaccionesService():

    def __init__(self,db) -> None:
        self.db = db

    def get_transacciones(self):
        result=self.db.query(TransaccionesModel).all()
        return result  