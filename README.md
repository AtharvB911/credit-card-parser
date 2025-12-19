# 💳 Credit Card Statement Parser

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red) ![OCR](https://img.shields.io/badge/OCR-Tesseract-green) ![Status](https://img.shields.io/badge/Status-Completed-success)

A robust financial document parser capable of extracting key data points from credit card statements. This solution features a **hybrid extraction engine** that handles both digital (native) PDFs and scanned (image-based) statements using OCR.

---

## 🚀 Key Features

* **Multi-Bank Support:** Parses statements from **5 Major Issuers**:
    * HDFC Bank (Native/Generated)
    * SBI Card (Native/Generated)
    * ICICI Bank (Native/Generated)
    * US Bank (Real-world Scanned Format)
    * Walmart / Capital One (Real-world Native Format)
* **Hybrid Parsing Engine:** Implements a 3-tier fallback logic:
    1.  **Level 1 (Layout Preserving):** `pdfplumber` for structured tables.
    2.  **Level 2 (Stream Extraction):** `pypdf` for raw data streams (handles generated PDFs).
    3.  **Level 3 (OCR):** `Tesseract` + `Poppler` for scanned images.
* **Data Persistence:** Automatically saves extracted records to a local **SQLite** database.
* **Interactive UI:** Built with **Streamlit** for easy drag-and-drop testing and history viewing.
* **Mock Data Generator:** Includes a script to generate legally safe "dummy" statements for demonstration.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.x | Core Logic |
| **Frontend** | Streamlit | User Interface |
| **Parsing** | `pdfplumber`, `pypdf` | Native Text Extraction |
| **OCR** | `pytesseract`, `pdf2image` | Image-to-Text Conversion |
| **Database** | SQLite3 | Local Storage |
| **Data Handling** | Pandas, Regex | Formatting & Pattern Matching |

---

## 📂 Project Structure

```text
credit-card-parser/
│
├── app.py                # Main Streamlit Application (Frontend)
├── backend.py            # Core Logic (Regex, OCR, Database)
├── generate_pdfs.py      # Script to create Mock PDFs for testing
├── requirements.txt      # Python dependencies
├── README.md             # Project Documentation
│
├── data/                 # Directory for storing sample PDFs
└── statements.db         # SQLite Database (Auto-generated)