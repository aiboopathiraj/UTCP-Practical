from fastapi import FastAPI, HTTPException

app = FastAPI(title="Commerce Tools API")

PRODUCTS = [
      {"id": 1, "name": "Lenovo Laptop", "price": 55000},
      {"id": 2, "name": "HP Laptop", "price": 62000},
      {"id": 3, "name": "Samsung Phone", "price": 25000},
  ]
  
ORDERS = {
      101: {"status": "Shipped", "product": "Lenovo Laptop"},
      102: {"status": "Delivered", "product": "Samsung Phone"},
  }

@app.get("/")
async def root():
    return "Server Running in localhost:8000"

@app.get("/products", operation_id="search_products")
def search_products(
    query: str,
    max_price: float | None = None
):
    """Search products by name and optional maximum price."""
    results = [
        p for p in PRODUCTS
        if query.lower() in p["name"].lower()
        and (max_price is None or p["price"] <= max_price)
    ]
    return {"products": results}


@app.get("/orders/{order_id}", operation_id="get_order_status")
def get_order_status(order_id: int):
    """Get the delivery status of an order by ID."""
    if order_id not in ORDERS:
        raise HTTPException(404, "Order not found")
    return ORDERS[order_id]
