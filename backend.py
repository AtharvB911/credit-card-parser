import sqlite3
import re
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfReader
import os


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Program Files\poppler\Library\bin" 

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# --- BANK PATTERNS ---
BANK_PATTERNS = {
    "HDFC": {
        "total_due": r"Total\s+Dues\s*:?\s*(?:Rs\.?)?\s*(?P<val>[\d,]+\.\d{2})",
        "due_date": r"Payment\s+Due\s+Date\s*:?\s*(?P<val>\d{2}/\d{2}/\d{4})",
        "statement_date": r"Statement\s+Date\s*:?\s*(?P<val>\d{2}/\d{2}/\d{4})",
        "credit_limit": r"Credit\s+Limit\s*:?\s*(?:Rs\.?)?\s*(?P<val>[\d,]+)",
        "card_no": r"Card\s+No\.\s*:?.*\s(?P<val>\d{4})$"
    },
    "SBI": {
        "total_due": r"Total\s+Amount\s+Due\s*:?\s*(?:Rs\.?)?\s*(?P<val>[\d,]+\.\d{2})",
        "due_date": r"Payment\s+Due\s+Date\s*:?\s*(?P<val>\d{2}-\w{3}-\d{2,4})",
        "statement_date": r"Statement\s+Date\s*:?\s*(?P<val>\d{2}-\w{3}-\d{2,4})",
        "credit_limit": r"Credit\s+Limit\s*:?\s*(?:Rs\.?)?\s*(?P<val>[\d,]+)",
        "card_no": r"Card\s+Number\s*:?\s*X{4}\s*X{4}\s*X{4}\s*(?P<val>\d{4})"
    },
    "ICICI": {
        "total_due": r"Total\s+Amount\s+Due\s*:?\s*(?:Rs\.?)?\s*(?P<val>[\d,]+\.\d{2})",
        "due_date": r"Payment\s+Due\s+Date\s*:?\s*(?P<val>\d{2}/\d{2}/\d{4})",
        "statement_date": r"Statement\s+Date\s*:?\s*(?P<val>\d{2}/\d{2}/\d{4})",
        "credit_limit": r"Credit\s+Limit\s*:?\s*(?:Rs\.?)?\s*(?P<val>[\d,]+)",
        "card_no": r"4\s*XXX\s*XXXX\s*XXXX\s*(?P<val>\d{4})"
    },
    "USBANK": {
        "total_due": r"New\s+Balance\s*\$?(?P<val>[\d,]+\.\d{2})",
        "due_date": r"Payment\s+Due\s+Date\s*(?P<val>\d{2}/\d{2}/\d{4})",
        "statement_date": r"Closing\s+Date:\s*(?P<val>\d{2}/\d{2}/\d{4})",
        "credit_limit": r"Credit\s+Line\s*\$?(?P<val>[\d,]+\.\d{2})",
        "card_no": r"Account\s+Ending\s+in\s*(?P<val>\d{4})" 
    },
    "WALMART": {
        "total_due": r"Account\s+Balance\s*\$?(?P<val>[\d,]+\.\d{2})",
        "due_date": r"Payment\s+Due\s+Date\(?s?\)?\s*(?P<val>\d{2}/\d{2}/\d{2})",
        "statement_date": r"Statement\s+Date\s*(?P<val>\d{2}/\d{2}/\d{2})",
        "credit_limit": r"Credit\s+Limit\s*\$?(?P<val>[\d,]+\.\d{2})",
        "card_no": r"Credit\s+Account\s+#\s*(?P<val>[\d\s]+)" 
    }
}

def extract_text_smart(pdf_path):
    text = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) > 0:
                text = pdf.pages[0].extract_text() or ""
    except Exception as e:
        print(f"pdfplumber failed: {e}")

    if len(text.strip()) < 50:
        print("⚠️ pdfplumber yielded low text. Switching to pypdf (better for generated files)...")
        try:
            reader = PdfReader(pdf_path)
            if len(reader.pages) > 0:
                text = reader.pages[0].extract_text() or ""
        except Exception as e:
            print(f"pypdf failed: {e}")


    if len(text.strip()) < 50:
        print("⚠️ Text still missing. File is likely an image. Starting OCR...")
        try:
            # Convert PDF Page to Image
            images = convert_from_path(pdf_path, first_page=1, last_page=1, poppler_path=POPPLER_PATH)
            if images:
                text = pytesseract.image_to_string(images[0])
                print("✅ OCR Complete.")
        except Exception as e:
            return f"OCR Failed. Check paths. Error: {e}"

    return text

# --- PARSING FUNCTIONS ---
def detect_bank(text):
    text = text.lower()
    if re.search(r"u\.?s\.?\s*bank", text): return "USBANK"
    if "walmart" in text: return "WALMART"
    if "hdfc bank" in text: return "HDFC"
    if "sbi card" in text or "state bank" in text: return "SBI"
    if "icici bank" in text: return "ICICI"
    return None

def extract_data(text, bank_name):
    data = {"Bank": bank_name}
    if bank_name not in BANK_PATTERNS: return data
    
    patterns = BANK_PATTERNS[bank_name]
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        data[field] = match.group("val") if match else "Not Found"
    return data

def save_to_db(data):
    conn = sqlite3.connect('statements.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS statements
                 (bank text, total_due text, due_date text, statement_date text, credit_limit text, card_no text)''')
    c.execute("INSERT INTO statements VALUES (:Bank, :total_due, :due_date, :statement_date, :credit_limit, :card_no)", data)
    conn.commit()
    conn.close()

def get_all_records():
    import pandas as pd
    conn = sqlite3.connect('statements.db')
    try:
        df = pd.read_sql_query("SELECT * FROM statements", conn)
        return df
    except:
        return pd.DataFrame()
    finally:
        conn.close()