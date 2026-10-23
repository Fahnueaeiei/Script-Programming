# LabX Basic: Automating Spreadsheets (Excel)

Reads sales data from an Excel file, calculates the total per item and the grand total with
`openpyxl`, and writes a formatted report to a new Excel file.

## Run
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install openpyxl
python create_sample_input.py   # creates data/input_sales.xlsx (includes one blank row on purpose)
python main.py                  # creates data/output_sales_report.xlsx
```

## Structure
```
labx-basic/
├── src/
│   ├── __init__.py
│   └── excel_processor.py      # core logic
├── data/
│   ├── input_sales.xlsx
│   └── output_sales_report.xlsx
├── screenshots/
│   └── output_sales_report.png
├── create_sample_input.py
├── main.py
└── README.md
```

## Result
Grand total of the sample data = **3,203.97** (blank row is skipped).

![output_sales_report](screenshots/output_sales_report.png)
