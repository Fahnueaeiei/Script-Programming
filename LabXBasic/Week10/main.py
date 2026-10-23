# labx-basic/main.py
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from excel_processor import ExcelProcessor


def main():
    """Main entry point for the spreadsheet automation application."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, 'data', 'input_sales.xlsx')
    output_file = os.path.join(base_dir, 'data', 'output_sales_report.xlsx')

    os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("Run `python create_sample_input.py` first, or create it manually (see README.md).")
        return

    processor = ExcelProcessor()
    print(f"Starting sales data processing from '{input_file}'...")
    success = processor.process_sales_data(input_file, output_file)

    if success:
        print(f"Sales report successfully generated and saved to '{output_file}'.")
    else:
        print("Failed to generate sales report.")


if __name__ == "__main__":
    main()
