from models.medidas import Medidas  as MedidasModel

class MedidasService():

    def __init__(self,db) -> None:
        self.db = db

    def get_medidas(self):
        result=self.db.query(MedidasModel).all()
        return result  