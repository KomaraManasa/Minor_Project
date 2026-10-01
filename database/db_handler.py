import sqlite3
import os
import json
from datetime import datetime

class DatabaseHandler:
    """
    Handles SQLite database operations for the Smart Career Recommendation application.
    Includes tables for resumes, extracted skills, jobs recommendations, and job authenticity verifications.
    """
    
    def __init__(self, db_path=None):
        """
        Initializes the database connection and creates tables if they do not exist.
        
        Args:
            db_path (str, optional): Absolute path to the SQLite database file. 
                                     Defaults to 'career_app.db' in the database folder.
        """
        if db_path is None:
            # Place career_app.db in the same directory as this script by default
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, "career_app.db")
        else:
            self.db_path = db_path
        
        self._create_tables()

    def _get_connection(self):
        """
        Establishes and returns a database connection.
        Configures Row factory to allow dictionary-like row access.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        """
        Creates SQLite tables for schema requirements.
        Uses relational integrity with foreign keys.
        """
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        create_resumes_table = """
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            extracted_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_skills_table = """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            skills_list TEXT NOT NULL,  -- Stored as JSON string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id) ON DELETE CASCADE
        );
        """
        
        create_jobs_table = """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            description TEXT,
            apply_link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id) ON DELETE CASCADE
        );
        """
        
        create_verifications_table = """
        CREATE TABLE IF NOT EXISTS verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_description TEXT NOT NULL,
            prediction_result TEXT NOT NULL,  -- 'Authentic' or 'Suspicious'
            confidence_score REAL NOT NULL,
            reasons TEXT NOT NULL,            -- Stored as JSON string list
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(create_resumes_table)
                cursor.execute(create_skills_table)
                cursor.execute(create_jobs_table)
                cursor.execute(create_verifications_table)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error during table initialization: {e}")
            raise

    def save_resume(self, filename: str, text: str) -> int:
        """
        Inserts resume details into the database.
        
        Args:
            filename (str): Name of the uploaded resume file.
            text (str): Extracted text from the PDF.
            
        Returns:
            int: The primary key ID of the inserted resume.
        """
        query = "INSERT INTO resumes (filename, extracted_text) VALUES (?, ?)"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (filename, text))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error saving resume: {e}")
            raise

    def save_skills(self, resume_id: int, skills: list) -> int:
        """
        Saves the list of extracted skills for a specific resume.
        
        Args:
            resume_id (int): Foreign key referring to resumes.id.
            skills (list): Python list of extracted skill strings.
            
        Returns:
            int: The primary key ID of the inserted skills row.
        """
        query = "INSERT INTO skills (resume_id, skills_list) VALUES (?, ?)"
        skills_json = json.dumps(skills)
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (resume_id, skills_json))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error saving skills: {e}")
            raise

    def save_recommended_jobs(self, resume_id: int, jobs: list):
        """
        Saves a list of recommended job listings associated with a resume.
        
        Args:
            resume_id (int): Foreign key referring to resumes.id.
            jobs (list): List of dictionaries, each containing 'title', 'company', 
                         'location', 'description', and 'apply_link'.
        """
        query = """
        INSERT INTO jobs (resume_id, title, company, location, description, apply_link)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                for job in jobs:
                    cursor.execute(query, (
                        resume_id,
                        job.get("title", ""),
                        job.get("company", ""),
                        job.get("location", ""),
                        job.get("description", ""),
                        job.get("apply_link", "")
                    ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error saving jobs: {e}")
            raise

    def save_verification(self, job_description: str, prediction_result: str, 
                          confidence_score: float, reasons: list) -> int:
        """
        Saves verification logs of job descriptions.
        
        Args:
            job_description (str): Full text description of the verified job.
            prediction_result (str): Classifier label ('Authentic' or 'Suspicious').
            confidence_score (float): Reliability score percentage (0.0 to 100.0).
            reasons (list): Explanation strings for the prediction.
            
        Returns:
            int: The primary key ID of the inserted verification.
        """
        query = """
        INSERT INTO verifications (job_description, prediction_result, confidence_score, reasons)
        VALUES (?, ?, ?, ?)
        """
        reasons_json = json.dumps(reasons)
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (job_description, prediction_result, confidence_score, reasons_json))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error saving verification: {e}")
            raise

    def get_resumes(self) -> list:
        """
        Fetches all stored resumes in descending order of upload date.
        
        Returns:
            list: List of dictionaries matching the database records.
        """
        query = "SELECT * FROM resumes ORDER BY created_at DESC"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error fetching resumes: {e}")
            return []

    def get_skills_by_resume(self, resume_id: int) -> list:
        """
        Retrieves skills list parsed from a specific resume.
        
        Args:
            resume_id (int): Primary key of the resume.
            
        Returns:
            list: List of skill strings.
        """
        query = "SELECT skills_list FROM skills WHERE resume_id = ? ORDER BY created_at DESC LIMIT 1"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                row = cursor.execute(query, (resume_id,)).fetchone()
                if row:
                    return json.loads(row["skills_list"])
                return []
        except sqlite3.Error as e:
            print(f"Database error fetching skills: {e}")
            return []

    def get_jobs_by_resume(self, resume_id: int) -> list:
        """
        Retrieves recommended jobs for a specific resume.
        
        Args:
            resume_id (int): Primary key of the resume.
            
        Returns:
            list: List of dictionaries containing the recommended job details.
        """
        query = "SELECT * FROM jobs WHERE resume_id = ? ORDER BY created_at DESC"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (resume_id,))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error fetching jobs: {e}")
            return []

    def get_all_verifications(self) -> list:
        """
        Fetches all job authenticity predictions made.
        
        Returns:
            list: List of dictionaries matching the verification records.
        """
        query = "SELECT * FROM verifications ORDER BY created_at DESC"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                results = []
                for row in cursor.fetchall():
                    item = dict(row)
                    item["reasons"] = json.loads(item["reasons"])
                    results.append(item)
                return results
        except sqlite3.Error as e:
            print(f"Database error fetching verifications: {e}")
            return []

    def get_dashboard_stats(self) -> dict:
        """
        Compiles analytical counts and metrics for display on the Results Dashboard.
        
        Returns:
            dict: Summary statistics including counts and confidence details.
        """
        stats = {
            "total_resumes": 0,
            "total_verified": 0,
            "authentic_count": 0,
            "suspicious_count": 0,
            "average_confidence": 0.0,
            "recent_verifications": []
        }
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Total Resumes Count
                cursor.execute("SELECT COUNT(*) FROM resumes")
                stats["total_resumes"] = cursor.fetchone()[0]
                
                # Total Verified and Average Confidence
                cursor.execute("SELECT COUNT(*), AVG(confidence_score) FROM verifications")
                v_count, avg_conf = cursor.fetchone()
                stats["total_verified"] = v_count or 0
                stats["average_confidence"] = round(avg_conf, 2) if avg_conf else 0.0
                
                # Authentic vs Suspicious counts
                cursor.execute("SELECT prediction_result, COUNT(*) FROM verifications GROUP BY prediction_result")
                for result, count in cursor.fetchall():
                    if result.lower() == "authentic":
                        stats["authentic_count"] = count
                    elif result.lower() == "suspicious":
                        stats["suspicious_count"] = count
                
                # Recent verifications list (last 5 entries)
                cursor.execute("SELECT prediction_result, confidence_score, created_at FROM verifications ORDER BY created_at DESC LIMIT 5")
                stats["recent_verifications"] = [dict(row) for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            print(f"Database error fetching dashboard metrics: {e}")
            
        return stats
