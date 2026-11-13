from pydantic import BaseModel,ConfigDict,EmailStr,Field
from typing import Literal
class UserCreate(BaseModel):
 name:str=Field(min_length=2,max_length=100)
 email:EmailStr
 password:str=Field(min_length=8,max_length=128)
class UserOut(BaseModel):
 id:int; name:str; email:EmailStr; role:str
 model_config=ConfigDict(from_attributes=True)
class TokenOut(BaseModel):
 access_token:str; token_type:str='bearer'; user:UserOut
class ProductCreate(BaseModel):
 name:str=Field(min_length=2,max_length=140)
 description:str=''
 price:float=Field(gt=0)
 stock:int=Field(ge=0)
 category:str='General'
 image_url:str=''
class ProductOut(ProductCreate):
 id:int
 model_config=ConfigDict(from_attributes=True)
class CartLine(BaseModel):
 product_id:int; quantity:int=Field(gt=0,le=50)
class CheckoutIn(BaseModel):
 items:list[CartLine]=Field(min_length=1,max_length=30)
 payment_method:Literal['simulated']='simulated'
class OrderItemOut(BaseModel):
 product_id:int; product_name:str; quantity:int; unit_price:float
 model_config=ConfigDict(from_attributes=True)
class OrderOut(BaseModel):
 id:int; status:str; payment_reference:str; total:float; items:list[OrderItemOut]
 model_config=ConfigDict(from_attributes=True)
