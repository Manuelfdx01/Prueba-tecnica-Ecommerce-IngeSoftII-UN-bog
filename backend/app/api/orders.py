from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models import Order, User
from app.schemas import CheckoutIn, OrderOut
from app.services.orders import checkout

router = APIRouter(prefix="/orders", tags=["Pedidos"])


@router.post("/checkout", response_model=OrderOut, status_code=201)
def create_order(
    payload: CheckoutIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items = [item.model_dump() for item in payload.items]
    return checkout(db, user.id, items)


@router.get("/me", response_model=list[OrderOut])
def my_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    statement = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == user.id)
        .order_by(Order.id.desc())
    )
    return db.scalars(statement).all()
