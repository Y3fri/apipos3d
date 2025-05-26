from datetime import datetime
from sqlalchemy.orm import Session
from models.reportes import Reportes as ReporteModel

class ReportesService:
    def __init__(self, db: Session):
        self.db = db

    def get_reportes(self, fecha: str):
        try:                        
            result = self.db.query(ReporteModel).filter(ReporteModel.rep_fecha == fecha).all()
            
            reportes_list = [
                {                                
                    "rep_asunto": reportes.rep_asunto,
                    "rep_observacion": reportes.rep_observacion,
                    "rep_fecha": reportes.rep_fecha.strftime("%Y-%m-%d"),  
                    "rep_hora": str(reportes.rep_hora),
                }
                for reportes in result
            ]
            return reportes_list
            
        except ValueError as e:
            raise ValueError(f"Formato de fecha incorrecto. Use DD/MM/YYYY. Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al obtener reportes: {str(e)}")