
import pandas as pd

# Load datasets
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")


# 1. Search for a product
def search_product(query):

    query = str(query).strip().lower()

    # Search by product ID or product name
    result = products[
        (products["product_id"].str.lower() == query) |
        (products["name"].str.lower().str.contains(query, na=False))
    ]

    if result.empty:
        return {"error": "No matching product found."}

    return result.head(5).to_dict(orient="records")


# 2. Check product inventory
def check_inventory(product_id):

    product_id = str(product_id).strip().upper()

    result = products[
        products["product_id"].str.upper() == product_id
    ]

    if result.empty:
        return {"error": "Product ID not found."}

    product = result.iloc[0]

    return {
        "product_id": product["product_id"],
        "name": product["name"],
        "stock": int(product["stock"]),
        "availability": (
            "In Stock" if product["stock"] > 0
            else "Out of Stock"
        )
    }


# 3. Retrieve order status
def get_order_status(order_id):

    order_id = str(order_id).strip().upper()

    result = orders[
        orders["order_id"].str.upper() == order_id
    ]

    if result.empty:
        return {"error": "Order ID not found."}

    order = result.iloc[0]

    return {
        "order_id": order["order_id"],
        "product_id": order["product_id"],
        "quantity": int(order["quantity"]),
        "order_status": order["order_status"],
        "payment_status": order["payment_status"],
        "total_amount": float(order["total_amount"]),
        "tracking_id": (
            None if pd.isna(order["tracking_id"])
            else order["tracking_id"]
        ),
        "estimated_delivery_date": (
            None if pd.isna(order["estimated_delivery_date"])
            else order["estimated_delivery_date"]
        ),
        "delivery_date": (
            None if pd.isna(order["delivery_date"])
            else order["delivery_date"]
        )
    }


# 4. Get overall product catalog summary
def get_catalog_summary():

    return {
        "total_products": len(products),

        "categories": products["category"].value_counts().to_dict(),

        "brands": products["brand"].value_counts().to_dict()
    }
