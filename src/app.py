import streamlit as st
from gmail_service import authenticate_gmail, get_emails
from summarizer import summarize_email

st.set_page_config(page_title="AI Email Summarizer", page_icon="📩")

st.title("📩 AI Email Summarizer")
st.write("Fetch your Gmail messages by query and get concise summaries.")

if st.button("Fetch and Summarize Emails"):
    with st.spinner("Fetching emails..."):
        service = authenticate_gmail()
        query = "from:bmathramkote@stratfordschools.com"
        emails = get_emails(service, query, max_results=5)

    st.success("Emails fetched successfully!")


    for idx, email in enumerate(emails, 1):
        with st.expander(f"Email #{idx}"):
            st.text_area("Raw Email", email, height=200)
            summary = summarize_email(email)
            st.subheader("Summary:")
            st.write(summary)
