from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict

class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100000)
    email: str
    password: str = Field(..., min_length=6, max_length=100)
    role: str 

class UserUpdateRequest(BaseModel):
    name:str
    password:str = Field(..., min_length=6, max_length=100)


class CartRequest(BaseModel):
    user_id: int


class ProductRequest(BaseModel):
    id : int
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=1, max_length=1000)
    price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    category_id: int | None = None


class ProductUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=1, max_length=1000)
    price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)



class CategoryRequest(BaseModel):
    id:int
    name:str




class OrderRequest(BaseModel):
    id:int
    userid:int
    total:float




class CartItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)






    
class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(gt=0)




class ReviewRequest(BaseModel):
    product_id: int = Field(
        description="ID of the product being reviewed"
    )
    rating: int = Field(
        ge=1,
        le=5,
        description="Rating from 1 to 5"
    )
    comment: str = Field(
        min_length=1,
        max_length=1000,
        description="Review comment"
    )


class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    transaction_id: str



class ShippingRequest(BaseModel):
    orderid: int
    addressline1: str
    addressline2: str | None = None
    city: str
    postalcode: str
    country: str


class WishlistRequest(BaseModel):
    product_id: int


