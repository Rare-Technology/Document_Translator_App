import streamlit as st
import deepl
import os
from dotenv import load_dotenv
from PIL import Image

# Set page config at the very beginning, removing the full-screen option
st.set_page_config(page_title="Rare Translator", page_icon="🌐", layout="wide", menu_items=None)

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

def add_custom_css():
    st.markdown("""
    <style>
    /* Adjust overall layout */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0.25rem 2rem;
    }
    
    /* Target the tab container */
    [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {
        background-color: transparent;
        padding: 0;
        margin-top: -1rem;
    }

    /* Remove all default borders and outlines */
    [data-baseweb="tab"], [data-baseweb="tab-list"], [data-baseweb="tab-highlight"] {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* Target each tab button */
    [data-baseweb="tab-list"] button[role="tab"] {
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 5px 15px !important;
        margin: 0 3px !important;
        border-radius: 10px 10px 0 0 !important;
        background-color: rgba(0, 0, 0, 0.05) !important;
        color: #999 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        box-shadow: none !important;
        position: relative !important;
    }

    /* Style for the active tab */
    [data-baseweb="tab-list"] button[role="tab"][aria-selected="true"]::after {
        content: '' !important;
        position: absolute !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 3px !important;
        background-color: #008542 !important;
    }

    [data-baseweb="tab-list"] button[role="tab"][aria-selected="true"] {
        background-color: rgba(0, 133, 66, 0.1) !important;
        color: #008542 !important;
    }

    /* Hover effect for tabs */
    [data-baseweb="tab-list"] button[role="tab"]:hover {
        background-color: rgba(0, 0, 0, 0.1) !important;
        color: #008542 !important;
    }

    /* Adjust the content area of the tabs */
    [data-baseweb="tab-panel"] {
        background-color: transparent;
        padding: 15px 0;
        border-radius: 0 0 10px 10px;
    }

    /* Force removal of any residual borders or lines */
    [data-baseweb="tab-list"]::after,
    [data-baseweb="tab-highlight"],
    [data-baseweb="tab-border"] {
        display: none !important;
        border: none !important;
        height: 0 !important;
    }

    /* Updated styles for the logo */
    .logo-container {
        position: absolute;
        top: 0.25rem;
        left: 1rem;
        z-index: 1000;
    }
    .logo-container img {
        height: 75px;
        width: auto;
    }
    
    /* Adjust header styles */
    h1 {
        font-size: 1.8rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        font-size: 1.4rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Custom style for the header container */
    .header-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 0.5rem;
        padding-top: 0.5rem;
    }
    
    /* Adjust the main content area */
    .main-content {
        margin-top: 0.5rem;
    }

    /* Remove full-screen option for images */
    button[title="View fullscreen"] {
        display: none !important;
    }

    /* Remove link icons from headers */
    .header-anchor {
        display: none !important;
    }

    h1:hover .header-anchor,
    h2:hover .header-anchor,
    h3:hover .header-anchor,
    h4:hover .header-anchor,
    h5:hover .header-anchor,
    h6:hover .header-anchor {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def home():
    st.header("Key Features:", divider=True)
    st.write("🗂️ **Document Translation**: Translate various file formats with ease.")
    st.write("💬 **Text Translation**: Quick and accurate text snippet translations.")

    st.header("How to Use:")
    st.write("1. Choose your service from the tabs above.")
    st.write("2. Select your target language.")
    st.write("3. Upload a document or input your text.")
    st.write("4. Click translate and watch the magic happen!")

def document_translator():
    st.header("Document Translator", divider=True)
    st.write("Upload your file and select the target language for translation.")
    st.warning("Ensure your target language differs from the source language for accurate results.", icon="⚠️")

    selected_language = st.selectbox(
        "Target Language:",
        list(LANGUAGE_MAP.keys()),
        index=0,
        key="document_target_language"
    )
    target_language = LANGUAGE_MAP[selected_language]

    uploaded_files = st.file_uploader(
        "Choose Files",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'pptx', 'txt'],
        key="document_file_uploader"
    )

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
        font-size: 20px;
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
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if st.button(f"Translate {uploaded_file.name}", key=f"translate_{uploaded_file.name}"):
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
                            mime='application/octet-stream',
                            key=f"download_{uploaded_file.name}"
                        )
                except Exception as e:
                    st.error(f"Translation Error: {str(e)}")
                finally:
                    if os.path.exists(uploaded_file.name):
                        os.remove(uploaded_file.name)
                    if os.path.exists(output_path):
                        os.remove(output_path)

def text_translator():
    st.header("Text Translator", divider=True)
    st.write("Enter your text and select the target language for translation.")
    st.warning("Ensure your target language differs from the source language for accurate results.", icon="⚠️")

    selected_language = st.selectbox(
        "Target Language:",
        list(LANGUAGE_MAP.keys()),
        index=0,
        key="text_target_language"
    )
    target_language = LANGUAGE_MAP[selected_language]

    text = st.text_area(
        "Enter Text",
        value="",
        height=200,
        placeholder="Type or paste your text here...",
        key="text_input"
    )
    translate_button = st.button("Translate", key="begin_text_translation")

    if translate_button and text:
        try:
            with st.spinner(f"Translating to {selected_language}..."):
                text_result = translator.translate_text(text=text, target_lang=target_language)

            st.success("Translation Complete! 🎉")
            st.subheader("Translated Text:")
            st.text_area(
                "",
                value=text_result.text,
                height=200,
                disabled=True,
                key="translated_text"
            )

            if st.button("Copy to Clipboard", key="copy_to_clipboard"):
                st.write("Text copied to clipboard!")
                st.markdown(
                    f"<script>navigator.clipboard.writeText(`{text_result.text}`)</script>",
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"Translation Error: {str(e)}")

def main():
    add_custom_css()

    # Add the logo
    logo_path = "images/logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        # Calculate width to maintain aspect ratio with 75px height
        aspect_ratio = logo.width / logo.height
        new_width = int(75 * aspect_ratio)
        
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image(logo, width=new_width, use_column_width=False)  # Disable full-screen option
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning(f"Logo file not found at {logo_path}")

    # Create a container for the header
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    
    # Create tabs
    tabs = st.tabs(["🏠HOME", "🗂️ DOCUMENT TRANSLATION", "💬 TEXT TRANSLATION"])
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Content based on selected tab
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    with tabs[0]:
        home()
    with tabs[1]:
        document_translator()
    with tabs[2]:
        text_translator()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()