from fastapi import APIRouter

from app.api import admin, auth, orders, products

api = APIRouter()
api.include_router(auth.router)
api.include_router(products.router)
api.include_router(orders.router)
api.include_router(admin.router)
