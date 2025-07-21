from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, Dict, Any

from app.schemas.product import ProductCreate
from app.services.product_service import create_product, list_products

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
async def create_product_endpoint(product: ProductCreate):
    try:
        return await create_product(product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def list_products_endpoint(
    name: Optional[str] = Query(None, description="Filter by product name"),
    size: Optional[str] = Query(None, description="Filter by size"),
    limit: int = Query(0, description="Number of records to return"),
    offset: int = Query(0, description="Number of records to skip")
):
    try:
        return await list_products(name=name, size=size, limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))