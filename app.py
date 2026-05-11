import streamlit as st
import fitz
import re
import pandas as pd

st.set_page_config(page_title="AutoDim Inspector", layout="wide")

st.title("📏 Auto Dimension Extraction Tool")
st.write("Upload your 2D drawing PDF and generate inspection sheet instantly")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    if st.button("Extract Dimensions"):

        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""

        for page in doc:
            text += page.get_text()

        # Dimension patterns
        patterns = [
            r"Ø\d+\.?\d*",
            r"R\d+\.?\d*",
            r"\d+\.?\d*\s?±\d+\.?\d*",
            r"\d+\.\d+"
        ]

        dimensions = []
        for p in patterns:
            dimensions += re.findall(p, text)

        dimensions = list(set(dimensions))

        df = pd.DataFrame({
            "S.No": range(1, len(dimensions) + 1),
            "Specified Dimension": dimensions,
            "Actual Dimension": "",
            "Status": ""
        })

        st.success("✅ Dimensions extracted successfully")

        edited_df = st.data_editor(df, use_container_width=True)

        csv = edited_df.to_csv(index=False)

        st.download_button(
            "📥 Download Inspection Sheet",
            csv,
            "Inspection_Report.csv",
            "text/csv"
        )
