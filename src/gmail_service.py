from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import streamlit as st
import json
import pickle
import os.path
from bs4 import BeautifulSoup
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists("credentials.json"):
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                # Streamlit Cloud mode — load from secrets.toml
                credentials_json = st.secrets["gmail"]["credentials"]
                creds_dict = json.loads(credentials_json)
                # Use from_client_config instead of from_client_secrets_file
                flow = InstalledAppFlow.from_client_config(creds_dict, SCOPES)
                creds = flow.run_console()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service


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