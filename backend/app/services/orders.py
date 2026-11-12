from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.order import Order,OrderItem
def checkout(db:Session,user_id:int,lines:list[dict])->Order:
 quantities={}
 for line in lines:
  pid=line['product_id']; quantities[pid]=quantities.get(pid,0)+line['quantity']
 if any(q>50 for q in quantities.values()): raise HTTPException(422,'Máximo 50 unidades por producto')
 try:
  products={}
  for pid,qty in quantities.items():
   result=db.execute(update(Product).where(Product.id==pid,Product.stock>=qty).values(stock=Product.stock-qty))
   if result.rowcount!=1: raise HTTPException(409,f'Producto {pid} inexistente o sin stock suficiente')
   products[pid]=db.get(Product,pid)
  total=sum(float(products[pid].price)*qty for pid,qty in quantities.items())
  order=Order(user_id=user_id,status='paid',payment_reference='SIM-'+uuid4().hex[:12].upper(),total=total)
  db.add(order); db.flush()
  for pid,qty in quantities.items():
   p=products[pid]; db.add(OrderItem(order_id=order.id,product_id=pid,product_name=p.name,quantity=qty,unit_price=p.price))
  db.commit(); db.refresh(order); return order
 except Exception:
  db.rollback(); raise
