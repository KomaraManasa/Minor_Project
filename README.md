# Smart Career Recommendation using Data-Driven Intelligence

An advanced, full-stack career assistant and security audit application. This system helps job seekers find open careers matching their skills parsed from PDF resumes, and checks the authenticity of job listings using machine learning algorithms trained on Kaggle's Fake Job Posting dataset.

---

## 🎯 Key Features

1. **Resume PDF Processing**: Automatic text extraction and token scrubbing.
2. **NLP Skill Miner**: Named entity matching to extract specific engineering competencies.
3. **API-Driven Matching**: Queries JSearch endpoints for live job matching based on extracted skills.
4. **Scam Classification Engine**: Compares Random Forest, Support Vector Machine, Logistic Regression, and Naive Bayes classifiers to predict whether a job description is legitimate or fraudulent.
5. **Interactive Explanations**: Details regular-expression flags and ML confidence values explaining predictions.
6. **SQLite Relational Logging**: Saves all resumes, skill tags, matched careers, and verification histories locally.
7. **Visual Analytics Dashboard**: Draws interactive Plotly figures of model scores and verification distributions.

---

## 📂 Project Structure

```text
SmartCareerRecommendation/
├── app.py                      # Main entrypoint setting up Streamlit configuration
├── requirements.txt            # Project dependencies (Streamlit, PyPDF2, spacy, scikit-learn, etc.)
├── .env.example                # Template for environment variables (API keys)
├── README.md                   # Setup and usage guide
├── resume/
│   ├── __init__.py
│   ├── parser.py               # Extract text from PDFs using PyPDF2
│   └── cleaner.py              # Text cleaning and preprocessing
├── utils/
│   ├── __init__.py
│   └── nlp_skills.py           # NLP skill extraction using spaCy and NLTK
├── jobs/
│   ├── __init__.py
│   └── recommender.py          # RapidAPI JSearch connector for live job search
├── verification/
│   ├── __init__.py
│   ├── trainer.py              # Training script comparing RF, SVM, LR, and NB models
│   └── model.py                # Job description verification classifier wrapper
├── database/
│   ├── __init__.py
│   └── db_handler.py           # SQLite database operations (resumes, skills, jobs, predictions)
├── assets/
│   └── custom.css              # Custom styling for premium Streamlit UI
└── data/
    └── fake_job_postings.csv   # Dataset for training (automatically generated as mockup if missing)
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Install Dependencies
Run the package manager to download libraries:
```bash
pip install -r requirements.txt
```
*Note: The system automatically checks and downloads NLTK resources and the spaCy `en_core_web_sm` model at first runtime.*

### 3. API Setup
1. Obtain a free JSearch API key by subscribing to JSearch on [RapidAPI](https://rapidapi.com/letscrape-6584-letscrape-free/api/jsearch).
2. Copy `.env.example` to create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and fill in your RapidAPI Key:
   ```text
   RAPIDAPI_KEY=your_copied_api_key_here
   ```
*If this key is missing or not provided, the application will automatically fall back to serving high-quality mock jobs to ensure visual stability during live demonstrations.*

### 4. Training the Model
For full production-grade accuracy:
1. Download the **Fake Job Postings Dataset** (`fake_job_postings.csv`) from [Kaggle](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction).
2. Place the CSV file in the `data/` folder as `data/fake_job_postings.csv`.
3. Train the model by running the training pipeline script:
   ```bash
   python -m verification.trainer
   ```
*If you do not have the Kaggle dataset downloaded yet, running the script or launching the Streamlit app will automatically generate a structured, synthetic dataset inside `data/fake_job_postings.csv` and train the models on it, ensuring the application remains plug-and-play.*

---

## 🚀 Running the Web Application

Launch the Streamlit web server directly from the terminal:
```bash
python -m streamlit run app.py
```

The application will launch and open in your default browser at `http://localhost:8501`.

---

## 📊 Evaluation & Metrics
The training pipeline compiles classification metrics for four algorithms. On the synthetic dataset, accuracies are typically:
- **Random Forest**: ~99% Accuracy
- **Support Vector Machine**: ~97% Accuracy
- **Logistic Regression**: ~95% Accuracy
- **Naive Bayes**: ~91% Accuracy

You can view the exact evaluation metrics and comparative bar charts inside the **5_Dashboard** page in the sidebar.
