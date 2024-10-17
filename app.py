import streamlit as st
import msal
import requests

# Microsoft Azure AD configuration
CLIENT_ID = "16ce6010-9959-42c4-bade-1d2f74b2f8c3"
CLIENT_SECRET = "42f87780-e706-4461-9f2a-96328617a566"
TENANT_ID = "4a179129-a51e-44b8-bc59-03e6e3b6d51d"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]
REDIRECT_PATH = "/auth/callback"

# Initialize MSAL client
msal_client = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

def login():
    auth_url = msal_client.get_authorization_request_url(
        SCOPE,
        redirect_uri=f"https://translate.rare.org{REDIRECT_PATH}"
    )
    st.markdown(f'<a href="{auth_url}" target="_self">Login with Microsoft</a>', unsafe_allow_html=True)

def callback():
    if "code" in st.experimental_get_query_params():
        code = st.experimental_get_query_params()["code"][0]
        result = msal_client.acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,
            redirect_uri=f"https://translate.rare.org{REDIRECT_PATH}"
        )
        if "access_token" in result:
            st.session_state.token = result["access_token"]
            st.experimental_rerun()
        else:
            st.error("Authentication failed")

def get_user_info():
    if "token" in st.session_state:
        headers = {'Authorization': f'Bearer {st.session_state.token}'}
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        if response.status_code == 200:
            return response.json()
    return None

def main():
    st.set_page_config(page_title="Streamlit SSO App")

    if st.experimental_get_query_params().get("code"):
        callback()

    user_info = get_user_info()

    if user_info:
        st.write(f"Welcome, {user_info['displayName']}!")
        st.write("You are logged in.")
        if st.button("Logout"):
            st.session_state.clear()
            st.experimental_rerun()
    else:
        st.write("Please log in to access the application.")
        login()

if __name__ == "__main__":
    main()