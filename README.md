# Smart Career Recommendation

A career recommendation and job verification application built using Python and Streamlit. The system helps users find job opportunities based on skills extracted from PDF resumes and checks job postings using machine learning models trained on a fake job posting dataset.

## Key Features

1. Resume PDF Processing: Extracts text from PDF resumes and cleans the extracted content.
2. Skill Extraction: Identifies relevant skills from the resume using NLP techniques.
3. Job Matching: Uses the JSearch API to search for job postings based on extracted skills.
4. Job Verification: Compares Random Forest, Support Vector Machine, Logistic Regression, and Naive Bayes models to classify job postings.
5. Verification Details: Provides the prediction result along with supporting checks from the job posting.
6. SQLite Database: Stores resume information, extracted skills, job searches, and verification history.
7. Dashboard: Displays model evaluation results and previous verification information.

## Project Structure

```text
SmartCareerRecommendation/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── resume/
│   ├── __init__.py
│   ├── parser.py
│   └── cleaner.py
├── utils/
│   ├── __init__.py
│   └── nlp_skills.py
├── jobs/
│   ├── __init__.py
│   └── recommender.py
├── verification/
│   ├── __init__.py
│   ├── trainer.py
│   └── model.py
├── database/
│   ├── __init__.py
│   └── db_handler.py
├── assets/
│   └── custom.css
└── data/
    └── fake_job_postings.csv
Installation and Setup
1. Prerequisites

Make sure Python 3.8 or a later version is installed.

2. Install Dependencies

Run:

pip install -r requirements.txt

The application uses Python libraries such as Streamlit, PyPDF2, spaCy, NLTK, scikit-learn, pandas, NumPy, requests, joblib, and Plotly.

3. API Setup

The application can use the JSearch API to search for live job postings.

Create a .env file in the project root and add your API key:

RAPIDAPI_KEY=your_api_key_here

The .env file is not included in the GitHub repository. The repository contains .env.example as a template.

If the API key is not available, the application can use the available job data in the project for demonstration purposes.

4. Training the Model

The job verification model uses a fake job posting dataset for training.

Place the dataset at:

data/fake_job_postings.csv

Then run:

python -m verification.trainer

The training script processes the dataset, converts the job posting text into TF-IDF features, trains multiple classification models, evaluates them, and saves the selected model and vectorizer in the models folder.

The models compared are:

Random Forest
Support Vector Machine
Logistic Regression
Multinomial Naive Bayes

The evaluation includes:

Accuracy
Precision
Recall
F1-score
5. Running the Application

Start the Streamlit application using:

python -m streamlit run app.py

The application will open in the browser at:

http://localhost:8501
Application Workflow
Upload a resume in PDF format.
Extract and clean the resume text.
Extract relevant skills from the resume.
Search for job postings based on the extracted skills.
Select a job posting for verification.
Use the trained machine learning model to classify the job posting.
View the verification result and previous results in the dashboard.
Machine Learning

The verification module uses TF-IDF to convert job posting text into numerical features.

The following classification models are trained and compared:

Random Forest
Support Vector Machine
Logistic Regression
Multinomial Naive Bayes

The model evaluation results are stored in the models folder along with the trained model and TF-IDF vectorizer.

Database

The project uses SQLite for local data storage.

The database can store information related to:

Resumes
Extracted skills
Job searches
Job postings
Verification results
Project Technologies
Python
Streamlit
PyPDF2
spaCy
NLTK
scikit-learn
pandas
NumPy
REST API
SQLite
Plotly
Notes

The project was developed as a student project to understand resume processing, NLP, API-based job searching, machine learning classification, and database operations.

The machine learning results depend on the dataset used for training. Therefore, the verification result should be treated as a prediction based on the available training data and not as a guaranteed determination that a job posting is genuine or fraudulent.
