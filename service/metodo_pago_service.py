from models.metodo_pago import Metodo_pago  as Metodo_pagoModel

class Metodo_pagoService():

    def __init__(self,db) -> None:
        self.db = db

    def get_metodo_pago(self):
        result=self.db.query(Metodo_pagoModel).all()
        return result  