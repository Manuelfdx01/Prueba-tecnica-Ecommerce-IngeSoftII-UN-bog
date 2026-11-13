from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_product_service
from app.dependencies import require_admin
from app.models import User
from app.schemas import ProductCreate, ProductOut, ProductUpdate
from app.services.products import (
    ProductHasOrdersError,
    ProductNotFoundError,
    ProductService,
)

router = APIRouter(prefix="/products", tags=["Productos"])


@router.get("", response_model=list[ProductOut])
def list_products(
    q: str | None = None,
    category: str | None = None,
    service: ProductService = Depends(get_product_service),
):
    return service.list_products(q, category)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.get_product(product_id)
    except ProductNotFoundError:
        raise HTTPException(404, "Producto no encontrado")


@router.post("", response_model=ProductOut, status_code=201)
def create_product(
    payload: ProductCreate,
    _: User = Depends(require_admin),
    service: ProductService = Depends(get_product_service),
):
    return service.create_product(payload)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    _: User = Depends(require_admin),
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.update_product(product_id, payload)
    except ProductNotFoundError:
        raise HTTPException(404, "Producto no encontrado")


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    _: User = Depends(require_admin),
    service: ProductService = Depends(get_product_service),
):
    try:
        service.delete_product(product_id)
    except ProductNotFoundError:
        raise HTTPException(404, "Producto no encontrado")
    except ProductHasOrdersError:
        raise HTTPException(
            409,
            "No se puede eliminar: el producto pertenece a pedidos existentes. "
            "Puedes dejar sus existencias en cero.",
        )
