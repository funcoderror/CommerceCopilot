from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

PRODUCTS_PATH = DATA_DIR / "products.csv"
ORDERS_PATH = DATA_DIR / "orders.csv"


def load_data():
    products = pd.read_csv(PRODUCTS_PATH)
    orders = pd.read_csv(ORDERS_PATH)

    return products, orders


def validate_data(products, orders):

    # Required columns
    required_product_columns = [
        "product_id", "name", "category",
        "price", "stock", "description"
    ]

    required_order_columns = [
        "order_id", "customer_id", "product_id",
        "quantity", "status"
    ]

    # Check columns
    assert all(
        col in products.columns
        for col in required_product_columns
    ), "Missing product columns!"

    assert all(
        col in orders.columns
        for col in required_order_columns
    ), "Missing order columns!"

    # Check duplicate IDs
    assert products["product_id"].is_unique, "Duplicate product IDs!"
    assert orders["order_id"].is_unique, "Duplicate order IDs!"

    # Check important missing values
    assert products["name"].notna().all(), "Missing product names!"
    assert products["price"].notna().all(), "Missing product prices!"
    assert orders["order_id"].notna().all(), "Missing order IDs!"

    # Check invalid numerical values
    assert (products["price"] >= 0).all(), "Negative product price!"
    assert (products["stock"] >= 0).all(), "Negative stock!"

    print("Data validation successful!")


def show_summary(products, orders):

    print("\n--- PRODUCT DATA ---")
    print("Shape:", products.shape)
    print("\nProducts by category:")
    print(products["category"].value_counts())

    print("\nProducts currently out of stock:")
    print(products[products["stock"] == 0][["product_id", "name"]])

    print("\n--- ORDER DATA ---")
    print("Shape:", orders.shape)
    print("\nOrders by status:")
    print(orders["status"].value_counts())

    print("\nFirst 5 products:")
    print(products.head())

    print("\nFirst 5 orders:")
    print(orders.head())


def check_data_quality(products, orders):

    print("\n========== DATA QUALITY CHECK ==========")

    # 1. Duplicate records
    print("\nDuplicate product IDs:", products["product_id"].duplicated().sum())
    print("Duplicate order IDs:", orders["order_id"].duplicated().sum())

    # 2. Missing values
    print("\nMissing values in products:")
    print(products.isnull().sum())

    print("\nMissing values in orders:")
    print(orders.isnull().sum())

    # 3. Invalid values
    print("\nProducts with negative prices:")
    print(products[products["price"] < 0])

    print("\nProducts with negative stock:")
    print(products[products["stock"] < 0])

    # 4. Product categories
    print("\nAvailable categories:")
    print(products["category"].unique())

    # 5. Order statuses
    print("\nAvailable order statuses:")
    print(orders["status"].unique())


if __name__ == "__main__":

    products, orders = load_data()

    validate_data(products, orders)

    show_summary(products, orders)

    check_data_quality(products, orders)