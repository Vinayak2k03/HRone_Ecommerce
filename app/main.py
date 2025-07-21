from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_to_mongo, close_mongo_connection
from app.routers import products, orders  # These are now directly the router objects

app = FastAPI(
    title="E-commerce API",
    description="E-commerce API with FastAPI and MongoDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Here, products and orders are already the router objects
app.include_router(products, prefix="/products", tags=["products"])
app.include_router(orders, prefix="/orders", tags=["orders"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the E-commerce API!"}