from sqlalchemy.orm import Session
from models.pedido import Pedido as PedidoModel
from models.pedido import Pedido as PedidoModel
from models.producto import Producto as ProductoModel

class PedidoService:
    def __init__(self, db: Session):
        self.db = db


    def get_pedido(self, venta : int):                   
        result = (
            self.db.query(PedidoModel)
            .filter(PedidoModel.ped_venta == venta)
            .all()
        )
        pedido_list = [
            {
                "ped_id": pedido.ped_id,                
                "ped_venta": pedido.ped_venta,
                "ped_producto": pedido.ped_producto,
                "ped_preTotal": pedido.ped_preTotal,
                "ped_cantidad": pedido.ped_cantidad,
                "nombre_producto": pedido.producto.pro_nombre,  
                "precio_pacial": pedido.producto.pro_precio_base,                            
            }
            for pedido in result
        ]
        return pedido_list
