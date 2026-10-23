# LabX Advanced: Advanced Spreadsheet Automation & Agentic Workflows

A JSON-configured "agent" that executes a list of tasks on an Excel workbook:
`copy_data`, `calculate_column`, `conditional_format`, `chart`. Every step is written to an
**Audit Log** sheet in the output workbook.

## Run
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install openpyxl
python3 create_sample_input.py   # creates data/input_data.xlsx (sheet "SalesData")
python3 main.py                  # creates data/output_report.xlsx
```

## Structure
```
labx-advanced/
├── src/
│   ├── __init__.py
│   ├── spreadsheet_agent.py        # task dispatcher + Excel operations
│   ├── config_parser.py            # loads / validates the JSON config
│   ├── utils.py                    # logging helpers
│   └── google_sheets_utils.py      # placeholder for gspread integration
├── configs/example_spreadsheet_config.json
├── data/
│   ├── input_data.xlsx
│   └── output_report.xlsx
├── screenshots/
├── create_sample_input.py
├── main.py
└── README.md
```

## Changes from the handout code (bugs fixed so it actually runs)
- `main.py`: relative import `from .src.utils ...` fails when run as `python main.py` → uses `sys.path` + `from src...`, and `chdir`s to the project root so config paths resolve.
- `config_parser.py`: validation demanded a `sheet` key on every task, but `copy_data` uses `source_sheet`/`dest_sheet` → validated per task type.
- `spreadsheet_agent.py`: `json` was used but never imported; the `expression` conditional-format called `conditional_formatting.add(..., ruleType=...)` (invalid) → now builds a `Rule`; solid fill is set so the colour shows in Excel.
- Config: chart `category_range` was `A1:A5` (included the header, misaligning labels) → `A2:A5`.
- Charts: `axis.delete = False` so axes are visible with openpyxl ≥ 3.1.
- Audit Log is built after the final log entry so the save step is included.

## Screenshots
`output_report.xlsx` – Audit Log

![audit](screenshots/output_report_audit_log.png)

`output_report.xlsx` – SalesData

![salesdata](screenshots/output_report_salesdata.png)

`output_report.xlsx` – Raw Data

![rawdata](screenshots/output_report_raw_data.png)
