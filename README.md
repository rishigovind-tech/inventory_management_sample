# 📦 Inventory Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Terminal%20%2F%20CLI-black?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)

**A complete, terminal-based Inventory Management System built with Python 3 and SQLite.**  
No external dependencies. No web framework. Pure Python.

</div>

---

## 📖 Project Overview

This Inventory Management System (IMS) is a fully functional, menu-driven command-line application designed to help businesses manage their product catalogue, track stock levels, record purchases and sales, and generate insightful inventory reports.

Built entirely with Python's standard library and SQLite, it demonstrates core software engineering skills including:

- **Relational database design** with foreign keys and constraints
- **Modular architecture** across 6 focused Python modules
- **CRUD operations** for products and suppliers
- **Business logic enforcement** (e.g., preventing overselling)
- **Data integrity** through input validation and transaction safety
- **Report generation** with aggregated SQL queries

---

## ✨ Features

### 🛍️ Product Management
| Feature | Description |
|---------|-------------|
| Add Product | Register new products with name, category, price, quantity, and supplier |
| Update Product | Modify any product field interactively |
| Delete Product | Remove products with confirmation prompt |
| View All Products | Tabular view of all registered products |
| Search Products | Partial-match search by product name or category |

### 🏢 Supplier Management
| Feature | Description |
|---------|-------------|
| Add Supplier | Register suppliers with name, contact, and email |
| Update Supplier | Edit supplier details interactively |
| Delete Supplier | Remove suppliers with confirmation |
| View All Suppliers | Tabular display of all suppliers |

### 📦 Inventory & Stock Management
| Feature | Description |
|---------|-------------|
| View Current Inventory | Full stock listing with quantities |
| Add Stock (Manual) | Manually increase a product's stock |
| Reduce Stock (Manual) | Write-off or adjustment deductions |
| Low Stock Alert | Lists products with ≤ 10 units remaining |
| Out of Stock Alert | Lists products with 0 units |

### 🛒 Purchase Management
| Feature | Description |
|---------|-------------|
| Record Purchase | Log purchases; stock automatically increases |
| Purchase History | All purchases stored with date |

### 💰 Sales Management
| Feature | Description |
|---------|-------------|
| Record Sale | Log sales; stock automatically decreases |
| Oversell Prevention | Blocks sales when stock is insufficient |
| Post-Sale Alerts | Notifies if stock becomes low or zero after sale |

### 📊 Reports
| # | Report | Description |
|---|--------|-------------|
| 1 | Total Products | Count of all registered products |
| 2 | Total Suppliers | Count of all registered suppliers |
| 3 | Total Purchases | Transaction count & total units purchased |
| 4 | Total Sales | Transaction count & total units sold |
| 5 | Low Stock Report | Products with ≤ 10 units |
| 6 | Out of Stock Report | Products with 0 units |
| 7 | Inventory Value Report | Per-product and total stock value (price × qty) |
| 8 | Top Selling Products | Top 10 ranked by total units sold |
| 9 | Full Summary | All 8 reports displayed sequentially |

---

## 🛠️ Technologies Used

| Component | Technology | Notes |
|-----------|------------|-------|
| Language | **Python 3.7+** | No external libraries |
| Database | **SQLite** (via `sqlite3`) | Standard library module |
| Interface | **Terminal / CLI** | Menu-driven, cross-platform |
| Modules used | `sqlite3`, `datetime`, `os`, `sys` | All standard library |

> ⚠️ **No Flask, Django, FastAPI, or GUI frameworks are used.**

---

## 🗃️ Database Schema

```sql
-- Suppliers table (must be created before products)
CREATE TABLE suppliers (
    supplier_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT    NOT NULL,
    contact       TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE
);

-- Products table with FK to suppliers
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT    NOT NULL,
    category     TEXT    NOT NULL,
    price        REAL    NOT NULL CHECK(price >= 0),
    quantity     INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
    supplier_id  INTEGER,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        ON DELETE SET NULL
);

-- Purchases: stock in
CREATE TABLE purchases (
    purchase_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id    INTEGER NOT NULL,
    quantity      INTEGER NOT NULL CHECK(quantity > 0),
    purchase_date TEXT    NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);

-- Sales: stock out
CREATE TABLE sales (
    sale_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity   INTEGER NOT NULL CHECK(quantity > 0),
    sale_date  TEXT    NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);
```

### Entity Relationship

```
suppliers ──< products ──< purchases
                       └──< sales
```

---

## 📁 Project Structure

```
inventory_management_system/
│
├── main.py          # Entry point — authentication, menus, navigation
├── database.py      # DB connection, schema creation, reusable query helpers
├── product.py       # Product CRUD — Add, Update, Delete, View, Search
├── supplier.py      # Supplier CRUD — Add, Update, Delete, View
├── inventory.py     # Stock management, purchase recording, sales recording
├── reports.py       # All 8 report functions + full summary
│
├── inventory.db     # SQLite database (auto-created on first run, git-ignored)
├── .gitignore       # Excludes .db files, __pycache__, .venv, IDE files
├── requirements.txt # No external dependencies (stdlib only)
├── LICENSE          # MIT License
└── README.md        # This file
```

---

## ⚙️ Installation

### Prerequisites

- **Python 3.7 or higher**

Verify:
```bash
python --version
```

No `pip install` required — **zero external dependencies**.

---

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/inventory-management-system-python-sqlite.git
cd inventory-management-system-python-sqlite
```

---

## ▶️ Usage

### Run the Application

```bash
python main.py
```

On first launch, `inventory.db` is automatically created.

### Login

```
Username : admin
Password : admin123
```

### Main Menu

```
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
```

### Recommended Workflow

```
1. Add Suppliers        → Supplier Management > Add Supplier
2. Add Products         → Product Management  > Add Product
3. Record Purchases     → Purchase Management > Record a Purchase
4. Record Sales         → Sales Management    > Record a Sale
5. Monitor Stock        → Inventory           > Low/Out of Stock Alerts
6. Generate Reports     → Reports             > Full Summary Report
```

---

## 🧪 Internship Requirements Checklist

| Requirement | Status |
|-------------|--------|
| ✅ Python only | No other language used |
| ✅ SQLite only | `sqlite3` standard library |
| ✅ Terminal-based application | Menu-driven CLI |
| ✅ No Flask | Not installed or imported |
| ✅ No Django | Not installed or imported |
| ✅ No FastAPI | Not installed or imported |
| ✅ No GUI frameworks | No Tkinter, PyQt, etc. |
| ✅ CRUD operations | Full CRUD for Products & Suppliers |
| ✅ Foreign keys enforced | `PRAGMA foreign_keys = ON` |
| ✅ Input validation | All inputs validated before DB write |
| ✅ Stock consistency | Purchases increase, Sales decrease stock |
| ✅ Reports generated | 8 report types + full summary |
| ✅ Data persists | SQLite `.db` file survives restarts |

---

## 🔐 Default Credentials

| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

> ⚠️ These are hardcoded for demonstration. In production, use hashed passwords (e.g., `bcrypt`).

---

## 🔄 Data Integrity & Validation

- **Foreign key constraints** enforced via `PRAGMA foreign_keys = ON`
- **CHECK constraints** prevent negative prices and quantities at the DB level
- **Cascade deletes** on purchases/sales when a product is removed
- **SET NULL** on `supplier_id` when a supplier is deleted (product is preserved)
- All user inputs validated before executing any SQL
- Duplicate supplier emails are rejected by the `UNIQUE` constraint
- Overselling is blocked with an explicit stock comparison before insert
- Date inputs validated against `YYYY-MM-DD` format using `datetime.strptime`

---

## 🚀 Future Improvements

- [ ] Hashed password authentication using `hashlib`
- [ ] Multiple user roles (Admin, Staff, Read-Only)
- [ ] Export reports to CSV using the `csv` module
- [ ] Product category filtering in reports
- [ ] Adjustable low-stock threshold per product
- [ ] Audit log (who changed what and when)
- [ ] Barcode / SKU support per product
- [ ] Batch import products from a CSV file

---

## 👨‍💻 Author

Developed as part of an internship project at **QubitEdge**  
Demonstrates Python programming, SQL database design, and modular software architecture.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with Python 3 + SQLite | Terminal-based | No external dependencies</sub>
</div>
