from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base,engine
from app.models import User,Product,Order,OrderItem
from app.api.routes import api
Base.metadata.create_all(bind=engine)
app=FastAPI(title='NexoShop API',version='1.0.0',description='API REST para e-commerce simplificado')
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(api,prefix='/api')
@app.get('/health')
def health(): return {'status':'ok'}
