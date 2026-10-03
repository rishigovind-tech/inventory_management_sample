"""
main.py
-------
Entry point for the Inventory Management System.

Provides:
  - Admin login (username: admin, password: admin123)
  - Hierarchical menu-driven terminal interface
  - Navigation across all modules:
      Product Management | Supplier Management | Inventory & Stock
      Purchase Management | Sales Management | Reports

Usage:
    python main.py
"""

import sys
import io
# Ensure UTF-8 output on all platforms (including Windows cp1252 terminals)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os
from database import initialize_database

# ── Module Imports ────────────────────────────────────────────────────────────
from product import (
    add_product, update_product, delete_product,
    view_all_products, search_product
)
from supplier import (
    add_supplier, update_supplier, delete_supplier,
    view_all_suppliers
)
from inventory import (
    add_stock, reduce_stock, view_inventory,
    view_low_stock, view_out_of_stock,
    record_purchase, record_sale
)
from reports import (
    report_total_products, report_total_suppliers,
    report_total_purchases, report_total_sales,
    report_low_stock, report_out_of_stock,
    report_inventory_value, report_top_selling,
    full_summary_report
)


# ── Credentials ───────────────────────────────────────────────────────────────

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ── UI Utilities ──────────────────────────────────────────────────────────────

def clear_screen():
    """Clear the terminal screen (works on Windows and Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Wait for the user to press Enter before returning to the menu."""
    input("\n  Press Enter to continue...")


def print_banner():
    """Display the application banner."""
    clear_screen()
    print("""
+==============================================================+
|                                                              |
|          INVENTORY MANAGEMENT SYSTEM  v1.0                   |
|                  Python + SQLite                             |
|                                                              |
+==============================================================+
""")


def print_main_menu():
    """Render the main navigation menu."""
    print("""
  +---------------------------------------------+
  |               MAIN MENU                     |
  +---------------------------------------------+
  |  1. Product Management                      |
  |  2. Supplier Management                     |
  |  3. Inventory & Stock Management            |
  |  4. Purchase Management                     |
  |  5. Sales Management                        |
  |  6. Reports                                 |
  |  0. Logout & Exit                           |
  +---------------------------------------------+
""")


# -- Authentication ------------------------------------------------------------

def login() -> bool:
    """
    Prompt for admin credentials.
    Returns True on success, False after 3 failed attempts.
    """
    print_banner()
    print("  Please log in to continue.\n")

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        username = input("  Username : ").strip()
        password = input("  Password : ").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print(f"\n  [OK] Welcome, {username.capitalize()}! Login successful.\n")
            pause()
            return True
        else:
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"  [ERROR] Invalid credentials. {remaining} attempt(s) remaining.\n")
            else:
                print("  [ERROR] Too many failed attempts. Access denied.")

    return False


# ── Sub-Menus ─────────────────────────────────────────────────────────────────

def menu_products():
    """Product Management sub-menu."""
    while True:
        clear_screen()
        print("""
  +---------------------------------------------+
  |           PRODUCT MANAGEMENT                |
  +---------------------------------------------+
  |  1. Add Product                             |
  |  2. Update Product                          |
  |  3. Delete Product                          |
  |  4. View All Products                       |
  |  5. Search Products                         |
  |  0. Back to Main Menu                       |
  +---------------------------------------------+
""")
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            view_all_products()
        elif choice == "5":
            search_product()
        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid option. Please try again.")

        pause()


def menu_suppliers():
    """Supplier Management sub-menu."""
    while True:
        clear_screen()
        print("""
  +---------------------------------------------+
  |           SUPPLIER MANAGEMENT               |
  +---------------------------------------------+
  |  1. Add Supplier                            |
  |  2. Update Supplier                         |
  |  3. Delete Supplier                         |
  |  4. View All Suppliers                      |
  |  0. Back to Main Menu                       |
  +---------------------------------------------+
""")
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            add_supplier()
        elif choice == "2":
            update_supplier()
        elif choice == "3":
            delete_supplier()
        elif choice == "4":
            view_all_suppliers()
        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid option. Please try again.")

        pause()


def menu_inventory():
    """Inventory & Stock Management sub-menu."""
    while True:
        clear_screen()
        print("""
  +---------------------------------------------+
  |        INVENTORY & STOCK MANAGEMENT         |
  +---------------------------------------------+
  |  1. View Current Inventory                  |
  |  2. Add Stock (Manual)                      |
  |  3. Reduce Stock (Manual)                   |
  |  4. Low Stock Alert                         |
  |  5. Out of Stock Alert                      |
  |  0. Back to Main Menu                       |
  +---------------------------------------------+
""")
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_stock()
        elif choice == "3":
            reduce_stock()
        elif choice == "4":
            view_low_stock()
        elif choice == "5":
            view_out_of_stock()
        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid option. Please try again.")

        pause()


def menu_purchases():
    """Purchase Management sub-menu."""
    while True:
        clear_screen()
        print("""
  +---------------------------------------------+
  |           PURCHASE MANAGEMENT               |
  +---------------------------------------------+
  |  1. Record a Purchase                       |
  |  0. Back to Main Menu                       |
  +---------------------------------------------+
""")
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            record_purchase()
        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid option. Please try again.")

        pause()


def menu_sales():
    """Sales Management sub-menu."""
    while True:
        clear_screen()
        print("""
  +---------------------------------------------+
  |             SALES MANAGEMENT                |
  +---------------------------------------------+
  |  1. Record a Sale                           |
  |  0. Back to Main Menu                       |
  +---------------------------------------------+
""")
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            record_sale()
        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid option. Please try again.")

        pause()


def menu_reports():
    """Reports sub-menu."""
    while True:
        clear_screen()
        print("""
  +---------------------------------------------+
  |                 REPORTS                     |
  +---------------------------------------------+
  |  1. Total Products                          |
  |  2. Total Suppliers                         |
  |  3. Total Purchases                         |
  |  4. Total Sales                             |
  |  5. Low Stock Report                        |
  |  6. Out of Stock Report                     |
  |  7. Inventory Value Report                  |
  |  8. Top Selling Products                    |
  |  9. Full Summary Report                     |
  |  0. Back to Main Menu                       |
  +---------------------------------------------+
""")
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            report_total_products()
        elif choice == "2":
            report_total_suppliers()
        elif choice == "3":
            report_total_purchases()
        elif choice == "4":
            report_total_sales()
        elif choice == "5":
            report_low_stock()
        elif choice == "6":
            report_out_of_stock()
        elif choice == "7":
            report_inventory_value()
        elif choice == "8":
            report_top_selling()
        elif choice == "9":
            full_summary_report()
        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid option. Please try again.")

        pause()


# ── Main Application Loop ─────────────────────────────────────────────────────

def main():
    """Initialize DB, authenticate, and run the main application loop."""

    # Step 1: Initialize the database (create tables if not exist)
    initialize_database()

    # Step 2: Authenticate the admin user
    if not login():
        print("\n  Exiting application. Goodbye.\n")
        sys.exit(1)

    # Step 3: Main menu loop
    while True:
        print_banner()
        print_main_menu()

        choice = input("  Enter choice: ").strip()

        if choice == "1":
            menu_products()
        elif choice == "2":
            menu_suppliers()
        elif choice == "3":
            menu_inventory()
        elif choice == "4":
            menu_purchases()
        elif choice == "5":
            menu_sales()
        elif choice == "6":
            menu_reports()
        elif choice == "0":
            print_banner()
            print("  Thank you for using the Inventory Management System.")
            print("  Goodbye!\n")
            sys.exit(0)
        else:
            print("  [ERROR] Invalid option. Please select a valid menu item.")
            pause()


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
