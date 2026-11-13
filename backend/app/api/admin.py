from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.dependencies import require_admin
from app.models import Order, Product, User
from app.schemas import OrderOut

router = APIRouter(prefix="/admin", tags=["Administración"])


@router.get("/orders", response_model=list[OrderOut])
def admin_orders(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    statement = (
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.id.desc())
    )
    return db.scalars(statement).all()


@router.get("/summary")
def admin_summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return {
        "products": db.scalar(select(func.count(Product.id))) or 0,
        "units_in_stock": db.scalar(
            select(func.coalesce(func.sum(Product.stock), 0))
        ) or 0,
        "orders": db.scalar(select(func.count(Order.id))) or 0,
        "revenue": float(
            db.scalar(select(func.coalesce(func.sum(Order.total), 0))) or 0
        ),
    }
