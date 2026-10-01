import spacy
import re
import logging

# Configure logger
logger = logging.getLogger(__name__)

class SkillExtractor:
    """
    Extracts multi-domain professional skills from resume text using spaCy and
    rule-based token boundary adjudication.
    Supports Computer Science, Medical & Healthcare, Finance & Business, and Core Engineering.
    """
    
    def __init__(self):
        # Load English spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            logger.warning("spaCy model 'en_core_web_sm' not loaded, using blank English model.")
            self.nlp = spacy.blank("en")

        # Multi-Domain Skill Knowledge Base
        self.skills_db = [
            # ==========================================
            # 1. MEDICAL, HEALTHCARE & PHARMA
            # ==========================================
            "MBBS", "MD", "BAMS", "BHMS", "Nursing", "Pharmacology", "Anatomy",
            "Physiology", "Pathology", "Microbiology", "Biochemistry", "Cardiology",
            "Neurology", "Pediatrics", "Dermatology", "Orthopedics", "Radiology",
            "Anesthesia", "Surgery", "Clinical Research", "Clinical Trials",
            "Patient Care", "Healthcare Management", "Medical Coding", "ICD-10",
            "Pharmacovigilance", "Drug Discovery", "Medical Device", "Telemedicine",
            "Electronic Health Records", "EHR", "EMR", "Emergency Care", "Diagnostics",
            "Phlebotomy", "Physical Therapy", "Public Health", "Dentistry", "Pharmacy",

            # ==========================================
            # 2. BUSINESS, FINANCE & MANAGEMENT
            # ==========================================
            "Accounting", "Financial Analysis", "Auditing", "Taxation", "Investment Banking",
            "Corporate Finance", "Risk Management", "Portfolio Management", "Wealth Management",
            "Digital Marketing", "SEO", "SEM", "Content Strategy", "Social Media Marketing",
            "Human Resources", "Recruitment", "Talent Acquisition", "Payroll Management",
            "Project Management", "Agile", "Scrum", "Business Development", "Sales",
            "Supply Chain Management", "Logistics", "Operations Management", "Business Strategy",
            "Market Research", "Financial Modeling", "QuickBooks", "SAP", "Excel Modeling",

            # ==========================================
            # 3. CORE ENGINEERING (Mechanical, Civil, Electrical)
            # ==========================================
            "AutoCAD", "SolidWorks", "CATIA", "ANSYS", "MATLAB", "Thermodynamics",
            "Fluid Mechanics", "Robotics", "PLC", "SCADA", "Circuit Design", "Embedded Systems",
            "PCB Design", "VLSI", "Power Systems", "Structural Analysis", "Revit", "STAAD Pro",
            "Surveying", "Geotechnical Engineering", "CNC Programming", "Six Sigma",

            # ==========================================
            # 4. COMPUTER SCIENCE & IT (Existing Taxonomy)
            # ==========================================
            "Python", "Java", "C++", "C#", "C", "JavaScript", "TypeScript", "PHP", "Ruby",
            "Go", "Rust", "Kotlin", "Swift", "R", "Scala", "Dart", "HTML", "CSS", "SQL",
            "React", "Angular", "Vue", "Next.js", "Node.js", "Express", "Django", "Flask",
            "FastAPI", "Spring Boot", "ASP.NET", "Laravel", "PyTorch", "TensorFlow",
            "Keras", "Scikit-Learn", "OpenCV", "NLTK", "spaCy", "Hugging Face", "Pandas",
            "NumPy", "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins",
            "Git", "GitHub", "GitLab", "Linux", "PostgreSQL", "MySQL", "MongoDB", "Redis",
            "GraphQL", "REST API", "Microservices", "CI/CD", "Machine Learning",
            "Deep Learning", "Natural Language Processing", "Computer Vision", "Blockchain",
            "Cybersecurity", "Penetration Testing", "Ethical Hacking", "Cryptography"
        ]

    def extract_skills(self, text: str) -> list:
        """
        Parses resume text and extracts matching domain competencies.
        """
        if not text or not isinstance(text, str):
            return []

        text_lower = text.lower()
        extracted = []

        for skill in self.skills_db:
            skill_lower = skill.lower()
            
            # Non-capturing group boundary checks to avoid substring collisions
            if len(skill_lower) <= 2:
                pattern = r'(?:^|[\s,.(/])' + re.escape(skill_lower) + r'(?:[\s,.)/]|$)'
            else:
                pattern = r'(?:^|[\s,.(/])' + re.escape(skill_lower) + r'(?:[\s,.)/]|$)'
                
            if re.search(pattern, text_lower):
                extracted.append(skill)

        # Deduplicate and sort
        unique_skills = sorted(list(set(extracted)), key=lambda x: (len(x), x), reverse=True)
        return sorted(unique_skills)