# Week 8 LabX ADV: Agentic Data Processing (Advanced CSV & JSON Workflows)

An "Agentic Data Processor" that runs CSV and JSON workflows defined in a declarative JSON config (`configs/data_pipeline_config.json`).

## Key Concepts Demonstrated
* **Agentic Workflow Orchestration**: `DataAgent` executes the tasks in the config sequentially.
* **Internal Data Store**: `data_store` passes intermediate results between tasks via `input_data_key` / `output_data_key`.
* **Advanced CSV Processing**: load, aggregate (sum/count/average), filter, save.
* **Advanced JSON Processing**: load, save, update nested data with dot-notation paths, query.
* **Cross-Format Conversion**: CSV to JSON and JSON to CSV.
* **Modularity**: `csv_tasks.py`, `json_tasks.py`, `conversion_tasks.py`, `config_parser.py`, `utils.py`.
* **Audit Logging**: every step is logged and saved to `reports/audit_report_*.json`.

## How to Run
```bash
cd labxadvanced
cd week8
python3 main.py
```
The pipeline will:
* Load `data/input_sales.csv`, aggregate sales by customer, save `data/processed_sales_by_customer.csv`
* Convert the raw sales data to JSON and save `data/sales_data.json`
* Load `data/input_inventory.json`, update stock/details, add PROD004, query a nested value, save `data/updated_inventory.json`
* Write an audit report to `reports/`

## Project Structure
```
labx-advanced/
├── src/
│   ├── __init__.py
│   ├── data_agent.py
│   ├── csv_tasks.py
│   ├── json_tasks.py
│   ├── conversion_tasks.py
│   ├── config_parser.py
│   └── utils.py
├── configs/
│   └── data_pipeline_config.json
├── data/
│   ├── input_sales.csv
│   ├── input_inventory.json
│   ├── processed_sales_by_customer.csv
│   ├── sales_data.json
│   └── updated_inventory.json
├── main.py
├── .gitignore
└── README.md
```

## Screenshots
Screenshots of the output files are in the `screenshots/` folder.
