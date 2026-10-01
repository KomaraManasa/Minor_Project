import os
import joblib
import re
import logging
from verification.trainer import ModelTrainer

# Configure logger
logger = logging.getLogger(__name__)

class JobVerifier:
    """
    Handles classification and explainability for job descriptions.
    Loads TF-IDF vectorizer and the best trained model to calculate 
    authenticity metrics, confidence scores, and reasons for prediction.
    """
    
    def __init__(self):
        """
        Initializes pathways and loads saved classification artifacts.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.model_dir = os.path.join(project_root, "models")
        
        self.vectorizer_path = os.path.join(self.model_dir, "tfidf_vectorizer.joblib")
        self.model_path = os.path.join(self.model_dir, "best_job_verifier.joblib")
        
        self.vectorizer = None
        self.model = None
        self._load_artifacts()

    def _load_artifacts(self):
        """
        Loads classification pipeline artifacts. If files do not exist,
        triggers the ModelTrainer script to run training automatically.
        """
        if not os.path.exists(self.vectorizer_path) or not os.path.exists(self.model_path):
            logger.info("Model artifacts not found. Launching auto-training handler...")
            trainer = ModelTrainer()
            trainer.train_and_evaluate()
            
        try:
            self.vectorizer = joblib.load(self.vectorizer_path)
            self.model = joblib.load(self.model_path)
            logger.info("ML verification artifacts loaded successfully.")
        except Exception as e:
            logger.error(f"Error during model loading: {e}")
            raise RuntimeError("Model loading failed.") from e

    def _clean_text(self, text: str) -> str:
        """
        Cleans input text in the same format as the training script.
        """
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def verify(self, job_description: str) -> dict:
        """
        Verifies the authenticity of a job description.
        
        Args:
            job_description (str): Full text of the job description.
            
        Returns:
            dict: Contains 'label' (Authentic/Suspicious), 'confidence' (float),
                  and 'reasons' (list of strings).
        """
        if not job_description or len(job_description.strip()) < 20:
            return {
                "label": "Suspicious",
                "confidence": 100.0,
                "reasons": [
                    "The provided job description is extremely short or empty. "
                    "Legitimate corporate postings contain clear, structured paragraphs "
                    "detailing job requirements, responsibilities, and benefits."
                ]
            }

        # Clean description text
        cleaned = self._clean_text(job_description)
        
        # Transform text to vector space
        features = self.vectorizer.transform([cleaned])
        
        # Run classification and probability estimation
        prediction = self.model.predict(features)[0]  # 0 = Authentic, 1 = Suspicious
        probabilities = self.model.predict_proba(features)[0]
        
        confidence = probabilities[prediction] * 100.0
        label = "Suspicious" if prediction == 1 else "Authentic"
        
        # Generate explanations for classification decision
        reasons = self._explain_prediction(label, job_description)
        
        return {
            "label": label,
            "confidence": round(confidence, 2),
            "reasons": reasons
        }

    def _explain_prediction(self, label: str, text: str) -> list:
        """
        Performs analysis on text tokens to explain why the model made a decision.
        
        Args:
            label (str): Classification result label.
            text (str): Input job description.
            
        Returns:
            list: List of human-readable reason strings.
        """
        text_lower = text.lower()
        reasons = []
        
        if label == "Suspicious":
            # Map regex checks to explanation cards
            indicators = {
                r"\b(telegram|whatsapp|line|signal|skype)\b": 
                    "Recruitment processes conducted via messaging apps (Telegram, WhatsApp) "
                    "rather than enterprise domains are high-risk indicators.",
                
                r"\b(wire|bank account|checking account|routing|crypto|bitcoin|paypal|western union)\b": 
                    "Mentions transferring money or requesting candidate financial details. "
                    "Legitimate employers do not ask you to process checks, open accounts, or buy crypto.",
                
                r"\b(earn \$?\d+ (daily|weekly|hourly|per day|per week|per hour))\b": 
                    "Promises disproportionately high salaries relative to general requirements.",
                
                r"\b(no experience|all candidates|no cv|no resume|instant start|no interview)\b": 
                    "Vague application process without credential checks or technical evaluations.",
                
                r"\b(gift card|cashier check|certified check|money order|deposit first)\b": 
                    "Mentions processing checks or purchasing gift cards, a common signature "
                    "for financial fraud or money laundering scams.",
                
                r"\b(work from home|work from anywhere|easy money|quick income)\b": 
                    "Heavy advertising of 'easy money' and 'flexible hours' which shifts focus "
                    "away from technical deliverables."
            }
            
            for pattern, reason in indicators.items():
                if re.search(pattern, text_lower):
                    reasons.append(reason)
                    
            if not reasons:
                reasons.append(
                    "The vocabulary and phrasing index strongly align with known "
                    "fraudulent patterns present in the Fake Job Posting dataset (e.g. low details combined with high perks)."
                )
        else:
            # Positive checks for legitimate job posts
            indicators = {
                r"\b(experience|years exp|qualification|degree|bachelor|master|b\.tech|mca)\b": 
                    "Mentions structured academic and professional experience requirements.",
                
                r"\b(responsibilities|duties|role responsibilities|key tasks)\b": 
                    "Defines clear daily deliverables, reports, or professional operations.",
                
                r"\b(skills|proficient|expert|knowledge of|experience with)\b": 
                    "Specifies detailed technical stack criteria or domain-specific competencies.",
                
                r"\b(equal opportunity|benefits|health insurance|medical|retirement|pf|leaves)\b": 
                    "References corporate employee compensation frameworks (provident funds, medical cover).",
                
                r"\b(collaboration|teamwork|collaborate|cross-functional)\b": 
                    "Highlights typical structural corporate team collaborations."
            }
            
            for pattern, reason in indicators.items():
                if re.search(pattern, text_lower):
                    reasons.append(reason)
                    
            if not reasons:
                reasons.append(
                    "Exhibits a professional corporate structure, grammatical consistency, "
                    "and focuses on specific software tools or business requirements."
                )
                
        return reasons
