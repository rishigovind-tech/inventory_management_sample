"""
product.py
----------
Handles all Product Management operations:
  - Add Product
  - Update Product
  - Delete Product
  - View All Products
  - Search Products
"""

from database import execute_query, fetch_all, fetch_one
from supplier import get_supplier_by_id


# ── Helpers ──────────────────────────────────────────────────────────────────

def print_products_table(products: list):
    """Pretty-print a list of product dicts as a formatted table."""
    if not products:
        print("\n  [INFO] No products found.")
        return

    # Header
    print("\n" + "=" * 95)
    print(f"  {'ID':<5} {'Product Name':<22} {'Category':<15} {'Price':>10} {'Qty':>6}  {'Supplier':<20}")
    print("=" * 95)

    for p in products:
        # Resolve supplier name
        supplier_name = "N/A"
        if p.get("supplier_id"):
            sup = get_supplier_by_id(p["supplier_id"])
            if sup:
                supplier_name = sup["supplier_name"]

        print(
            f"  {p['product_id']:<5} "
            f"{p['product_name']:<22} "
            f"{p['category']:<15} "
            f"{p['price']:>10.2f} "
            f"{p['quantity']:>6}  "
            f"{supplier_name:<20}"
        )

    print("=" * 95)
    print(f"  Total records: {len(products)}\n")


def get_product_by_id(product_id: int):
    """Return a single product dict by its ID, or None."""
    return fetch_one(
        "SELECT * FROM products WHERE product_id = ?;",
        (product_id,)
    )


def get_all_products():
    """Return a list of all products."""
    return fetch_all("SELECT * FROM products ORDER BY product_id;")


# ── CRUD Operations ───────────────────────────────────────────────────────────

def add_product():
    """Interactively prompt the user and insert a new product record."""
    print("\n  ── Add New Product ──────────────────────────────")

    # Collect inputs with validation
    product_name = input("  Product Name   : ").strip()
    if not product_name:
        print("  [ERROR] Product name cannot be empty.")
        return

    category = input("  Category       : ").strip()
    if not category:
        print("  [ERROR] Category cannot be empty.")
        return

    # Price validation
    try:
        price = float(input("  Price          : ").strip())
        if price < 0:
            raise ValueError
    except ValueError:
        print("  [ERROR] Price must be a non-negative number.")
        return

    # Quantity validation
    try:
        quantity = int(input("  Quantity       : ").strip())
        if quantity < 0:
            raise ValueError
    except ValueError:
        print("  [ERROR] Quantity must be a non-negative integer.")
        return

    # Optional supplier
    try:
        sup_input = input("  Supplier ID (leave blank to skip): ").strip()
        supplier_id = int(sup_input) if sup_input else None
        if supplier_id is not None:
            sup = get_supplier_by_id(supplier_id)
            if not sup:
                print(f"  [ERROR] Supplier with ID {supplier_id} does not exist.")
                return
    except ValueError:
        print("  [ERROR] Supplier ID must be an integer.")
        return

    # Insert record
    row_id = execute_query(
        "INSERT INTO products (product_name, category, price, quantity, supplier_id) "
        "VALUES (?, ?, ?, ?, ?);",
        (product_name, category, price, quantity, supplier_id)
    )

    if row_id and row_id > 0:
        print(f"\n  [SUCCESS] Product '{product_name}' added with ID {row_id}.")
    else:
        print("\n  [ERROR] Failed to add product.")


def update_product():
    """Interactively update an existing product's details."""
    print("\n  ── Update Product ───────────────────────────────")

    try:
        product_id = int(input("  Enter Product ID to update: ").strip())
    except ValueError:
        print("  [ERROR] Product ID must be an integer.")
        return

    product = get_product_by_id(product_id)
    if not product:
        print(f"  [ERROR] No product found with ID {product_id}.")
        return

    print(f"\n  Updating: {product['product_name']} (ID: {product_id})")
    print("  (Press Enter to keep the current value)\n")

    # Gather new values — fall back to existing if blank
    new_name = input(f"  Product Name [{product['product_name']}]: ").strip()
    new_name = new_name if new_name else product["product_name"]

    new_category = input(f"  Category [{product['category']}]: ").strip()
    new_category = new_category if new_category else product["category"]

    try:
        price_input = input(f"  Price [{product['price']:.2f}]: ").strip()
        new_price = float(price_input) if price_input else product["price"]
        if new_price < 0:
            raise ValueError
    except ValueError:
        print("  [ERROR] Invalid price.")
        return

    try:
        qty_input = input(f"  Quantity [{product['quantity']}]: ").strip()
        new_quantity = int(qty_input) if qty_input else product["quantity"]
        if new_quantity < 0:
            raise ValueError
    except ValueError:
        print("  [ERROR] Invalid quantity.")
        return

    try:
        sup_input = input(f"  Supplier ID [{product.get('supplier_id', 'N/A')}]: ").strip()
        if sup_input == "":
            new_supplier_id = product.get("supplier_id")
        elif sup_input.lower() == "none":
            new_supplier_id = None
        else:
            new_supplier_id = int(sup_input)
            sup = get_supplier_by_id(new_supplier_id)
            if not sup:
                print(f"  [ERROR] Supplier with ID {new_supplier_id} does not exist.")
                return
    except ValueError:
        print("  [ERROR] Supplier ID must be an integer.")
        return

    result = execute_query(
        "UPDATE products SET product_name=?, category=?, price=?, quantity=?, supplier_id=? "
        "WHERE product_id=?;",
        (new_name, new_category, new_price, new_quantity, new_supplier_id, product_id)
    )

    if result is not None and result >= 0:
        print(f"\n  [SUCCESS] Product ID {product_id} updated successfully.")
    else:
        print("\n  [ERROR] Failed to update product.")


def delete_product():
    """Delete a product by ID after confirmation."""
    print("\n  ── Delete Product ───────────────────────────────")

    try:
        product_id = int(input("  Enter Product ID to delete: ").strip())
    except ValueError:
        print("  [ERROR] Product ID must be an integer.")
        return

    product = get_product_by_id(product_id)
    if not product:
        print(f"  [ERROR] No product found with ID {product_id}.")
        return

    confirm = input(
        f"  Are you sure you want to delete '{product['product_name']}'? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("  [CANCELLED] Delete operation cancelled.")
        return

    result = execute_query(
        "DELETE FROM products WHERE product_id = ?;",
        (product_id,)
    )

    if result is not None and result >= 0:
        print(f"\n  [SUCCESS] Product '{product['product_name']}' deleted.")
    else:
        print("\n  [ERROR] Failed to delete product.")


def view_all_products():
    """Fetch and display all products."""
    print("\n  ── All Products ─────────────────────────────────")
    products = get_all_products()
    print_products_table(products)


def search_product():
    """Search products by name or category (case-insensitive partial match)."""
    print("\n  ── Search Products ──────────────────────────────")

    keyword = input("  Enter search keyword (name or category): ").strip()
    if not keyword:
        print("  [ERROR] Search keyword cannot be empty.")
        return

    pattern = f"%{keyword}%"
    products = fetch_all(
        "SELECT * FROM products WHERE product_name LIKE ? OR category LIKE ? "
        "ORDER BY product_name;",
        (pattern, pattern)
    )

    print(f"\n  Search results for '{keyword}':")
    print_products_table(products)
