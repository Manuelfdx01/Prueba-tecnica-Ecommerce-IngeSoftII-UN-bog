from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import OrderItem, Product
from app.ports.product_repository import ProductRepository
from app.schemas import ProductCreate, ProductUpdate


class SqlAlchemyProductRepository(ProductRepository):
    """Adaptador de persistencia de productos basado en SQLAlchemy."""

    def __init__(self, session: Session):
        self._session = session

    def list(self, query: str | None, category: str | None) -> list[Product]:
        statement = select(Product).order_by(Product.id.desc())
        if query:
            statement = statement.where(Product.name.ilike(f"%{query}%"))
        if category:
            statement = statement.where(Product.category == category)
        return list(self._session.scalars(statement).all())

    def get(self, product_id: int) -> Product | None:
        return self._session.get(Product, product_id)

    def create(self, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())
        self._session.add(product)
        self._session.commit()
        self._session.refresh(product)
        return product

    def update(self, product: Product, changes: ProductUpdate) -> Product:
        for field, value in changes.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        self._session.commit()
        self._session.refresh(product)
        return product

    def has_order_history(self, product_id: int) -> bool:
        statement = (
            select(OrderItem.id)
            .where(OrderItem.product_id == product_id)
            .limit(1)
        )
        return self._session.scalar(statement) is not None

    def delete(self, product: Product) -> None:
        self._session.delete(product)
        self._session.commit()
