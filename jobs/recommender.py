import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class JobRecommender:
    """
    Connects to JSearch API with dynamic multi-domain job query building.
    Generates tailored mock jobs for Medical/Healthcare, Business/Finance, Engineering, and Tech.
    """
    
    def __init__(self):
        self.api_key = os.getenv("RAPIDAPI_KEY")
        self.api_host = "jsearch.p.rapidapi.com"
        self.api_url = "https://jsearch.p.rapidapi.com/search"

    def fetch_jobs(self, skills: list, location: str = "India", num_jobs: int = 5) -> list:
        if not skills:
            return self._generate_mock_jobs(["Professional Specialist"], location, num_jobs)

        # Formulate search query dynamically across any domain
        top_skills = skills[:3]
        search_query = f"{', '.join(top_skills)} in {location}"
        logger.info(f"Querying Job Feed for: '{search_query}'")

        # Fallback to mock data if key is missing or default
        if not self.api_key or self.api_key == "your_rapidapi_key_here":
            return self._generate_mock_jobs(skills, location, num_jobs)

        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.api_host
        }
        params = {
            "query": search_query,
            "num_pages": "1",
            "date_posted": "all"
        }

        try:
            response = requests.get(self.api_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                raw_jobs = response.json().get("data", [])
                formatted = []
                for job in raw_jobs[:num_jobs]:
                    loc = ", ".join(filter(None, [job.get('job_city'), job.get('job_country')])) or "Remote"
                    formatted.append({
                        "title": job.get("job_title", "Specialist"),
                        "company": job.get("employer_name", "Enterprise Corp"),
                        "location": loc,
                        "description": job.get("job_description", "No description provided."),
                        "apply_link": job.get("job_apply_link", "https://careers.google.com")
                    })
                if formatted:
                    return formatted
        except Exception as e:
            logger.error(f"API query exception: {e}")

        return self._generate_mock_jobs(skills, location, num_jobs)

    def _generate_mock_jobs(self, skills: list, location: str, num_jobs: int) -> list:
        primary = skills[0] if skills else "Specialist"
        secondary = skills[1] if len(skills) > 1 else "Management"
        skills_str = ", ".join(skills[:5])

        # Detect domain based on primary skills
        med_keywords = ["MBBS", "Nursing", "Pharmacology", "Cardiology", "Surgery", "Clinical", "Patient", "Anatomy", "Pathology", "Health"]
        fin_keywords = ["Finance", "Accounting", "Auditing", "Marketing", "HR", "Sales", "Banking", "Taxation", "Investment"]
        eng_keywords = ["AutoCAD", "SolidWorks", "MATLAB", "PLC", "Civil", "Mechanical", "Electrical", "Structural"]

        if any(k.lower() in primary.lower() for k in med_keywords):
            # Medical / Healthcare Mock Openings
            templates = [
                {
                    "title": f"Medical Consultant - {primary}",
                    "company": "Apollo Hospitals Enterprise",
                    "location": f"Hyderabad, Telangana, {location}",
                    "description": f"Apollo Hospitals is hiring a Medical Associate with background in {primary} & {secondary}.\nKey Competencies: {skills_str}.\nRole: Patient assessment, diagnosis support, clinical compliance.",
                    "apply_link": "https://www.apollohospitals.com/careers"
                },
                {
                    "title": f"Clinical Research Specialist ({primary})",
                    "company": "Fortis Healthcare Ltd",
                    "location": f"Bangalore, Karnataka, {location}",
                    "description": f"Join our clinical operations unit. Responsibilities include trial protocol monitoring and healthcare data evaluation in {primary}.\nRequired Skills: {skills_str}.",
                    "apply_link": "https://www.fortishealthcare.com/careers"
                },
                {
                    "title": f"Healthcare Operations Associate",
                    "company": "Max Healthcare",
                    "location": f"Delhi NCR, {location}",
                    "description": f"We are seeking an energetic healthcare professional. Hands-on expertise in {primary} and {secondary} is highly preferred.\nSkills: {skills_str}.",
                    "apply_link": "https://www.maxhealthcare.in/careers"
                }
            ]
        elif any(k.lower() in primary.lower() for k in fin_keywords):
            # Finance / Business Openings
            templates = [
                {
                    "title": f"Senior {primary} Analyst",
                    "company": "Deloitte India",
                    "location": f"Mumbai, Maharashtra, {location}",
                    "description": f"Deloitte is looking for a specialist in {primary} and {secondary}.\nKey Skills: {skills_str}.\nResponsibilities: Client auditing, strategy consulting, business reporting.",
                    "apply_link": "https://www2.deloitte.com/careers"
                },
                {
                    "title": f"Associate - {primary} & Operations",
                    "company": "HDFC Bank Ltd",
                    "location": f"Bangalore, Karnataka, {location}",
                    "description": f"HDFC Bank is hiring in our corporate division. Background in {skills_str} required.\nExperience: 0-3 Years.",
                    "apply_link": "https://www.hdfcbank.com/careers"
                }
            ]
        else:
            # Technology / Engineering Openings
            templates = [
                {
                    "title": f"Associate Engineer - {primary}",
                    "company": "Tata Consultancy Services (TCS)",
                    "location": f"Bangalore, Karnataka, {location}",
                    "description": f"TCS is hiring an Associate Engineer with expertise in {primary}.\nSkills: {skills_str}.\nResponsibilities: System analysis, feature implementation, platform optimization.",
                    "apply_link": "https://www.tcs.com/careers"
                },
                {
                    "title": f"Specialist ({primary} & {secondary})",
                    "company": "Infosys Ltd",
                    "location": f"Hyderabad, Telangana, {location}",
                    "description": f"Infosys has open positions for professionals skilled in {primary}. Experience with {skills_str} is preferred.",
                    "apply_link": "https://www.infosys.com/careers"
                },
                {
                    "title": f"Technical Consultant - {primary}",
                    "company": "Wipro Technologies",
                    "location": f"Pune, Maharashtra, {location}",
                    "description": f"Wipro is seeking candidates with practical experience in {primary} & {secondary}.\nKey Skills: {skills_str}.",
                    "apply_link": "https://careers.wipro.com"
                }
            ]

        return templates[:num_jobs]