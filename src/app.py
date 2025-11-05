import streamlit as st
from gmail_service import get_emails, authenticate_gmail
from googleapiclient.discovery import build
from summarizer import summarize_email
import streamlit.components.v1 as components


def get_email_service(creds):
    service = build('gmail', 'v1', credentials=creds)
    query = "from:bmathramkote@stratfordschools.com"
    emails = get_emails(service, query, max_results=5)
    st.success("Emails fetched successfully!")
    for idx, email in enumerate(emails, 1):
        exp = st.expander(f"Email #{idx}", expanded=False)
        with exp:
            st.text_area("Raw Email", email, height=200)
            summary = summarize_email(email)
            st.subheader("Summary:")
            st.write(summary)
            # Auto-scroll to this expander
            components.html(f"""
                <script>
                const exp = window.parent.document.querySelectorAll('section div[aria-expanded="true"]')[{idx-1}];
                if(exp) exp.scrollIntoView({{behavior: "smooth"}});
                </script>
            """, height=0)

st.set_page_config(page_title="AI Email Summarizer", page_icon="📩")

st.title("📩 AI Email Summarizer")
st.write("Fetch your Gmail messages by query and get concise summaries.")

creds = st.session_state.get("gmail_creds")
if creds:
    get_email_service(creds);
else:

    if st.button("Fetch and Summarize Emails"):
        with st.spinner("Fetching emails..."):
            creds = authenticate_gmail()
            get_email_service(creds);
            # Example: list last 5 email IDs
    



   



