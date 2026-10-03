"""
reports.py
----------
Generates all inventory and sales reports:
  1. Total Products
  2. Total Suppliers
  3. Total Purchases
  4. Total Sales
  5. Low Stock Report
  6. Out of Stock Report
  7. Inventory Value Report
  8. Top Selling Products
"""

from database import fetch_all, fetch_one
from inventory import LOW_STOCK_THRESHOLD


# ── Helper ────────────────────────────────────────────────────────────────────

def _section_header(title: str):
    """Print a styled section header."""
    width = 65
    print("\n" + "=" * width)
    print(f"  {title.upper()}")
    print("=" * width)


# ── Individual Report Functions ───────────────────────────────────────────────

def report_total_products():
    """Display the total number of products in the system."""
    _section_header("Report: Total Products")
    row = fetch_one("SELECT COUNT(*) AS total FROM products;")
    total = row["total"] if row else 0
    print(f"  Total Products Registered : {total}")


def report_total_suppliers():
    """Display the total number of suppliers."""
    _section_header("Report: Total Suppliers")
    row = fetch_one("SELECT COUNT(*) AS total FROM suppliers;")
    total = row["total"] if row else 0
    print(f"  Total Suppliers Registered: {total}")


def report_total_purchases():
    """Display total purchase transactions and total units purchased."""
    _section_header("Report: Total Purchases")
    row = fetch_one(
        "SELECT COUNT(*) AS transactions, COALESCE(SUM(quantity), 0) AS total_units "
        "FROM purchases;"
    )
    print(f"  Purchase Transactions : {row['transactions']}")
    print(f"  Total Units Purchased : {row['total_units']}")


def report_total_sales():
    """Display total sale transactions and total units sold."""
    _section_header("Report: Total Sales")
    row = fetch_one(
        "SELECT COUNT(*) AS transactions, COALESCE(SUM(quantity), 0) AS total_units "
        "FROM sales;"
    )
    print(f"  Sale Transactions : {row['transactions']}")
    print(f"  Total Units Sold  : {row['total_units']}")


def report_low_stock():
    """List all products with stock at or below the low-stock threshold."""
    _section_header(f"Report: Low Stock (≤ {LOW_STOCK_THRESHOLD} units)")

    products = fetch_all(
        "SELECT p.product_id, p.product_name, p.category, p.quantity "
        "FROM products p "
        "WHERE p.quantity > 0 AND p.quantity <= ? "
        "ORDER BY p.quantity ASC;",
        (LOW_STOCK_THRESHOLD,)
    )

    if not products:
        print(f"  [OK] No products are low on stock.")
        return

    print(f"\n  {'ID':<6} {'Product Name':<25} {'Category':<18} {'Qty':>6}")
    print("  " + "-" * 58)
    for p in products:
        print(
            f"  {p['product_id']:<6} "
            f"{p['product_name']:<25} "
            f"{p['category']:<18} "
            f"{p['quantity']:>6}"
        )
    print(f"\n  Total low-stock items: {len(products)}")


def report_out_of_stock():
    """List all products with zero stock."""
    _section_header("Report: Out of Stock")

    products = fetch_all(
        "SELECT p.product_id, p.product_name, p.category "
        "FROM products p "
        "WHERE p.quantity = 0 "
        "ORDER BY p.product_name;"
    )

    if not products:
        print("  [OK] No products are currently out of stock.")
        return

    print(f"\n  {'ID':<6} {'Product Name':<25} {'Category':<18}")
    print("  " + "-" * 50)
    for p in products:
        print(
            f"  {p['product_id']:<6} "
            f"{p['product_name']:<25} "
            f"{p['category']:<18}"
        )
    print(f"\n  Total out-of-stock items: {len(products)}")


def report_inventory_value():
    """
    Calculate total inventory value = SUM(price * quantity) for all products.
    Also list a per-product breakdown.
    """
    _section_header("Report: Inventory Value")

    products = fetch_all(
        "SELECT product_id, product_name, category, price, quantity, "
        "       (price * quantity) AS value "
        "FROM products "
        "ORDER BY value DESC;"
    )

    if not products:
        print("  [INFO] No products in inventory.")
        return

    print(f"\n  {'ID':<5} {'Product Name':<22} {'Category':<15} {'Price':>9} {'Qty':>5} {'Value':>12}")
    print("  " + "-" * 72)

    total_value = 0.0
    for p in products:
        total_value += p["value"]
        print(
            f"  {p['product_id']:<5} "
            f"{p['product_name']:<22} "
            f"{p['category']:<15} "
            f"{p['price']:>9.2f} "
            f"{p['quantity']:>5} "
            f"{p['value']:>12.2f}"
        )

    print("  " + "-" * 72)
    print(f"  {'TOTAL INVENTORY VALUE':>52} : {total_value:>12.2f}")


def report_top_selling():
    """
    Show the top 10 best-selling products ranked by total quantity sold.
    Joins the sales table with products.
    """
    _section_header("Report: Top Selling Products")

    results = fetch_all(
        "SELECT p.product_id, p.product_name, p.category, "
        "       SUM(s.quantity) AS total_sold, "
        "       COUNT(s.sale_id) AS num_transactions "
        "FROM sales s "
        "JOIN products p ON s.product_id = p.product_id "
        "GROUP BY s.product_id "
        "ORDER BY total_sold DESC "
        "LIMIT 10;"
    )

    if not results:
        print("  [INFO] No sales data available yet.")
        return

    print(f"\n  {'Rank':<5} {'Product Name':<25} {'Category':<15} {'Units Sold':>10} {'Transactions':>13}")
    print("  " + "-" * 72)

    for rank, row in enumerate(results, start=1):
        print(
            f"  {rank:<5} "
            f"{row['product_name']:<25} "
            f"{row['category']:<15} "
            f"{row['total_sold']:>10} "
            f"{row['num_transactions']:>13}"
        )

    print(f"\n  Showing top {len(results)} selling product(s).")


# ── Full Summary Report ────────────────────────────────────────────────────────

def full_summary_report():
    """Run all reports sequentially as a full dashboard summary."""
    print("\n\n" + "#" * 65)
    print("##  FULL INVENTORY MANAGEMENT REPORT  " + "#" * 27)
    print("#" * 65)

    report_total_products()
    report_total_suppliers()
    report_total_purchases()
    report_total_sales()
    report_inventory_value()
    report_low_stock()
    report_out_of_stock()
    report_top_selling()

    print("\n" + "=" * 65)
    print("  End of Report")
    print("=" * 65 + "\n")
