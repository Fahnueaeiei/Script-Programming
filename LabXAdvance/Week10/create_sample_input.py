# labx-advanced/create_sample_input.py
# Generates data/input_data.xlsx (sheet "SalesData") exactly as specified in the lab handout.
import os
import openpyxl

base_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "SalesData"
rows = [
    ("Product Name", "Quantity", "Unit Price"),
    ("Laptop", 2, 1200.50),
    ("Mouse", 5, 25.00),
    ("Keyboard", 3, 75.99),
    ("Monitor", 1, 300.00),
    ("Projector", 1, 850.00),
    ("Webcam", 10, 45.00),
    ("Headset", 4, 99.99),
    ("SSD", 2, 180.00),
    ("Router", 1, 70.00),
]
for r in rows:
    ws.append(r)
for cell in ws[1]:
    cell.font = openpyxl.styles.Font(bold=True)
ws.column_dimensions["A"].width = 16
ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 12
wb.save(os.path.join(base_dir, "data", "input_data.xlsx"))
print("Created data/input_data.xlsx")
