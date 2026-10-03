"""
database.py
-----------
Handles SQLite database connection, initialization, and schema creation.
All tables are created here with proper foreign key constraints.
"""

import sqlite3
import os

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.db")


def get_connection():
    """
    Create and return a SQLite database connection.
    Enables foreign key support and row_factory for dict-like row access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key enforcement
    conn.row_factory = sqlite3.Row               # Rows accessible by column name
    return conn


def initialize_database():
    """
    Create all database tables if they do not already exist.
    Tables: suppliers, products, purchases, sales
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # ── Suppliers Table ─────────────────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT    NOT NULL,
                contact       TEXT    NOT NULL,
                email         TEXT    NOT NULL UNIQUE
            );
        """)

        # ── Products Table ───────────────────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT    NOT NULL,
                category     TEXT    NOT NULL,
                price        REAL    NOT NULL CHECK(price >= 0),
                quantity     INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
                supplier_id  INTEGER,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
                    ON DELETE SET NULL
            );
        """)

        # ── Purchases Table ──────────────────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                purchase_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id    INTEGER NOT NULL,
                quantity      INTEGER NOT NULL CHECK(quantity > 0),
                purchase_date TEXT    NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
                    ON DELETE CASCADE
            );
        """)

        # ── Sales Table ──────────────────────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity   INTEGER NOT NULL CHECK(quantity > 0),
                sale_date  TEXT    NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
                    ON DELETE CASCADE
            );
        """)

        conn.commit()
        print("[OK] Database initialized successfully.")

    except sqlite3.Error as e:
        print(f"[ERROR] Database initialization failed: {e}")
        conn.rollback()
    finally:
        conn.close()


def execute_query(query: str, params: tuple = ()):
    """
    Execute a write query (INSERT / UPDATE / DELETE) and return lastrowid.
    Returns -1 on failure.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"[ERROR] Integrity constraint violated: {e}")
        return -1
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        conn.rollback()
        return -1
    finally:
        conn.close()


def fetch_all(query: str, params: tuple = ()):
    """
    Execute a SELECT query and return all matching rows as a list of dicts.
    Returns an empty list on failure.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"[ERROR] Query failed: {e}")
        return []
    finally:
        conn.close()


def fetch_one(query: str, params: tuple = ()):
    """
    Execute a SELECT query and return the first matching row as a dict.
    Returns None if no row found or on failure.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f"[ERROR] Query failed: {e}")
        return None
    finally:
        conn.close()
