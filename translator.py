import streamlit as st
import deepl
import os
from dotenv import load_dotenv

# Set page config at the very beginning, removing the full-screen option
st.set_page_config(page_title="Rare's Translator", page_icon="🌐", layout="wide", menu_items=None)

# Load environment variables
load_dotenv("configs/app.env")
auth_key = os.getenv("DEEPL_API_KEY")

# Initialize DeepL translator
translator = deepl.Translator(auth_key=auth_key)

# Language mapping
LANGUAGE_MAP = {
    "English (American)": "EN-US",
    "English (British)": "EN-GB",
    "Japanese": "JA",
    "German": "DE",
    "French": "FR",
    "Portuguese (Brazilian)": "PT-BR",
    "Portuguese (Except Brazilian)": "PT-PT",
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

def home():
    st.image("images/4729_Brand_USA - HQ_Rare_RGB_Digital_Use.png", width=100)
    st.title("Rare's Translator")
    st.write("Welcome to the Rare Translator, a powerful tool for seamless language translation.")
    
    st.header("Key Features:")
    st.write("🗂️ **Document Translation**: Translate various file formats with ease.")
    st.write("💬 **Text Translation**: Quick and accurate text snippet translations.")
    
    st.header("How to Use:")
    st.write("1. Choose your service from the sidebar.")
    st.write("2. Select your target language.")
    st.write("3. Upload a document or input your text.")
    st.write("4. Click translate and watch the magic happen!")
    
    st.header("Supported Formats:")
    
    # Using official icons for supported formats with adjusted size
    st.markdown("""
    <style>
    .format-icon {
        height: 20px;
        width: 20px;
        margin-right: 5px;
        vertical-align: middle;
    }
    .format-text {
        font-size: 16px;
        vertical-align: middle;
    }
    </style>
    <div style="margin-bottom:20px;">
        <img src="https://img.icons8.com/color/48/000000/pdf.png" class="format-icon"/><span class="format-text">PDF</span>
        <img src="https://img.icons8.com/color/48/000000/word.png" class="format-icon"/><span class="format-text">DOCX</span>
        <img src="https://img.icons8.com/color/48/000000/powerpoint.png" class="format-icon"/><span class="format-text">PPTX</span>
        <img src="https://img.icons8.com/color/48/000000/txt.png" class="format-icon"/><span class="format-text">TXT</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("Ensure your target language differs from the source language for accurate results.")
    
    st.info("Need help? Contact our support team for assistance.")

def document_translator():
    st.title("Document Translator")
    st.write("Upload your file and select the target language for translation.")

    selected_language = st.selectbox("Target Language:", list(LANGUAGE_MAP.keys()), index=0)
    target_language = LANGUAGE_MAP[selected_language]
    
    uploaded_files = st.file_uploader("Choose Files", accept_multiple_files=True, type=['pdf', 'docx', 'pptx', 'txt'])
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if st.button(f"Translate {uploaded_file.name}", key=f"{uploaded_file}_Begin Translation"):
                try:
                    with st.spinner("Translation in Progress..."):
                        with open(f"./{uploaded_file.name}", "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        output_dir = "./output_files"
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                        
                        output_path = f"./output_files/{selected_language}_{uploaded_file.name}"
                        
                        translator.translate_document_from_filepath(
                            input_path=f"./{uploaded_file.name}",
                            output_path=output_path,
                            target_lang=target_language
                        )
                    
                    st.success("Translation Complete! 🎉")
                    
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label=f"Download Translated File",
                            data=file,
                            file_name=f"{target_language}_{uploaded_file.name}",
                            mime='application/octet-stream'
                        )
                except Exception as e:
                    st.error(f"Translation Error: {str(e)}")
                finally:
                    if os.path.exists(uploaded_file.name):
                        os.remove(uploaded_file.name)
                    if os.path.exists(output_path):
                        os.remove(output_path)

def text_translator():
    st.title("Text Translator")
    st.write("Enter your text and select the target language for translation.")

    selected_language = st.selectbox("Target Language:", list(LANGUAGE_MAP.keys()), index=0)
    target_language = LANGUAGE_MAP[selected_language]

    text = st.text_area("Enter Text", value="", height=200, placeholder="Type or paste your text here...")
    translate_button = st.button("Translate", key="Begin Text Translation")

    if translate_button and text:
        try:
            with st.spinner(f"Translating to {selected_language}..."):
                text_result = translator.translate_text(text=text, target_lang=target_language)
            
            st.success("Translation Complete! 🎉")
            st.subheader("Translated Text:")
            st.text_area("", value=text_result.text, height=200, disabled=True)
            
            if st.button("Copy to Clipboard"):
                st.write("Text copied to clipboard!")
                st.markdown(f"<script>navigator.clipboard.writeText('{text_result.text}')</script>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Translation Error: {str(e)}")

def main():
    st.sidebar.title("Navigation")
    page_names_to_funcs = {
        "Home": home,
        "Document Translation": document_translator,
        "Text Translation": text_translator
    }

    demo_name = st.sidebar.radio("Go to", list(page_names_to_funcs.keys()))
    page_names_to_funcs[demo_name]()

if __name__ == "__main__":
    main()