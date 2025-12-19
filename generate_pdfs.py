from fpdf import FPDF
import random

def create_statement(bank_name, filename, data):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{bank_name} Credit Card Statement", ln=1, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 5, txt="Mr. John Doe", ln=1)
    pdf.cell(200, 5, txt="123, Tech Park, Bangalore, KA", ln=1)
    pdf.ln(10)
    
    pdf.set_font("Arial", size=11)
    
    if bank_name == "HDFC":
        # HDFC Layout
        pdf.cell(0, 8, txt=f"Statement Date: {data['statement_date']}", ln=1)
        pdf.cell(0, 8, txt=f"Payment Due Date: {data['due_date']}", ln=1)
        pdf.cell(0, 8, txt=f"Credit Limit: Rs. {data['limit']}", ln=1)
        pdf.cell(0, 8, txt=f"Total Dues: Rs. {data['total']}", ln=1)
        pdf.ln(5)
        pdf.cell(0, 8, txt=f"Card No. : XXXX XXXX XXXX {data['card_last4']}", ln=1)

    elif bank_name == "SBI":
        pdf.cell(0, 8, txt=f"Statement Date: {data['statement_date'].replace('/', '-')}", ln=1)
        pdf.cell(0, 8, txt=f"Payment Due Date: {data['due_date'].replace('/', '-')}", ln=1)
        pdf.cell(0, 8, txt=f"Credit Limit:  {data['limit']}", ln=1)
        pdf.cell(0, 8, txt=f"Total Amount Due: Rs. {data['total']}", ln=1)
        pdf.ln(5)
        pdf.cell(0, 8, txt=f"Card Number: XXXX XXXX XXXX {data['card_last4']}", ln=1)

    elif bank_name == "ICICI":
        pdf.cell(0, 8, txt=f"Statement Date: {data['statement_date']}", ln=1)
        pdf.cell(0, 8, txt=f"Payment Due Date: {data['due_date']}", ln=1)
        pdf.cell(0, 8, txt=f"Total Amount Due: Rs. {data['total']}", ln=1)
        pdf.cell(0, 8, txt=f"Credit Limit: Rs. {data['limit']}", ln=1)
        pdf.ln(5)
        pdf.cell(0, 8, txt=f"4XXX XXXX XXXX {data['card_last4']}", ln=1)

    elif bank_name == "AMEX":
        pdf.cell(0, 8, txt=f"Statement Date: {data['statement_date']}", ln=1)
        pdf.cell(0, 8, txt=f"Payment Due Date: {data['due_date']}", ln=1)
        pdf.cell(0, 8, txt=f"New Balance: Rs. {data['total']}", ln=1)
        pdf.cell(0, 8, txt=f"Credit Limit: Rs. {data['limit']}", ln=1)
        pdf.ln(5)
        pdf.cell(0, 8, txt=f"Account Ending 12345 {data['card_last4']}", ln=1) # 5 digits

    elif bank_name == "CITI":
        pdf.cell(0, 8, txt=f"Date of Statement: {data['statement_date']}", ln=1)
        pdf.cell(0, 8, txt=f"Payment Due Date: {data['due_date']}", ln=1)
        pdf.cell(0, 8, txt=f"Total Amount Due: Rs. {data['total']}", ln=1)
        pdf.cell(0, 8, txt=f"Credit Limit: Rs. {data['limit']}", ln=1)
        pdf.ln(5)
        pdf.cell(0, 8, txt=f"Card No. : XXXX XXXX XXXX {data['card_last4']}", ln=1)

    pdf.ln(20)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Transaction Details", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, txt="10/12/2024   Starbucks Coffee   Rs. 350.00", ln=1)
    pdf.cell(0, 8, txt="12/12/2024   Amazon Retail      Rs. 1,200.00", ln=1)
    
    pdf.output(filename)
    print(f"Generated: {filename}")

samples = [
    ("HDFC", "Statement_HDFC.pdf", {"total": "15,200.50", "due_date": "05/01/2025", "statement_date": "15/12/2024", "limit": "1,50,000", "card_last4": "1122"}),
    ("SBI", "Statement_SBI.pdf",  {"total": "8,450.00", "due_date": "10-Jan-2025", "statement_date": "20-Dec-2024", "limit": "75,000", "card_last4": "3344"}),
    ("ICICI", "Statement_ICICI.pdf", {"total": "22,100.00", "due_date": "02/01/2025", "statement_date": "12/12/2024", "limit": "2,00,000", "card_last4": "5566"}),
]

for name, fname, data in samples:
    create_statement(name, fname, data)