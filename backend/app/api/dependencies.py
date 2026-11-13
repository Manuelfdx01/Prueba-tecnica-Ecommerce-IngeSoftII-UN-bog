from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.sqlalchemy_product_repository import (
    SqlAlchemyProductRepository,
)
from app.services.products import ProductService


def get_product_service(
    db: Session = Depends(get_db),
) -> ProductService:
    repository = SqlAlchemyProductRepository(db)
    return ProductService(repository)
