import streamlit as st
import deepl
import os
from dotenv import load_dotenv
from PIL import Image
import msal
import requests
import logging
import time
import pyperclip

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set page config at the very beginning, removing the full-screen option
st.set_page_config(page_title="Rare Translator", page_icon="🌐", layout="centered", menu_items=None)

# Load environment variables
load_dotenv("configs/app.env")
auth_key = os.getenv("DEEPL_API_KEY")

# SSO Configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")

# Check if SSO configuration is complete
sso_config_complete = all([CLIENT_ID, CLIENT_SECRET, TENANT_ID])

if sso_config_complete:
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPE = ["User.Read"]
    REDIRECT_PATH = "/"

    # Initialize MSAL client
    try:
        msal_client = msal.ConfidentialClientApplication(
            CLIENT_ID, authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )
    except Exception as e:
        st.error(f"Error initializing MSAL client: {str(e)}")
        sso_config_complete = False
else:
    st.error("SSO configuration is incomplete. Please check your environment variables.")

# Initialize DeepL translator
if auth_key:
    try:
        translator = deepl.Translator(auth_key=auth_key)
    except Exception as e:
        st.error(f"Error initializing DeepL translator: {str(e)}")
else:
    st.error("DeepL API key is missing. Please check your environment variables.")

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
    
def get_base_url():
    # Check if we're running locally
    if os.getenv('DEVELOPMENT') == 'true':
        return "http://localhost:8501"
    return "https://translate.rare.org"

def login():
    if sso_config_complete:
        base_url = get_base_url()
        auth_url = msal_client.get_authorization_request_url(
            SCOPE,
            redirect_uri=f"{base_url}{REDIRECT_PATH}"
        )
        st.markdown(f'<a href="{auth_url}" target="_self">Login with Microsoft</a>', unsafe_allow_html=True)
    else:
        st.error("SSO is not configured correctly. Please contact the administrator.")

def callback():
    logging.info("Callback function called")
    
    if not sso_config_complete:
        logging.error("SSO configuration is incomplete")
        st.error("SSO is not configured correctly. Please contact the administrator.")
        return

    # Check if we already have a valid token
    if "token" in st.session_state:
        logging.info("Token already exists in session, redirecting to main page")
        st.query_params.clear()
        st.rerun()
        return

    # Check for authorization code
    if "code" not in st.query_params:
        logging.warning("No 'code' found in query parameters")
        st.error("Authentication failed: No authorization code received")
        return

    code = st.query_params["code"]
    
    # Prevent code reuse by storing used codes
    if "used_codes" not in st.session_state:
        st.session_state.used_codes = set()

    if code in st.session_state.used_codes:
        logging.warning("Authorization code has already been used")
        st.error("Session expired. Please log in again.")
        st.query_params.clear()
        time.sleep(2)
        st.rerun()
        return

    # Add code to used codes set
    st.session_state.used_codes.add(code)

    try:
        logging.info(f"Attempting to acquire token with authorization code: {code[:10]}...")
        base_url = get_base_url()
        result = msal_client.acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,
            redirect_uri=f"{base_url}{REDIRECT_PATH}"
        )

        if "access_token" in result:
            st.session_state.token = result["access_token"]
            if "refresh_token" in result:
                st.session_state.refresh_token = result["refresh_token"]
            logging.info("Access token acquired successfully")
            st.success("Login successful! Redirecting to main page...")
            st.query_params.clear()
            time.sleep(1)
            st.rerun()
        else:
            error_desc = result.get("error_description", "No error description available")
            logging.error(f"Failed to acquire token. Result: {result}")
            
            if "AADSTS54005" in error_desc:
                st.error("Session expired. Please log in again.")
                st.session_state.clear()
            else:
                st.error("Authentication failed: Unable to acquire token")
                st.write("Error details:", error_desc)
            
            st.query_params.clear()
            time.sleep(2)
            st.rerun()

    except Exception as e:
        logging.exception("Exception occurred during token acquisition")
        st.error(f"Authentication failed: {str(e)}")
        st.session_state.clear()
        st.query_params.clear()
        time.sleep(2)
        st.rerun()

# Add this helper function to refresh the token when needed
def refresh_access_token():
    if "refresh_token" not in st.session_state:
        return False

    try:
        result = msal_client.acquire_token_by_refresh_token(
            st.session_state.refresh_token,
            scopes=SCOPE
        )
        
        if "access_token" in result:
            st.session_state.token = result["access_token"]
            if "refresh_token" in result:
                st.session_state.refresh_token = result["refresh_token"]
            return True
    except Exception as e:
        logging.exception("Failed to refresh token")
        return False

    return False

def check_development():
    dev_mode = os.getenv('DEVELOPMENT')
    print(f"Development mode: {dev_mode}")
    return dev_mode == 'true'

def is_development():
    return check_development()

def get_user_info():
    # Bypass authentication in development mode
    if is_development():
        return {
            "displayName": "Development User",
            "userPrincipalName": "dev@localhost"
        }
    
    # Original authentication logic for production
    if sso_config_complete and "token" in st.session_state:
        headers = {'Authorization': f'Bearer {st.session_state.token}'}
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        
        if response.status_code == 401:  # Token expired
            if refresh_access_token():
                # Retry with new token
                headers = {'Authorization': f'Bearer {st.session_state.token}'}
                response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        
        if response.status_code == 200:
            return response.json()
    return None

def home():
    st.subheader("Key Features", divider=True)
    st.write("🗂️ **Document Translation**: Translate various file formats with ease.")
    st.write("📃 **Text Translation**: Quick and accurate text snippet translations.")

    st.subheader("How to Use")
    st.write("1. Choose your service from the tabs above.\n2. Select your target language.\n3. Upload a document or input your text.\n4. Click translate and watch the magic happen!")

def document_translator():
    st.subheader("Document Translator", divider=True)
    st.write("Upload your file and select the target language for translation.")
    st.subheader("Supported Formats")
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

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_size_mb = uploaded_file.size / (1024 * 1024)  # Convert to MB
            if file_size_mb > 20:  # Warning for files larger than 20MB
                st.warning(f"Large file detected ({file_size_mb:.1f}MB). Files with large images might need optimization for best results.", icon="⚠️")
            if st.button(f"Translate {uploaded_file.name}", key=f"translate_{uploaded_file.name}"):
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Create temp directory if it doesn't exist
                    temp_dir = "./temp_files"
                    output_dir = "./output_files"
                    for directory in [temp_dir, output_dir]:
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                    # Save uploaded file in smaller chunks with progress tracking
                    input_path = os.path.join(temp_dir, uploaded_file.name)
                    file_size = uploaded_file.size
                    CHUNK_SIZE = 512 * 1024  # 512KB chunks for more granular progress
                    
                    status_text.text("Preparing file for translation...")
                    progress_bar.progress(0)
                    
                    bytes_written = 0
                    with open(input_path, "wb") as f:
                        while True:
                            chunk = uploaded_file.read(CHUNK_SIZE)
                            if not chunk:
                                break
                            f.write(chunk)
                            bytes_written += len(chunk)
                            progress = min(bytes_written / file_size, 1.0)
                            progress_bar.progress(progress)

                    status_text.text("Translating document...")
                    progress_bar.progress(0.5)  # Show translation is in progress
                    
                    output_path = os.path.join(output_dir, f"{selected_language}_{uploaded_file.name}")

                    # Create a new translator instance for this specific translation
                    # This ensures a fresh connection for each translation
                    local_translator = deepl.Translator(auth_key=auth_key)
                    
                    # Translate document
                    local_translator.translate_document_from_filepath(
                        input_path=input_path,
                        output_path=output_path,
                        target_lang=target_language
                    )

                    progress_bar.progress(1.0)
                    status_text.text("Translation complete! Preparing download...")

                    # Stream the file download in chunks
                    with open(output_path, "rb") as file:
                        file_data = file.read()
                        st.download_button(
                            label=f"Download Translated File",
                            data=file_data,
                            file_name=f"{target_language}_{uploaded_file.name}",
                            mime='application/octet-stream',
                            key=f"download_{uploaded_file.name}"
                        )

                    status_text.empty()
                    progress_bar.empty()
                    st.success("Translation Complete! 🎉")

                except Exception as e:
                    st.error(f"Translation Error: {str(e)}")
                    logging.error(f"Translation failed for {uploaded_file.name}: {str(e)}", exc_info=True)
                    # Add more detailed error information
                    if isinstance(e, deepl.exceptions.ConnectionException):
                        st.error("Connection issue detected. This might be due to the file size or complexity. Try:")
                        st.markdown("""
                        1. Reducing image sizes in the document
                        2. Splitting the document into smaller parts
                        3. Converting images to a more compressed format
                        """)

                finally:
                    # Clean up temporary files
                    try:
                        if os.path.exists(input_path):
                            os.remove(input_path)
                        if os.path.exists(output_path):
                            os.remove(output_path)
                    except Exception as e:
                        logging.error(f"Error cleaning up temporary files: {str(e)}")

def text_translator():
    st.subheader("Text Translator", divider=True)
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
            
            # Inject the JavaScript and HTML together with matching styles
            st.components.v1.html(
                f"""
                <div style="padding-right: 15px; margin-left:-6px;">
                    <textarea id="translatedText" 
                             style="width: 100%; 
                                    height: 200px; 
                                    margin-bottom: 10px; 
                                    padding: 10px;
                                    border-radius: 0.5rem;
                                    background-color: #262730;
                                    border: 1px solid #262730;
                                    color: white;
                                    font-family: 'Source Sans Pro', sans-serif;
                                    font-size: 1rem;
                                    font-weight: 400;
                                    line-height: 1.5;" 
                             readonly>{text_result.text}</textarea>
                    <button onclick="copyText()" 
                            onmouseover="this.style.backgroundColor='#1d2330'; this.style.borderColor='#4f535e'"
                            onmouseout="this.style.backgroundColor='#131720'; this.style.borderColor='#41444C'"
                            style="padding: 0.5rem 1rem; 
                                   cursor: pointer; 
                                   background-color: #131720;
                                   border: 1px solid #41444C;
                                   border-radius: 0.5rem;
                                   color: white;
                                   font-family: 'Source Sans Pro', sans-serif;
                                   font-size: 1rem;
                                   font-weight: 400;
                                   line-height: 1.5;
                                   margin: 0px;
                                   user-select: none;
                                   background-clip: padding-box;
                                   transition: all 0.2s ease;">
                        Copy Text
                    </button>
                </div>

                <script>
                    function copyText() {{
                        var copyText = document.getElementById("translatedText");
                        copyText.select();
                        document.execCommand("copy");
                    }}
                </script>
                """,
                height=300
            )

        except Exception as e:
            st.error(f"Translation Error: {str(e)}")

def main():
    add_custom_css()

    # Skip authentication flow in development mode
    if is_development():
        user_info = get_user_info()  # Will return the development user
    else:
        # Check for callback
        if "code" in st.query_params:
            callback()
        # Check authentication status
        user_info = get_user_info()

    # Rest of the main function remains the same
    if is_development() or (sso_config_complete and user_info):
        # User is authenticated or in development mode, show the main application
        # Add the logo
        logo_path = "images/logo.png"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            aspect_ratio = logo.width / logo.height
            new_width = int(75 * aspect_ratio)
            
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            st.image(logo, width=new_width, use_column_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Logo file not found at {logo_path}")

        # Create a container for the header
        st.markdown('<div class="header-container">', unsafe_allow_html=True)
        
        # Create tabs
        tabs = st.tabs(["🏠 HOME", "🗂️ DOCUMENTS", "📃 TEXT"])
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Content based on selected tab
        with tabs[0]:
            home()
        with tabs[1]:
            document_translator()
        with tabs[2]:
            text_translator()
        
        # Only show logout button in production
        if not is_development():
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("Logout", key="logout_button", help="Click to log out"):
                st.session_state.clear()
                st.experimental_rerun()
    else:
        # User is not authenticated in production, show login page
        st.title("Welcome to Rare Translator")
        st.write("Please log in to access the application.")
        login()

# Add this outside the main() function
css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.2rem;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

if __name__ == "__main__":
    main()