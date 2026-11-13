from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.product import Product


def checkout(
    db: Session,
    user_id: int,
    lines: list[dict],
) -> Order:
    quantities = {}

    for line in lines:
        product_id = line["product_id"]
        quantities[product_id] = (
            quantities.get(product_id, 0) + line["quantity"]
        )

    if any(quantity > 50 for quantity in quantities.values()):
        raise HTTPException(422, "Máximo 50 unidades por producto")

    try:
        products = {}

        for product_id, quantity in quantities.items():
            result = db.execute(
                update(Product)
                .where(
                    Product.id == product_id,
                    Product.stock >= quantity,
                )
                .values(stock=Product.stock - quantity)
            )

            if result.rowcount != 1:
                raise HTTPException(
                    409,
                    f"Producto {product_id} inexistente o sin stock suficiente",
                )

            products[product_id] = db.get(Product, product_id)

        total = sum(
            (
                Decimal(str(products[product_id].price)) * quantity
                for product_id, quantity in quantities.items()
            ),
            Decimal("0.00"),
        )

        order = Order(
            user_id=user_id,
            status="paid",
            payment_reference=f"SIM-{uuid4().hex[:12].upper()}",
            total=total,
        )
        db.add(order)
        db.flush()

        for product_id, quantity in quantities.items():
            product = products[product_id]
            order_item = OrderItem(
                order_id=order.id,
                product_id=product_id,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.price,
            )
            db.add(order_item)

        db.commit()
        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise
