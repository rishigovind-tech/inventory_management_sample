"""
supplier.py
-----------
Handles all Supplier Management operations:
  - Add Supplier
  - Update Supplier
  - Delete Supplier
  - View All Suppliers
"""

from database import execute_query, fetch_all, fetch_one


# ── Helpers ──────────────────────────────────────────────────────────────────

def print_suppliers_table(suppliers: list):
    """Pretty-print a list of supplier dicts as a formatted table."""
    if not suppliers:
        print("\n  [INFO] No suppliers found.")
        return

    print("\n" + "=" * 75)
    print(f"  {'ID':<5} {'Supplier Name':<25} {'Contact':<15} {'Email':<25}")
    print("=" * 75)

    for s in suppliers:
        print(
            f"  {s['supplier_id']:<5} "
            f"{s['supplier_name']:<25} "
            f"{s['contact']:<15} "
            f"{s['email']:<25}"
        )

    print("=" * 75)
    print(f"  Total records: {len(suppliers)}\n")


def get_supplier_by_id(supplier_id: int):
    """Return a single supplier dict by its ID, or None."""
    return fetch_one(
        "SELECT * FROM suppliers WHERE supplier_id = ?;",
        (supplier_id,)
    )


def get_all_suppliers():
    """Return a list of all suppliers."""
    return fetch_all("SELECT * FROM suppliers ORDER BY supplier_id;")


# ── CRUD Operations ───────────────────────────────────────────────────────────

def add_supplier():
    """Interactively prompt the user and insert a new supplier record."""
    print("\n  ── Add New Supplier ─────────────────────────────")

    supplier_name = input("  Supplier Name  : ").strip()
    if not supplier_name:
        print("  [ERROR] Supplier name cannot be empty.")
        return

    contact = input("  Contact Number : ").strip()
    if not contact:
        print("  [ERROR] Contact number cannot be empty.")
        return

    email = input("  Email Address  : ").strip()
    if not email or "@" not in email:
        print("  [ERROR] A valid email address is required.")
        return

    row_id = execute_query(
        "INSERT INTO suppliers (supplier_name, contact, email) VALUES (?, ?, ?);",
        (supplier_name, contact, email)
    )

    if row_id and row_id > 0:
        print(f"\n  [SUCCESS] Supplier '{supplier_name}' added with ID {row_id}.")
    else:
        print("\n  [ERROR] Failed to add supplier. Email may already exist.")


def update_supplier():
    """Interactively update an existing supplier's details."""
    print("\n  ── Update Supplier ──────────────────────────────")

    try:
        supplier_id = int(input("  Enter Supplier ID to update: ").strip())
    except ValueError:
        print("  [ERROR] Supplier ID must be an integer.")
        return

    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        print(f"  [ERROR] No supplier found with ID {supplier_id}.")
        return

    print(f"\n  Updating: {supplier['supplier_name']} (ID: {supplier_id})")
    print("  (Press Enter to keep the current value)\n")

    new_name = input(f"  Supplier Name [{supplier['supplier_name']}]: ").strip()
    new_name = new_name if new_name else supplier["supplier_name"]

    new_contact = input(f"  Contact [{supplier['contact']}]: ").strip()
    new_contact = new_contact if new_contact else supplier["contact"]

    new_email = input(f"  Email [{supplier['email']}]: ").strip()
    if new_email and "@" not in new_email:
        print("  [ERROR] Invalid email format.")
        return
    new_email = new_email if new_email else supplier["email"]

    result = execute_query(
        "UPDATE suppliers SET supplier_name=?, contact=?, email=? WHERE supplier_id=?;",
        (new_name, new_contact, new_email, supplier_id)
    )

    if result is not None and result >= 0:
        print(f"\n  [SUCCESS] Supplier ID {supplier_id} updated successfully.")
    else:
        print("\n  [ERROR] Failed to update supplier.")


def delete_supplier():
    """Delete a supplier by ID after confirmation."""
    print("\n  ── Delete Supplier ──────────────────────────────")

    try:
        supplier_id = int(input("  Enter Supplier ID to delete: ").strip())
    except ValueError:
        print("  [ERROR] Supplier ID must be an integer.")
        return

    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        print(f"  [ERROR] No supplier found with ID {supplier_id}.")
        return

    confirm = input(
        f"  Are you sure you want to delete supplier '{supplier['supplier_name']}'? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("  [CANCELLED] Delete operation cancelled.")
        return

    result = execute_query(
        "DELETE FROM suppliers WHERE supplier_id = ?;",
        (supplier_id,)
    )

    if result is not None and result >= 0:
        print(f"\n  [SUCCESS] Supplier '{supplier['supplier_name']}' deleted.")
    else:
        print("\n  [ERROR] Failed to delete supplier.")


def view_all_suppliers():
    """Fetch and display all suppliers."""
    print("\n  ── All Suppliers ────────────────────────────────")
    suppliers = get_all_suppliers()
    print_suppliers_table(suppliers)
