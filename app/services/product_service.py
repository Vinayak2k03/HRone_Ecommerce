from typing import Optional, Dict, Any

from app.database import get_collection
from app.schemas.product import ProductCreate

async def create_product(product: ProductCreate) -> Dict[str, Any]:
    products_collection = get_collection("products")
    product_dict = product.dict()
    result = await products_collection.insert_one(product_dict)
    
    # Return just the ID as per requirement
    return {"id": str(result.inserted_id)}


async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 0,
    offset: int = 0
) -> Dict[str, Any]:
    products_collection = get_collection("products")
    
    # Build query
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size
    
    # Calculate total for pagination
    total_count = await products_collection.count_documents(query)
    
    # Set default limit if not specified
    actual_limit = 10 if limit <= 0 else limit
    
    # Get products with pagination
    cursor = products_collection.find(query).sort("_id", 1).skip(offset).limit(actual_limit)
    products = await cursor.to_list(length=actual_limit)
    
    # Format products for the response - include only id, name, and price
    formatted_products = []
    for product in products:
        formatted_products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"]
            # Note: sizes are intentionally excluded as per your example
        })
    
    # Calculate pagination values dynamically
    next_offset = offset + actual_limit if offset + actual_limit < total_count else None
    prev_offset = offset - actual_limit if offset - actual_limit >= 0 else -10
    
    return {
        "data": formatted_products,
        "page": {
            "next": str(next_offset) if next_offset is not None else "10",
            "limit": limit,
            "previous": str(prev_offset) if prev_offset >= 0 else "-10"
        }
    }