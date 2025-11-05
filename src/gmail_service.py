from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import streamlit as st
import json
import os
from bs4 import BeautifulSoup
import base64
import tempfile
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TEMP_CRED_FILE = os.path.join(tempfile.gettempdir(), "gmail_creds.pkl")


def check_creds():
    creds = st.session_state.get("gmail_creds")
    if creds:
        return creds
    
     # Step 1: Check if stored credentials exist
    if os.path.exists(TEMP_CRED_FILE):
        with open(TEMP_CRED_FILE, "rb") as f:
            creds = pickle.load(f)
        st.session_state["gmail_creds"] = creds
        return creds


def authenticate_gmail():
    if "STREAMLIT_RUNTIME" in os.environ:
        authenticate_gmail_cloud()
    else:
        # Local environment -> use local server flow
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        st.session_state["gmail_creds"] = creds
        with open(TEMP_CRED_FILE, "wb") as f:
            pickle.dump(creds, f)
        return creds

def authenticate_gmail_cloud():
    credentials_json = st.secrets["gmail"]["credentials"]
    creds_dict = json.loads(credentials_json)
    redirect_uri = "https://ai-email-summarizer.streamlit.app/oauth2callback"

    # Initialize OAuth Flow
    flow = Flow.from_client_config(
        creds_dict,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

    # Step 3a: Show authorization link if no code yet
    query_params = st.experimental_get_query_params()
    if "code" not in query_params:
        auth_url, _ = flow.authorization_url(prompt="consent")
        st.markdown(f"[Authorize Gmail]({auth_url})")
        st.info("Click the link above to authorize Gmail. The new tab will redirect back automatically.")
        return None

    # Step 3b: Code received after redirect
    if "code" in query_params:
        code = query_params["code"][0]
        flow.fetch_token(code=code)
        creds = flow.credentials
        st.session_state["gmail_creds"] = creds
        # Persist credentials to temp file for session continuity
        with open(TEMP_CRED_FILE, "wb") as f:
            pickle.dump(creds, f)
        st.experimental_rerun()  # refresh app with credentials
        return creds

def get_emails(service, query: str, max_results=5):
    """
    Fetch emails from Gmail based on a query.
    Example queries:
      - "from:boss@company.com"
      - "subject:project update"
      - "from:manager@company.com subject:weekly"
    """
    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    messages = results.get('messages', [])

    email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        for part in msg_data['payload'].get('parts', []):
            if part['mimeType'] == 'text/html':
                data = part['body']['data']
                html = base64.urlsafe_b64decode(data).decode('utf-8')
                text = BeautifulSoup(html, 'html.parser').get_text()
                email_list.append(text)
    return email_list