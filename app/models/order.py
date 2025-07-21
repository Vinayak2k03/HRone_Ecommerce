from pydantic import BaseModel, Field
from typing import List, Dict, Any

class OrderItem(BaseModel):
    product_id: str = Field(..., alias="productId")
    qty: int

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class OrderCreate(BaseModel):
    user_id: str = Field(..., alias="userId")
    items: List[OrderItem]

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class OrderResponse(BaseModel):
    id: str

class OrderListResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: dict