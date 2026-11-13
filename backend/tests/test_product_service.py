from dataclasses import dataclass
from decimal import Decimal

from app.schemas import ProductCreate
from app.services.products import (
    ProductHasOrdersError,
    ProductNotFoundError,
    ProductService,
)


@dataclass
class FakeProduct:
    id: int
    name: str


class FakeProductRepository:
    """Implementación de prueba del contrato ProductRepository."""

    def __init__(self):
        self.products = {1: FakeProduct(id=1, name="Producto de prueba")}
        self.order_history = set()

    def list(self, query, category):
        return list(self.products.values())

    def get(self, product_id):
        return self.products.get(product_id)

    def create(self, payload):
        product = FakeProduct(id=2, name=payload.name)
        self.products[product.id] = product
        return product

    def update(self, product, changes):
        if changes.name is not None:
            product.name = changes.name
        return product

    def has_order_history(self, product_id):
        return product_id in self.order_history

    def delete(self, product):
        self.products.pop(product.id, None)


def test_product_service_uses_repository_contract():
    repository = FakeProductRepository()
    service = ProductService(repository)

    result = service.list_products()

    assert result[0].name == "Producto de prueba"


def test_product_service_creates_product_through_repository():
    service = ProductService(FakeProductRepository())
    payload = ProductCreate(
        name="Nuevo producto",
        price=Decimal("12000.00"),
        stock=3,
    )

    product = service.create_product(payload)

    assert product.name == "Nuevo producto"


def test_product_service_rejects_missing_product():
    service = ProductService(FakeProductRepository())

    try:
        service.get_product(999)
    except ProductNotFoundError:
        return

    raise AssertionError("Se esperaba ProductNotFoundError")


def test_product_service_prevents_deleting_products_with_orders():
    repository = FakeProductRepository()
    repository.order_history.add(1)
    service = ProductService(repository)

    try:
        service.delete_product(1)
    except ProductHasOrdersError:
        return

    raise AssertionError("Se esperaba ProductHasOrdersError")
