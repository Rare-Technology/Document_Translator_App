import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import time
import deepl
from io import StringIO
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()
auth_key = os.getenv("DEEPL_API_KEY")

translator = deepl.Translator(auth_key=auth_key)

st.header("Translate to your target Language")

selected_language = st.selectbox("Select Target Language:",
                       ("English (American)", "English (British)", "Japanese", "German", "French", "Portugese (Brazilian)", "Portugese (Except Brazilian)"), index=0)

map = {
    "English (American)": "EN-US",
    "French": "FR",
    "English (British)": "EN-GB",
    "Japanese": "JA",
    "German": "DE",
    "Portugese (Except Brazilian)": "PT-PT",
    "Portugese (Brazilian)": "PT-BR"
}

target_language = map.get(selected_language)

st.subheader("Enter Text for Translation:")

try:
    text = st.text_area("Enter Text for translation to your target language and hit 'Ctrl + Enter'", value="")
    text_result = translator.translate_text(text=text, target_lang=target_language)
    st.write(f"Translating input to {selected_language} ...")
    st.divider()
    st.text(text_result)
    st.divider()
except Exception as e:
    st.divider()
    st.write("Enter Text to translate")
    st.divider()

st.subheader("Input file for Translation:")


# The API also supports .docx, .pptx, .xlsx, .txt, PDF, and HTML files.
uploaded_files = st.file_uploader("Choose Files to Translate", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        output_path = f"{selected_language}_{uploaded_file.name}"

        # translation
        start = time.perf_counter()
        translator.translate_document_from_filepath(input_path=uploaded_file.name,
                                    output_path=output_path,
                                    target_lang=target_language)

        stop = time.perf_counter()
        # with st.spinner("Translation in progress.."):
        #     time.sleep(stop - start)

        st.success("Translation successful! Download your translated file below.", icon='✅')
        with open(output_path, "rb") as file:
            button = st.download_button(
                label=f"Download {target_language}_{uploaded_file.name}",
                data=file,
                file_name=output_path,
                mime='application/octet-stream'
            )
        
        if button is not None:
            os.remove(output_path)
            os.remove(uploaded_file.name)

    except Exception as e:
        st.error(f'We encountered an error: {e}', icon="🚨")