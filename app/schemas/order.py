from pydantic import BaseModel, Field
from typing import List, Dict, Any

class OrderItem(BaseModel):
    product_id: str = Field(..., alias="productId")
    qty: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {str: str}

class OrderCreate(BaseModel):
    user_id: str = Field(..., alias="userId")
    items: List[OrderItem]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {str: str}

class OrderResponse(BaseModel):
    id: str

class OrderListResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: dict