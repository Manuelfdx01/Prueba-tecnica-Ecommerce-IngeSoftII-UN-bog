from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select,func
from sqlalchemy.orm import Session,selectinload
from app.core.database import get_db
from app.core.security import hash_password,verify_password,create_access_token
from app.dependencies import get_current_user,require_admin
from app.models import User,Product,Order,OrderItem
from app.schemas import UserCreate,UserOut,TokenOut,ProductCreate,ProductUpdate,ProductOut,CheckoutIn,OrderOut
from app.services.orders import checkout
api=APIRouter()
@api.post('/auth/register',response_model=UserOut,status_code=201)
def register(payload:UserCreate,db:Session=Depends(get_db)):
 email=str(payload.email).lower()
 if db.scalar(select(User).where(User.email==email)): raise HTTPException(409,'Este correo ya está registrado')
 user=User(name=payload.name,email=email,hashed_password=hash_password(payload.password)); db.add(user); db.commit(); db.refresh(user); return user
@api.post('/auth/login',response_model=TokenOut)
def login(form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
 user=db.scalar(select(User).where(User.email==form.username.lower()))
 if not user or not verify_password(form.password,user.hashed_password): raise HTTPException(401,'Correo o contraseña incorrectos')
 return {'access_token':create_access_token(str(user.id)),'user':user}
@api.get('/auth/me',response_model=UserOut)
def me(user:User=Depends(get_current_user)): return user
@api.get('/products',response_model=list[ProductOut])
def list_products(q:str|None=None,category:str|None=None,db:Session=Depends(get_db)):
 stmt=select(Product).order_by(Product.id.desc())
 if q: stmt=stmt.where(Product.name.ilike('%'+q+'%'))
 if category: stmt=stmt.where(Product.category==category)
 return db.scalars(stmt).all()
@api.get('/products/{product_id}',response_model=ProductOut)
def get_product(product_id:int,db:Session=Depends(get_db)):
 p=db.get(Product,product_id)
 if not p: raise HTTPException(404,'Producto no encontrado')
 return p
@api.post('/products',response_model=ProductOut,status_code=201)
def create_product(payload:ProductCreate,db:Session=Depends(get_db),_:User=Depends(require_admin)):
 p=Product(**payload.model_dump()); db.add(p); db.commit(); db.refresh(p); return p
@api.patch('/products/{product_id}',response_model=ProductOut)
def update_product(product_id:int,payload:ProductUpdate,db:Session=Depends(get_db),_:User=Depends(require_admin)):
 p=db.get(Product,product_id)
 if not p: raise HTTPException(404,'Producto no encontrado')
 for k,v in payload.model_dump(exclude_unset=True).items(): setattr(p,k,v)
 db.commit(); db.refresh(p); return p
@api.delete('/products/{product_id}',status_code=204)
def delete_product(product_id:int,db:Session=Depends(get_db),_:User=Depends(require_admin)):
 p=db.get(Product,product_id)
 if not p: raise HTTPException(404,'Producto no encontrado')
 if db.scalar(select(OrderItem.id).where(OrderItem.product_id==product_id).limit(1)):
  raise HTTPException(409,'No se puede eliminar: el producto pertenece a pedidos existentes. Puedes dejar sus existencias en cero.')
 db.delete(p); db.commit()
@api.post('/orders/checkout',response_model=OrderOut,status_code=201)
def create_order(payload:CheckoutIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
 return checkout(db,user.id,[x.model_dump() for x in payload.items])
@api.get('/orders/me',response_model=list[OrderOut])
def my_orders(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
 stmt=select(Order).options(selectinload(Order.items)).where(Order.user_id==user.id).order_by(Order.id.desc())
 return db.scalars(stmt).all()
@api.get('/admin/orders',response_model=list[OrderOut])
def admin_orders(db:Session=Depends(get_db),_:User=Depends(require_admin)):
 stmt=select(Order).options(selectinload(Order.items)).order_by(Order.id.desc())
 return db.scalars(stmt).all()
@api.get('/admin/summary')
def admin_summary(db:Session=Depends(get_db),_:User=Depends(require_admin)):
 return {'products':db.scalar(select(func.count(Product.id))) or 0,'units_in_stock':db.scalar(select(func.coalesce(func.sum(Product.stock),0))) or 0,'orders':db.scalar(select(func.count(Order.id))) or 0,'revenue':float(db.scalar(select(func.coalesce(func.sum(Order.total),0))) or 0)}
