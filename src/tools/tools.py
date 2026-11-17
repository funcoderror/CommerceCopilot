
import pandas as pd
import re
from sentence_transformers import util
from src.embedding_model import embedding_model

# Load datasets
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")

# Prepare searchable product information
searchable_columns = [
    col for col in ["name", "brand", "category", "description"]
    if col in products.columns
]

product_texts = (
    products[searchable_columns]
    .fillna("")
    .astype(str)
    .agg(" ".join, axis=1)
    .tolist()
)

# Generate product embeddings once during initialization
product_embeddings = embedding_model.encode(
    product_texts,
    convert_to_tensor=True,
    normalize_embeddings=True
)

# 1. Search for a product
def search_product(query):

    query = str(query).strip().lower()

    if not query:
        return {"error": "Please provide a product name or query."}

    # STEP 1: Exact product ID matching
    result = products[
        products["product_id"].astype(str).str.lower() == query
    ]

    if not result.empty:
        return result.head(5).to_dict(orient="records")

    # STEP 2: Direct product name matching
    result = products[
        products["name"].astype(str).str.lower().str.contains(
            re.escape(query), na=False
        )
    ]

    if not result.empty:
        return result.head(5).to_dict(orient="records")

    # STEP 3: Clean conversational query
    stopwords = {
        "what", "is", "the", "of", "for", "me",
        "show", "find", "get", "much", "cost",
        "price", "tell", "about", "do", "you",
        "have", "a", "an", "i", "want", "looking"
    }

    cleaned_query = " ".join(
        word for word in re.sub(r"[^a-zA-Z0-9]+", " ", query).split()
        if word not in stopwords
    )

    if not cleaned_query:
        cleaned_query = query

    # STEP 4: Generate query embedding
    query_embedding = embedding_model.encode(
        cleaned_query,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    # STEP 5: Calculate semantic similarity
    similarities = util.cos_sim(
        query_embedding,
        product_embeddings
    )[0]

    # STEP 6: Retrieve top matching products
    top_indices = similarities.argsort(
        descending=True
    )[:5]

    results = []

    for idx in top_indices:
        score = similarities[idx].item()

        # Minimum relevance threshold
        if score >= 0.30:
            results.append(products.iloc[int(idx)].to_dict())

    if not results:
        return {"error": "No relevant products found."}

    return results


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
