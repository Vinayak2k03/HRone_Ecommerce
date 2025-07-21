from typing import Dict, Any
from bson import ObjectId

from app.database import get_collection
from app.schemas.order import OrderCreate

async def create_order(order: OrderCreate) -> Dict[str, Any]:
    orders_collection = get_collection("orders")
    products_collection = get_collection("products")
    
    # Calculate total
    total = 0.0
    for item in order.items:
        product = await products_collection.find_one({"_id": ObjectId(item.product_id)})
        if product:
            total += product["price"] * item.qty
    
    order_dict = order.dict(by_alias=False)  # Use snake_case fields for DB
    order_dict["total"] = total
    
    result = await orders_collection.insert_one(order_dict)
    
    return {"id": str(result.inserted_id)}

async def list_orders(user_id: str, limit: int = 0, offset: int = 0) -> Dict[str, Any]:
    orders_collection = get_collection("orders")
    products_collection = get_collection("products")
    
    query = {"user_id": user_id}
    
    # Calculate total for pagination
    total_count = await orders_collection.count_documents(query)
    
    # Set default limit if not specified
    actual_limit = 10 if limit <= 0 else limit
    
    # Get orders with pagination
    cursor = orders_collection.find(query).sort("_id", 1).skip(offset).limit(actual_limit)
    orders = await cursor.to_list(length=actual_limit)
    
    # Format orders for API response with product details
    formatted_orders = []
    for order in orders:
        formatted_order = {
            "id": str(order["_id"]),
            "items": [],
            "total": order["total"]
        }
        
        # Fetch product details for each item using a more efficient approach
        product_ids = [ObjectId(item["product_id"]) for item in order["items"]]
        products = {}
        
        # Get all required products in one query instead of individual queries
        if product_ids:
            product_cursor = products_collection.find({"_id": {"$in": product_ids}})
            async for product in product_cursor:
                products[str(product["_id"])] = {
                    "name": product["name"],
                    "id": str(product["_id"])
                }
        
        # Assemble items with product details
        for item in order["items"]:
            product_id = item["product_id"]
            if product_id in products:
                formatted_item = {
                    "productDetails": products[product_id],
                    "qty": item["qty"]
                }
                formatted_order["items"].append(formatted_item)
        
        formatted_orders.append(formatted_order)
    
    # Calculate pagination values dynamically
    next_offset = offset + actual_limit if offset + actual_limit < total_count else None
    prev_offset = offset - actual_limit if offset - actual_limit >= 0 else -10
    
    return {
        "data": formatted_orders,
        "page": {
            "next": str(next_offset) if next_offset is not None else "10",
            "limit": limit,
            "previous": str(prev_offset) if prev_offset >= 0 else "-10"
        }
    }