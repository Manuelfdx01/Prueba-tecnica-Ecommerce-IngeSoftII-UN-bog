from app.models import Product
from app.ports.product_repository import ProductRepository
from app.schemas import ProductCreate, ProductUpdate


class ProductNotFoundError(Exception):
    """El producto solicitado no existe."""


class ProductHasOrdersError(Exception):
    """El producto no se puede eliminar porque tiene pedidos asociados."""


class ProductService:
    """Reglas de aplicación para administrar el catálogo."""

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def list_products(
        self,
        query: str | None = None,
        category: str | None = None,
    ) -> list[Product]:
        return self._repository.list(query, category)

    def get_product(self, product_id: int) -> Product:
        product = self._repository.get(product_id)
        if product is None:
            raise ProductNotFoundError
        return product

    def create_product(self, payload: ProductCreate) -> Product:
        return self._repository.create(payload)

    def update_product(
        self,
        product_id: int,
        changes: ProductUpdate,
    ) -> Product:
        product = self.get_product(product_id)
        return self._repository.update(product, changes)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        if self._repository.has_order_history(product_id):
            raise ProductHasOrdersError
        self._repository.delete(product)
