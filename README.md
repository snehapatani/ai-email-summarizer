🧠 AI Email Summarizer

An intelligent tool that connects to Gmail and automatically summarizes lengthy emails using Hugging Face transformer models.
Designed for managers and professionals who want to stay on top of communication — without reading every email in full.

🚀 Features

✉️ Fetch emails securely from Gmail using the Gmail API

🤖 Summarize email text with Hugging Face transformer models

🔍 Filter emails by sender, subject, or date range

📋 Generate concise, context-aware summaries

💾 Store summaries locally or in a database

🔐 OAuth 2.0 authentication for secure Gmail access

🏗️ Architecture Overview
User ──> Gmail API ──> Email Fetcher ──> Hugging Face Model ──> Summary Output


Gmail API → Fetches emails and metadata

BeautifulSoup → Converts HTML emails to clean text

Hugging Face Transformers → Performs text summarization

Optional UI (Streamlit/Flask) → User-friendly dashboard

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/snehapatani/ai-email-summarizer.git
cd ai-email-summarizer

2️⃣ Create a Virtual Environment
python -m venv venv
venv\Scripts\activate      # Windows
# or
source venv/bin/activate   # macOS/Linux

4️⃣ Setup Gmail API Credentials

Go to Google Cloud Console

Create an OAuth 2.0 Client ID

Download the credentials.json file

Move it outside the project folder to protect it:

C:\Users\<you>\.config\ai-email-summarizer\credentials.json


Set an environment variable:

set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\<you>\.config\ai-email-summarizer\credentials.json

5️⃣ Run the Application
python app.py

🧩 Example Usage

Input:

Summarize unread emails from "hr@morganstanley.com
" this week.

Output:

“Two unread emails found. One confirms your meeting schedule; the other outlines updated HR policies.”

📁 Project Structure
ai-email-summarizer/
│
├── app.py                # Entry point
├── gmail_service.py       # Gmail API integration
├── summarizer.py          # Hugging Face summarization logic
├── README.md              # Project documentation
└── .gitignore             # Excluded sensitive files

🔐 Security & Privacy

Credentials and tokens are excluded via .gitignore

Uses OAuth 2.0 for secure Gmail authentication

Sensitive data is never logged or stored in Git

🧠 Tech Stack

Python 3.x

Hugging Face Transformers

Google Gmail API

BeautifulSoup4

Streamlit (optional UI)

💡 Future Enhancements

🧾 Summarize attachments and meeting invites

🗓️ Daily digest view

📊 Streamlit dashboard for summary history

🔉 Voice summary playback

👩‍💻 Author

Sneha Shah
Software Engineering Manager | AI & Distributed Systems Enthusiast
LinkedIn
 • GitHub