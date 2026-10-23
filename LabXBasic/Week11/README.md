# Week 11: Automating PDFs & Word Documents

Python automation with `PyPDF2` (extract text, merge PDFs) and `python-docx` (build a Word report).

## Run
```bash
python3 -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 main.py
```
Inputs (in `documents/`): `input_article.pdf`, `dummy_doc1.pdf`, `dummy_doc2.pdf`.
Outputs: `documents/output_report.docx` (extracted text + heading + table) and `documents/merged_output.pdf` (doc1 + doc2).
