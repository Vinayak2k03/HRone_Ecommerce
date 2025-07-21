from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import Dict, Any

from app.schemas.order import OrderCreate
from app.services.order_service import create_order, list_orders

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
async def create_order_endpoint(order: OrderCreate):
    try:
        return await create_order(order)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=Dict[str, Any])
async def list_orders_endpoint(
    user_id: str = Path(..., description="User ID"),
    limit: int = Query(0, description="Number of records to return"),
    offset: int = Query(0, description="Number of records to skip")
):
    try:
        return await list_orders(user_id=user_id, limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))