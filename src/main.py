from fastapi import FastAPI
from routers import cart_router, product_router, user_router,category_router,order_router
from routers import review_router, payment_router, shipping_router, wishlist_router


app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(category_router)
app.include_router(order_router)
app.include_router(review_router)
app.include_router(payment_router)
app.include_router(shipping_router)
app.include_router(wishlist_router)

