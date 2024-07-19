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
import traceback
import logging

load_dotenv()
auth_key = os.getenv("DEEPL_API_KEY")

translator = deepl.Translator(auth_key=auth_key)

st.image("images\\4729_Brand_USA - HQ_Rare_RGB_Digital_Use.jpg", width=50)
st.header("The Translator")

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

text_column, doc_column = st.columns(2)
open_text_translation = text_column.button('Translate Text', type='primary', key='open text translator')
open_doc_translation = doc_column.button(label="Translate Document", type='secondary', key='open document translator')

# Text Translation
if open_text_translation:
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
        traceback.print_exc()

# Document Translation
else:
    st.subheader("Translate Documents")
    st.write("Ensure that your target language is different from the language of your document!")
    # The API also supports .docx, .pptx, .xlsx, .txt, PDF, and HTML files.
    uploaded_files = st.file_uploader("Choose Files to Translate", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        doc_translate = st.button(f"Translate {uploaded_file.name}", key=f"{uploaded_file}_Begin Translation")
        if doc_translate:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                # if directory exists:
                    # define output_path
                # else:
                    # mkdir and define path
                output_path = f"files\\{selected_language}_{uploaded_file.name}"

                # translation
                translation_status = st.empty()
                translation_status.text("Translation in Progress....")

                translator.translate_document_from_filepath(input_path=uploaded_file.name,
                                            output_path=output_path,
                                            target_lang=target_language)
                translation_status.empty()
                st.success("Translation successful! Download your translated file below...", icon='✅')
                time.sleep(2)
                translation_status.empty()
                with open(output_path, "rb") as file:
                    button = st.download_button(
                        label=f"Download {target_language}_{uploaded_file.name}",
                        data=file,
                        file_name=output_path,
                        mime='application/octet-stream'
                    )

                if button:
                    os.remove(output_path)
            except Exception as e:
                st.error(f'The translation could not be completed. We encountered an error: \n{e}', icon="🚨")
                traceback.print_exc()
            finally:
                os.remove(uploaded_file.name)


st.divider()

disclaimer = st.empty()
disclaimer = st.text("For internal use only!")