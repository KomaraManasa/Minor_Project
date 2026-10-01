import PyPDF2
import io
import logging

# Configure logger
logger = logging.getLogger(__name__)

class ResumeParser:
    """
    Handles PDF reading and text extraction using the PyPDF2 library.
    Supports reading from both local file paths and in-memory byte streams 
    (such as Streamlit's UploadedFile object).
    """

    @staticmethod
    def extract_text(pdf_source) -> str:
        """
        Extracts raw text from a PDF file source.
        
        Args:
            pdf_source (str, bytes, or file-like object): Path to the PDF file, 
                        raw byte content, or a file-like byte stream.
            
        Returns:
            str: The concatenated raw text extracted from all pages of the PDF.
                 Returns an empty string if parsing fails.
        """
        extracted_text = []
        try:
            # If the PDF source is provided as raw bytes, wrap it in BytesIO
            if isinstance(pdf_source, bytes):
                pdf_file = io.BytesIO(pdf_source)
            else:
                pdf_file = pdf_source

            reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(reader.pages)
            logger.info(f"Initiating extraction on PDF source. Pages detected: {num_pages}")

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text)
            
            full_text = "\n".join(extracted_text)
            logger.info("PDF text extraction completed successfully.")
            return full_text.strip()

        except Exception as e:
            logger.error(f"Error encountered during PDF text extraction: {e}")
            return ""
