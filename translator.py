import streamlit as st

st.image("images/4729_Brand_USA - HQ_Rare_RGB_Digital_Use.jpg", width=75)

# Home page - layout of all instructions for the document and text translation
def home():
    st.sidebar.success("Select the translation service above.")

    st.title("Rare's Translator")

    st.markdown(
        """
        The Translator is a Rare service for translating documents or text from one 
        language to another.

        It contains options for translating standalone text or documents into your desired language.

        The sidebar contains options for selecting the required service for translating text or documents.
        """
    )

# Document Translation
def document_translator():
    from datetime import date, timedelta
    import deepl
    import time
    import os
    from dotenv import load_dotenv
    import traceback
    import logging

    load_dotenv("configs/app.env")
    auth_key = os.getenv("DEEPL_API_KEY")

    translator = deepl.Translator(auth_key=auth_key)
    st.header("Document Translator")
    st.write("Ensure that your target language is not same as the language of your document!")

    selected_language = st.selectbox("Select Target Language:",
                       ("English (American)", "English (British)", 
                        "Japanese", "German", "French", "Portugese (Brazilian)", 
                        "Portugese (Except Brazilian)", "Spanish", "Finnish",
                        "Indonesian", "Italian", "Latvian", "Dutch", "Polish",
                        "Russian", "Slovenian", "Swedish", "Turkish", "Chinese (simplified)",
                        "Chinese (traditional)"), index=0)

    map = {
        "English (American)": "EN-US",
        "French": "FR",
        "English (British)": "EN-GB",
        "Japanese": "JA",
        "German": "DE",
        "Portugese (Except Brazilian)": "PT-PT",
        "Portugese (Brazilian)": "PT-BR",
        "Spanish": "ES",
        "Finnish": "FI",
        "Indonesian": "ID",
        "Italian": "IT",
        "Latvian": "LV",
        "Dutch": "NL",
        "Polish": "PL",
        "Russian": "RU",
        "Slovenian": "SL",
        "Swedish": "SV",
        "Turkish": "TR",
        "Chinese (simplified)": "ZH-HANS",
        "Chinese (traditional)": "ZH-HANT"
    }

    target_language = map.get(selected_language)
    
    # The API also supports .docx, .pptx, .xlsx, .txt, PDF, and HTML files.
    uploaded_files = st.file_uploader("Choose Files to Translate (.pdf, .docx, .pptx, .txt files)", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        doc_translate = st.button(f"Translate {uploaded_file.name}", key=f"{uploaded_file}_Begin Translation")
        if doc_translate:
            with open(f"./{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            try:
                output_dir = "./output_files"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                output_path = f"./output_files/{selected_language}_{uploaded_file.name}"

                # translation
                translation_status = st.empty()
                translation_status.text("Translation in Progress....")

                translator.translate_document_from_filepath(input_path=f"./{uploaded_file.name}",
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
            except deepl.exceptions.DocumentTranslationException as doc_e:
                # st.write(type(doc_e))
                st.error(f"Error: {doc_e.args[0].split(':')[1]} \n\n Please choose a different target language from the one in your document. If the problem persists, try again.")
                # traceback.print_exc()
            except deepl.exceptions.DeepLException as g_e:
                st.error(f'Error in translating document: \n\n {g_e.args[0].split(":")[1]} \n\n Please ensure you have uploaded the supported document types: pdf, docx, pptx, or txt. \nIf the problem persists, try again.', icon="🚨")
            except Exception as e:
                st.error(f'Error in translating document: \n\n {e.args[0].split(":")[1]}', icon="🚨")
                # traceback.print_exc()
            finally:
                os.remove(uploaded_file.name)

# Text Translation
def text_translator():
    from datetime import date, timedelta
    import deepl
    import os
    from dotenv import load_dotenv
    import traceback
    import logging

    load_dotenv("configs/app.env")
    auth_key = os.getenv("DEEPL_API_KEY")

    translator = deepl.Translator(auth_key=auth_key)
    st.header("Text Translator")

    selected_language = st.selectbox("Select Target Language:",
                       ("English (American)", "English (British)", 
                        "Japanese", "German", "French", "Portugese (Brazilian)", 
                        "Portugese (Except Brazilian)", "Spanish", "Finnish",
                        "Indonesian", "Italian", "Latvian", "Dutch", "Polish",
                        "Russian", "Slovenian", "Swedish", "Turkish", "Chinese (simplified)",
                        "Chinese (traditional)"), index=0)

    map = {
        "English (American)": "EN-US",
        "French": "FR",
        "English (British)": "EN-GB",
        "Japanese": "JA",
        "German": "DE",
        "Portugese (Except Brazilian)": "PT-PT",
        "Portugese (Brazilian)": "PT-BR",
        "Spanish": "ES",
        "Finnish": "FI",
        "Indonesian": "ID",
        "Italian": "IT",
        "Latvian": "LV",
        "Dutch": "NL",
        "Polish": "PL",
        "Russian": "RU",
        "Slovenian": "SL",
        "Swedish": "SV",
        "Turkish": "TR",
        "Chinese (simplified)": "ZH-HANS",
        "Chinese (traditional)": "ZH-HANT"
    }

    target_language = map.get(selected_language)

    st.subheader("Enter Text for Translation:")

    try:
        text = st.text_area("Enter Text for translation to your target language and Click 'Translate text' button", value="")
        text_translate = st.button("Translate text", key="Begin Text Translation")
        if text_translate:
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

page_names_to_funcs = {
    "HomePage": home,
    "Document Translation": document_translator,
    "Text Translation": text_translator
}

demo_name = st.sidebar.selectbox("Choose a Service", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()