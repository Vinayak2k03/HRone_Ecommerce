from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Size(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[Size] = []

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    sizes: List[Size] = []

class ProductListResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: dict