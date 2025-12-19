import streamlit as st
import backend
import os

st.set_page_config(page_title="Statement Parser", page_icon="💳", layout="wide")
st.title("💳 Smart Credit Card Parser (OCR Enabled)")

st.sidebar.header("Database Records")
if st.sidebar.button("Refresh History"):
    df = backend.get_all_records()
    if not df.empty:
        st.sidebar.dataframe(df)
    else:
        st.sidebar.write("No records yet.")

uploaded_file = st.file_uploader("Upload PDF Statement", type="pdf")

if uploaded_file is not None:
    temp_path = "temp_statement.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner('Processing... (If scanned, OCR may take 10s)'):
        text = backend.extract_text_smart(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)

        with st.expander("Debug: View Extracted Text"):
            st.text(text)

        bank = backend.detect_bank(text)
        
        if bank:
            st.success(f"✅ Detected Bank: **{bank}**")
            data = backend.extract_data(text, bank)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Due", data.get('total_due', 'N/A'))
            c2.metric("Due Date", data.get('due_date', 'N/A'))
            c3.metric("Limit", data.get('credit_limit', 'N/A'))
            
            st.json(data)
            
            if st.button("Save to Database"):
                backend.save_to_db(data)
                st.toast("Saved successfully!", icon="💾")
        else:
            if "OCR Failed" in text:
                st.error(text) 
            else:
                st.error("❌ Bank not recognized. Ensure the logo/name is clear.")