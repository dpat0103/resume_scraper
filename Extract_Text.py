import spacy
from pdfminer.high_level import extract_text
import re

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Function to parse resume text
def parse_resume(text):
    doc = nlp(text)
    resume_data = {
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "experience": [],
        "education": []
    }
    
    # Extract name (assuming the first sentence contains the name)
    if doc.ents:
        resume_data["name"] = doc.ents[0].text
    
    # Extract email and phone number
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    phone_pattern = re.compile(r"\b\d{10}\b")
    
    for token in doc:
        if email_pattern.match(token.text):
            resume_data["email"] = token.text
        if phone_pattern.match(token.text):
            resume_data["phone"] = token.text
    
    # Extract skills (example keywords, customize as needed)
    skill_keywords = {"Python", "Java", "C++", "Machine Learning", "Data Analysis"}
    for token in doc:
        if token.text in skill_keywords:
            resume_data["skills"].append(token.text)
    
    # Extract experience and education (based on common section headers)
    experience_section = False
    education_section = False
    
    for sent in doc.sents:
        sent_text = sent.text.lower()
        if "experience" in sent_text:
            experience_section = True
            education_section = False
        elif "education" in sent_text:
            experience_section = False
            education_section = True
        
        if experience_section and not any(header in sent_text for header in ["experience", "education"]):
            resume_data["experience"].append(sent.text)
        if education_section and not any(header in sent_text for header in ["experience", "education"]):
            resume_data["education"].append(sent.text)
    
    return resume_data

# Example usage
pdf_path = "_Resume - Amaad Rajpar.pdf"
resume_text = extract_text_from_pdf(pdf_path)
parsed_resume = parse_resume(resume_text)

print(parsed_resume)
