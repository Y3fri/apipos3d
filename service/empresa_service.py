from models.empresa import Empresa as EmpresaModel

class EmpresaService():

    def __init__(self,db) -> None:
        self.db = db

    def get_empresa(self, empresa_id: int):        
        result = self.db.query(EmpresaModel).filter(EmpresaModel.emp_id == empresa_id).first()
        return result 


