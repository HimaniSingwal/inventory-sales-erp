# Inventory + Sales ERP (Django)

A minimal ERP system for handling Products, Inventory, and Sales using Python (Django) and SQLite.

---

## Features

### Product Management
- Add / Edit / Delete Products
- Unique SKU for each item

### Inventory Control
- Adjust stock In/Out
- Track stock movement history
- Auto stock reduction on sale
- Low stock alerts (below threshold)

### Sales Management
- Create Sale Entry
- Generate Invoice
- Print Invoice

### Dashboard Metrics
- Total Products
- Total Stock
- Inventory Value
- Low Stock Items
- Search & Sorting enabled

---

##  Tech Stack

- Python 3
- Django Framework
- SQLite Database
- Bootstrap 5 (UI)

---

##  How to Run

```bash
# Clone the repository
git clone https://github.com/HimaniSingwal/inventory-sales-erp.git

# Enter project folder
cd inventory-sales-erp

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
