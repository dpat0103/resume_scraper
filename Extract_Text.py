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
    
    # Extract email
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    email_matches = email_pattern.findall(text)
    if email_matches:
        resume_data["email"] = email_matches[0]
    
    # Extract phone number
    phone_pattern = re.compile(r"\(?\b[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b")
    phone_matches = phone_pattern.findall(text)
    if phone_matches:
        resume_data["phone"] = phone_matches[0]
    
    # Extract name (using a heuristic approach for the first few lines of the document)
    lines = text.split('\n')
    for line in lines[:10]:  # Look at the first 10 lines to find the name
        if line.strip():  # Skip empty lines
            doc_line = nlp(line.strip())
            for ent in doc_line.ents:
                if ent.label_ == "PERSON":
                    resume_data["name"] = ent.text
                    break
            if resume_data["name"]:
                break
    

    
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

print("Name:", parsed_resume["name"])
print()
print("Email:", parsed_resume["email"])
print()
print("Phone:", parsed_resume["phone"])
print()
print("Skills:")
for skill in parsed_resume["skills"]:
    print(f"- {skill}")
print()
print("Experience:")
for exp in parsed_resume["experience"]:
    print(f"- {exp}")
print()
print("Education:")
for edu in parsed_resume["education"]:
    print(f"- {edu}")
print()