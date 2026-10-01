import re

class ResumeCleaner:
    """
    Provides utility methods to clean and preprocess raw text from resumes.
    Removes web links, contact details, unnecessary punctuation, and formats whitespaces,
    while preserving symbols crucial for representing technical skills (like '+', '#', '.').
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans raw resume text to prepare it for NLP-based skill extraction.
        
        Args:
            text (str): Raw extracted text.
            
        Returns:
            str: Cleaned and normalized text.
        """
        if not text:
            return ""

        # Convert to lowercase for uniformity
        cleaned = text.lower()

        # Remove URLs (http/https and www links)
        cleaned = re.sub(r'https?://\S+|www\.\S+', ' ', cleaned)

        # Remove email addresses
        cleaned = re.sub(r'\S+@\S+', ' ', cleaned)

        # Remove phone numbers (matches various international and local formats)
        cleaned = re.sub(r'\+?\d[\d\-\(\)\s]{7,15}\d', ' ', cleaned)

        # Remove special characters but preserve '+', '#', '.' (crucial for C++, C#, .NET, Node.js)
        # We replace other punctuation marks and symbols with spaces
        cleaned = re.sub(r'[^a-zA-Z0-9\+\#\.\s]', ' ', cleaned)

        # Remove standalone single letters except 'c', 'r', 'g' (e.g., C, R, Go languages)
        cleaned = re.sub(r'\b[a-b|d-f|h-q|s-z]\b', ' ', cleaned)

        # Replace multiple consecutive spaces, tabs, or newlines with a single space
        cleaned = re.sub(r'\s+', ' ', cleaned)

        return cleaned.strip()
