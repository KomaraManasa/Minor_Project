import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
import re

class ModelTrainer:
    """
    Handles data ingestion, text preprocessing, feature extraction (TF-IDF),
    training and evaluation of multiple Machine Learning models, and exports the 
    best model for job description verification.
    """
    
    def __init__(self, data_path=None, model_dir=None):
        """
        Initializes dataset path and output model artifact directories.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        self.data_path = data_path or os.path.join(project_root, "data", "fake_job_postings.csv")
        self.model_dir = model_dir or os.path.join(project_root, "models")
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.vectorizer_path = os.path.join(self.model_dir, "tfidf_vectorizer.joblib")
        self.model_path = os.path.join(self.model_dir, "best_job_verifier.joblib")
        self.stats_path = os.path.join(self.model_dir, "training_stats.json")

    def _clean_text(self, text: str) -> str:
        """
        Helper to clean text features by lowercasing and removing punctuation.
        """
        if not isinstance(text, str):
            return ""
        text = text.lower()
        # Remove digits and special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _generate_synthetic_data(self) -> pd.DataFrame:
        """
        Generates structured synthetic job descriptions to serve as fallback data 
        if the external Kaggle fake_job_postings.csv is missing.
        """
        print("Fake job posting dataset not found. Generating synthetic dataset...")
        
        # Real-sounding job postings
        authentic_descriptions = [
            "We are seeking a Backend Developer to join our core engineering group. You will build APIs, "
            "optimize relational databases, and collaborate closely with front-end engineers. "
            "Stack includes Python, Django, PostgreSQL, and Git. Requires a BS in Computer Science "
            "or related field with 2+ years of professional development experience.",
            
            "Looking for a front-end specialist with expertise in React.js, HTML5, CSS3, and ES6. "
            "Responsibilities: Constructing reusable components, designing layout flow, and optimizing "
            "web performance across viewports. Collaborative Git workflows. 3+ years experience.",
            
            "Cloud Engineer wanted immediately. Maintain cloud architecture on AWS (EC2, S3, RDS, Lambda). "
            "Automate resource creation using Terraform. Monitor logging metrics. Linux system administration "
            "and basic scripting skills are required. AWS certifications are highly preferred.",
            
            "Data Analyst opening. Clean, aggregate, and analyze data to extract business insights. "
            "Familiarity with SQL, Python (Pandas, Numpy), and visualizers (Tableau, Power BI). "
            "Good communications skills and basic statistics knowledge required. Full-time position.",
            
            "Project Coordinator to facilitate development sprints, track timeline milestones, and "
            "act as point of contact between clients and developers. Certified Scrum Master (CSM) or "
            "PMP is preferred. Minimum 1 year experience coordinating engineering processes."
        ] * 60  # 300 entries
        
        # Fake-sounding job postings with classic phishing signals
        suspicious_descriptions = [
            "EASY WORK FROM HOME! Earn $5000 weekly posting advertisement links online. No CV or "
            "interview necessary. Get paid daily in cryptocurrency or Western Union. All applicants "
            "accepted. Requirements: laptop, bank account, and internet access. Start immediately!",
            
            "FINANCIAL AGENT URGENTLY NEEDED. Receive incoming funds to your personal checking account. "
            "Withdraw cash and wire it to our partner logistics account using bitcoin ATMs. Keep a "
            "10% processing fee. Extremely easy income. Earn up to $3000/day. Send bank details now.",
            
            "Mystery shopper job opportunity. Get paid to buy gift cards and test local stores. We will "
            "mail you a certified cashier check for $2500. Deposit the check in your account, purchase "
            "Amazon gift cards, and email us the redemption codes. You keep $500. Quick cash!",
            
            "Data entry operator. Immediate hiring. Work flexible hours from home. Earnings of $50/hour. "
            "No resumes required. We interview only via Whatsapp/Telegram messaging. To secure the role, "
            "you must register your routing number for deposit setup. Click link to begin.",
            
            "Logistics assistant role. Receive physical packages at your home, inspect contents, and "
            "re-ship them to international destinations. Company covers shipping costs. Compensation: "
            "commission per package. No experience needed. Start today and earn easy side money."
        ] * 60  # 300 entries

        data = []
        for desc in authentic_descriptions:
            data.append({
                "title": "Software Engineer",
                "company_profile": "Established technology services company.",
                "description": desc,
                "requirements": "Strong algorithmic thinking and teamwork.",
                "fraudulent": 0
            })
            
        for desc in suspicious_descriptions:
            data.append({
                "title": "Work From Home Coordinator",
                "company_profile": "Startup international financial services LTD.",
                "description": desc,
                "requirements": "Must have active checking account for payments.",
                "fraudulent": 1
            })
            
        df = pd.DataFrame(data)
        # Shuffle records randomly
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        return df

    def prepare_data(self) -> tuple:
        """
        Loads the dataset, handles text concatenation/cleaning, and builds TF-IDF features.
        
        Returns:
            tuple: Training and testing matrices (X_train_vec, X_test_vec, y_train, y_test).
        """
        if os.path.exists(self.data_path):
            print(f"Found Kaggle Job Dataset at: {self.data_path}")
            df = pd.read_csv(self.data_path)
        else:
            df = self._generate_synthetic_data()
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            df.to_csv(self.data_path, index=False)
            print(f"Fallback CSV saved at: {self.data_path}")

        # Clean null values in text fields
        df['title'] = df['title'].fillna('')
        df['company_profile'] = df['company_profile'].fillna('')
        df['description'] = df['description'].fillna('')
        df['requirements'] = df['requirements'].fillna('')
        
        # Concatenate text features to create a single clean feature corpus
        df['combined_text'] = df['title'] + " " + df['company_profile'] + " " + df['description'] + " " + df['requirements']
        
        # Clean text
        print("Cleaning dataset corpus text...")
        df['clean_text'] = df['combined_text'].apply(self._clean_text)
        
        X = df['clean_text']
        y = df['fraudulent']
        
        # Perform stratified splitting to preserve class proportions
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Convert text into TF-IDF numerical vectors
        print("Fitting TF-IDF Vectorizer...")
        vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)
        
        # Save vectorizer artifact
        joblib.dump(vectorizer, self.vectorizer_path)
        print(f"TF-IDF Vectorizer successfully exported to: {self.vectorizer_path}")
        
        return X_train_vec, X_test_vec, y_train, y_test

    def train_and_evaluate(self) -> dict:
        """
        Trains and compares Random Forest, Support Vector Machine, Logistic Regression, 
        and Naive Bayes classifiers. Stores evaluation reports and exports the best model.
        
        Returns:
            dict: Comparison metrics and name of the best performing model.
        """
        X_train_vec, X_test_vec, y_train, y_test = self.prepare_data()
        
        models = {
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            "Support Vector Machine": SVC(kernel='linear', probability=True, random_state=42),
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
            "Naive Bayes": MultinomialNB()
        }
        
        comparison_stats = {}
        best_accuracy = 0.0
        best_model_name = ""
        best_model_object = None
        
        print("\n--- Starting Model Training and Evaluation ---")
        for name, classifier in models.items():
            print(f"Training Classifier: {name}...")
            classifier.fit(X_train_vec, y_train)
            
            # Predict and evaluate
            y_pred = classifier.predict(X_test_vec)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)
            
            comparison_stats[name] = {
                "accuracy": round(accuracy * 100, 2),
                "precision": round(report['weighted avg']['precision'] * 100, 2),
                "recall": round(report['weighted avg']['recall'] * 100, 2),
                "f1-score": round(report['weighted avg']['f1-score'] * 100, 2)
            }
            print(f"{name} Evaluation: Accuracy = {accuracy*100:.2f}%")
            
            # Check for the best model
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model_name = name
                best_model_object = classifier

        # Export best model
        joblib.dump(best_model_object, self.model_path)
        print(f"\nSaved Best Model ({best_model_name}) to: {self.model_path}")
        
        # Save analysis summary to json
        training_stats = {
            "comparison": comparison_stats,
            "best_model": {
                "name": best_model_name,
                "accuracy": round(best_accuracy * 100, 2)
            }
        }
        
        with open(self.stats_path, 'w') as f:
            json.dump(training_stats, f, indent=4)
        print(f"Exported training comparison JSON: {self.stats_path}")
        
        return training_stats

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_and_evaluate()
