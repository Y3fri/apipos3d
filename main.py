from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine,Base
from middlewares.error_handler import ErrorHandler
from routers.empresa import empresa_router
from routers.estado import estado_router
from routers.sso_usuario import sso_usuario_router
from routers.categoria import categoria_router
from routers.medidas import medidas_router
from routers.transacciones import transacciones_router
from routers.metodo_pago import metodo_pago_router
from routers.producto import producto_router
from routers.inversion import inversion_router
from routers.venta import venta_router
from routers.pedido import pedido_router
from routers.perdidas import perdidas_router
from routers.reportes import reportes_router

app = FastAPI(
    title= 'Tienda1',
    description= 'API de inventario y contaduria de tiendas ',
    version= '0.0.1',
    openapi_tags=[] 
)


origins = [    
    "http://localhost:3000",    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandler)
app.include_router(empresa_router)
app.include_router(estado_router)
app.include_router(sso_usuario_router)
app.include_router(categoria_router)
app.include_router(medidas_router)
app.include_router(transacciones_router)
app.include_router(metodo_pago_router)
app.include_router(producto_router)
app.include_router(inversion_router)
app.include_router(venta_router)
app.include_router(pedido_router)
app.include_router(perdidas_router)
app.include_router(reportes_router)



Base.metadata.create_all(bind=engine)