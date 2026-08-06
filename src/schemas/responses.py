from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict

class UserResponse(BaseModel):
    id:int
    name: str
    email: str
    role: str


class CartResponse(BaseModel):
    id: int
    user_id: int

class ProductResponse(BaseModel):
    id : int
    name: str
    description: str
    price: float
    stock: int

class CategoryResponse(BaseModel):
    name:str


class OrderResponse(BaseModel):
    id:int
    userid:int
    total:float


class OrderProductResponse(BaseModel):
    quantity:int
    order_id:int
    product_id:int



class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    model_config = ConfigDict(from_attributes=True)


class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product: ProductResponse
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ShippingResponse(BaseModel):
    id: int
    userid: int
    orderid: int
    addressline1: str
    addressline2: str | None = None
    city: str
    postalcode: str
    country: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WishlistResponse(BaseModel):
    id: int
    user_id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)




