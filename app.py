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
        text = extract_text_with_ocr(doc)

        for page in doc:
            import pytesseract
import cv2
import numpy as np
from PIL import Image

def extract_text_with_ocr(doc):
    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Convert PDF page to image
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Convert to OpenCV format
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Improve image for OCR
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # OCR
        text = pytesseract.image_to_string(thresh)
        full_text += text

    return full_text
``

        # Dimension patterns
        patterns = [
            
r"R\d+\.?\d*",      # Radius
    r"\d+°",            # Angle
    r"\d+\.?\d*"        # Linear values

        ]

        dimensions = []
        for p in patterns:
            dimensions += re.findall(p, text)

        dimensions = list(set(dimensions))

        df = pd.DataFrame({
            "
 "Balloon No": range(1, len(dimensions) + 1),
    "Dimension Type": [
        "Radius" if "R" in d else "Angle" if "°" in d else "Linear"
        for d in dimensions
    ],
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
