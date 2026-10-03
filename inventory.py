"""
inventory.py
------------
Handles all Inventory & Stock Management operations:
  - Add Stock
  - Reduce Stock
  - View Current Inventory
  - Low Stock Alerts  (threshold: <= 10 units)
  - Out of Stock Alerts (quantity == 0)

Also handles:
  - Record Purchase (increases stock)
  - Record Sale     (decreases stock, prevents overselling)
"""

from datetime import datetime
from database import execute_query, fetch_all, fetch_one
from product import get_product_by_id, get_all_products, print_products_table


# ── Constants ─────────────────────────────────────────────────────────────────

LOW_STOCK_THRESHOLD = 10   # Units at or below this value trigger low-stock alert


# ── Internal Stock Helpers ────────────────────────────────────────────────────

def _update_stock(product_id: int, delta: int):
    """
    Adjust the quantity of a product by `delta` (positive = add, negative = remove).
    Returns True on success, False on failure or insufficient stock.
    """
    product = get_product_by_id(product_id)
    if not product:
        print(f"  [ERROR] Product with ID {product_id} not found.")
        return False

    new_qty = product["quantity"] + delta
    if new_qty < 0:
        print(
            f"  [ERROR] Insufficient stock. Available: {product['quantity']}, "
            f"Requested: {abs(delta)}."
        )
        return False

    result = execute_query(
        "UPDATE products SET quantity = ? WHERE product_id = ?;",
        (new_qty, product_id)
    )
    return result is not None and result >= 0


def _get_today():
    """Return today's date as an ISO-8601 string (YYYY-MM-DD)."""
    return datetime.now().strftime("%Y-%m-%d")


# ── Inventory Display ─────────────────────────────────────────────────────────

def view_inventory():
    """Display the current stock levels for all products."""
    print("\n  ── Current Inventory ────────────────────────────")
    products = get_all_products()
    print_products_table(products)


# ── Stock Operations ──────────────────────────────────────────────────────────

def add_stock():
    """
    Manually add stock to a product.
    Useful for corrections outside of formal purchase records.
    """
    print("\n  ── Add Stock ────────────────────────────────────")

    try:
        product_id = int(input("  Enter Product ID: ").strip())
    except ValueError:
        print("  [ERROR] Product ID must be an integer.")
        return

    product = get_product_by_id(product_id)
    if not product:
        print(f"  [ERROR] No product found with ID {product_id}.")
        return

    print(f"  Product  : {product['product_name']}")
    print(f"  Current  : {product['quantity']} units")

    try:
        qty = int(input("  Quantity to add: ").strip())
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  [ERROR] Quantity must be a positive integer.")
        return

    if _update_stock(product_id, qty):
        print(f"\n  [SUCCESS] Added {qty} units to '{product['product_name']}'.")
        updated = get_product_by_id(product_id)
        print(f"  New stock level: {updated['quantity']} units.")
    else:
        print("\n  [ERROR] Stock update failed.")


def reduce_stock():
    """
    Manually reduce stock from a product.
    Useful for write-offs or damage corrections.
    """
    print("\n  ── Reduce Stock ─────────────────────────────────")

    try:
        product_id = int(input("  Enter Product ID: ").strip())
    except ValueError:
        print("  [ERROR] Product ID must be an integer.")
        return

    product = get_product_by_id(product_id)
    if not product:
        print(f"  [ERROR] No product found with ID {product_id}.")
        return

    print(f"  Product  : {product['product_name']}")
    print(f"  Current  : {product['quantity']} units")

    try:
        qty = int(input("  Quantity to reduce: ").strip())
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  [ERROR] Quantity must be a positive integer.")
        return

    if _update_stock(product_id, -qty):
        print(f"\n  [SUCCESS] Reduced {qty} units from '{product['product_name']}'.")
        updated = get_product_by_id(product_id)
        print(f"  New stock level: {updated['quantity']} units.")
    else:
        print("\n  [ERROR] Stock update failed.")


# ── Alert Views ───────────────────────────────────────────────────────────────

def view_low_stock():
    """Display products with stock at or below LOW_STOCK_THRESHOLD (but > 0)."""
    print(f"\n  ── Low Stock Alert (≤ {LOW_STOCK_THRESHOLD} units) ──────────────────")

    products = fetch_all(
        "SELECT * FROM products WHERE quantity > 0 AND quantity <= ? "
        "ORDER BY quantity ASC;",
        (LOW_STOCK_THRESHOLD,)
    )

    if not products:
        print(f"\n  [OK] No products are low on stock (threshold: {LOW_STOCK_THRESHOLD} units).")
        return

    print_products_table(products)


def view_out_of_stock():
    """Display products with zero stock."""
    print("\n  ── Out of Stock Alert ───────────────────────────")

    products = fetch_all(
        "SELECT * FROM products WHERE quantity = 0 ORDER BY product_name;"
    )

    if not products:
        print("\n  [OK] No products are out of stock.")
        return

    print_products_table(products)


# ── Purchase Management ───────────────────────────────────────────────────────

def record_purchase():
    """
    Record a product purchase:
      - Logs a row in the `purchases` table.
      - Automatically increases the product's stock.
    """
    print("\n  ── Record Purchase ──────────────────────────────")

    try:
        product_id = int(input("  Enter Product ID: ").strip())
    except ValueError:
        print("  [ERROR] Product ID must be an integer.")
        return

    product = get_product_by_id(product_id)
    if not product:
        print(f"  [ERROR] No product found with ID {product_id}.")
        return

    print(f"  Product  : {product['product_name']}")
    print(f"  Current  : {product['quantity']} units")

    try:
        qty = int(input("  Quantity Purchased: ").strip())
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  [ERROR] Quantity must be a positive integer.")
        return

    # Allow custom date or default to today
    date_input = input(f"  Purchase Date (YYYY-MM-DD) [default: {_get_today()}]: ").strip()
    purchase_date = date_input if date_input else _get_today()

    # Validate date format
    try:
        datetime.strptime(purchase_date, "%Y-%m-%d")
    except ValueError:
        print("  [ERROR] Invalid date format. Use YYYY-MM-DD.")
        return

    # Insert purchase record
    row_id = execute_query(
        "INSERT INTO purchases (product_id, quantity, purchase_date) VALUES (?, ?, ?);",
        (product_id, qty, purchase_date)
    )

    if row_id and row_id > 0:
        # Update stock
        if _update_stock(product_id, qty):
            updated = get_product_by_id(product_id)
            print(f"\n  [SUCCESS] Purchase recorded (ID: {row_id}).")
            print(f"  New stock level for '{product['product_name']}': {updated['quantity']} units.")
        else:
            print("\n  [ERROR] Purchase logged but stock update failed. Please check manually.")
    else:
        print("\n  [ERROR] Failed to record purchase.")


# ── Sales Management ──────────────────────────────────────────────────────────

def record_sale():
    """
    Record a product sale:
      - Validates sufficient stock before proceeding.
      - Logs a row in the `sales` table.
      - Automatically decreases the product's stock.
    """
    print("\n  ── Record Sale ──────────────────────────────────")

    try:
        product_id = int(input("  Enter Product ID: ").strip())
    except ValueError:
        print("  [ERROR] Product ID must be an integer.")
        return

    product = get_product_by_id(product_id)
    if not product:
        print(f"  [ERROR] No product found with ID {product_id}.")
        return

    print(f"  Product  : {product['product_name']}")
    print(f"  In Stock : {product['quantity']} units")

    if product["quantity"] == 0:
        print("  [ERROR] This product is out of stock. Sale cannot proceed.")
        return

    try:
        qty = int(input("  Quantity Sold: ").strip())
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  [ERROR] Quantity must be a positive integer.")
        return

    # Stock-sufficiency check
    if qty > product["quantity"]:
        print(
            f"  [ERROR] Insufficient stock. Available: {product['quantity']}, "
            f"Requested: {qty}."
        )
        return

    # Allow custom date or default to today
    date_input = input(f"  Sale Date (YYYY-MM-DD) [default: {_get_today()}]: ").strip()
    sale_date = date_input if date_input else _get_today()

    # Validate date format
    try:
        datetime.strptime(sale_date, "%Y-%m-%d")
    except ValueError:
        print("  [ERROR] Invalid date format. Use YYYY-MM-DD.")
        return

    # Insert sale record
    row_id = execute_query(
        "INSERT INTO sales (product_id, quantity, sale_date) VALUES (?, ?, ?);",
        (product_id, qty, sale_date)
    )

    if row_id and row_id > 0:
        if _update_stock(product_id, -qty):
            updated = get_product_by_id(product_id)
            print(f"\n  [SUCCESS] Sale recorded (ID: {row_id}).")
            print(f"  Remaining stock for '{product['product_name']}': {updated['quantity']} units.")

            # Post-sale alerts
            if updated["quantity"] == 0:
                print(f"  [ALERT] '{product['product_name']}' is now OUT OF STOCK!")
            elif updated["quantity"] <= LOW_STOCK_THRESHOLD:
                print(
                    f"  [ALERT] '{product['product_name']}' is LOW on stock "
                    f"({updated['quantity']} units remaining)."
                )
        else:
            print("\n  [ERROR] Sale logged but stock update failed. Please check manually.")
    else:
        print("\n  [ERROR] Failed to record sale.")
