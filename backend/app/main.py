from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api
from app.core.config import settings

app = FastAPI(
    title="NexoShop API",
    version="1.1.0",
    description="API REST para e-commerce simplificado",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
