# labx-basic/create_sample_input.py
# Generates data/input_sales.xlsx (Sheet1) exactly as specified in the lab handout,
# including one intentionally empty row to show the script skips blank rows.
import os
import openpyxl

base_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Sheet1"
rows = [
    ("Product Name", "Quantity", "Unit Price"),
    ("Laptop", 2, 1200.50),
    ("Mouse", 5, 25.00),
    ("Keyboard", 3, 75.99),
    ("Monitor", 1, 300.00),
    (None, None, None),          # empty row on purpose
    ("Printer", 1, 150.00),
]
for r in rows:
    ws.append(r)
wb.save(os.path.join(base_dir, "data", "input_sales.xlsx"))
print("Created data/input_sales.xlsx")
