import docx2txt
import re
import spacy

def extract_text(resume_path):
    resume_text = docx2txt.process(resume_path)
    text = [line.replace('\t', ' ') for line in resume_text.split('\n') if line]
    return ' '.join(text)

result = extract_text("test.docx")

def extract_info(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for token in doc.ents:
#print(token.text, token.label_)
        if token.label_ == 'PERSON':
            print(token.text)
            return
def extract_number(text):
    phone = re.findall(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-.)]*(\d{3})[-. ]*(\d{4})\b', text)
    for match in phone:
        print("".join(match))


extract_info(result)
extract_number(result)
