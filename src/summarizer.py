# summarizer.py
from transformers import pipeline

# Load summarization model (only once)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_email(email_text: str) -> str:
    """
    Summarize the given email text using a local Hugging Face model.
    """
    if not email_text or len(email_text.strip()) == 0:
        return "No content to summarize."

    # Truncate to avoid model input limit (BART limit ≈ 1024 tokens)
    email_text = email_text[:4000]

    # Run summarization
    summary = summarizer(
        email_text,
        max_length=130,
        min_length=30,
        do_sample=False
    )

    return summary[0]['summary_text']
