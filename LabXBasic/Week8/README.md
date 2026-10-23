# Week 8 LabX BASIC: Automating with CSV and JSON Data

This project reads, processes and writes CSV and JSON files using Python's built-in `csv` and `json` modules.

## Key Concepts Demonstrated
* **CSV Reading (DictReader)** and **CSV Writing (DictWriter)**
* **CSV Data Processing**: total/average calculation and filtering (Amount >= 100)
* **JSON Reading (`json.load`)** and **JSON Writing (`json.dump`, pretty-printed)**
* **JSON Data Manipulation**: update stock levels, add a new product
* **Modular Design**: `csv_handler.py`, `json_handler.py`, `utils.py`
* **Robustness**: basic error handling and logging

## How to Run
```bash
cd labxbasic
cd week8
python3 main.py
```
The script will:
* Read `data/input_sales.csv`, filter rows with Amount >= 100, add a summary row, and write `data/output_filtered_sales.csv`
* Read `data/input_inventory.json`, update stock for PROD001 and PROD003, add PROD004, and write `data/output_updated_inventory.json`

## Project Structure
```
labx-basic/
├── src/
│   ├── __init__.py
│   ├── csv_handler.py
│   ├── json_handler.py
│   └── utils.py
├── data/
│   ├── input_sales.csv
│   ├── output_filtered_sales.csv
│   ├── input_inventory.json
│   └── output_updated_inventory.json
├── main.py
├── .gitignore
└── README.md
```

## Screenshots
Screenshots of the output files are in the `screenshots/` folder.
