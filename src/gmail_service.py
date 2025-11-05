from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import streamlit as st
import json
import os
from bs4 import BeautifulSoup
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = st.session_state.get("gmail_creds")
    if creds:
        return creds

    if "STREAMLIT_RUNTIME" in os.environ:
        # Cloud environment -> use console flow
        credentials_json = st.secrets["gmail"]["credentials"]
        creds_dict = json.loads(credentials_json)
        st.info("Click the link below to authorize Gmail:")
        flow = InstalledAppFlow.from_client_config(creds_dict, SCOPES)
        auth_url, _ = flow.authorization_url(prompt="consent")
        st.markdown(f"[Authorize Gmail]({auth_url})")
        code = st.text_input("Enter the authorization code here:")
        if code:
            flow.fetch_token(code=code)
            creds = flow.credentials
            st.session_state["gmail_creds"] = creds
            return creds
    else:
        # Local environment -> use local server flow
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        st.session_state["gmail_creds"] = creds
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