import spacy
from tqdm import tqdm
from spacy.tokens import DocBin
train_data=[('I am doctor and finding the jobs in london',{"entities":[(5,10,"job_title")]}),
            ('hi, I am the nurse in and blongs to madical profession. I am finding the nursing position in canada',{"entities":[(13,17,"job_title")]}),
            ('I am Registered Nurse and finding the jobs in london',{"entities":[(5,21,"job_title")]}),
            ('I am Physician Assistant and finding the jobs in london',{"entities":[(5,23,"job_title")]}),
            ('please suggest me the job regarding Medical Assistant and finding the jobs in london',{"entities":[(34,51,"job_title")]}),
            ('please suggest me the job regarding Physical Therapist and finding the jobs in london',{"entities":[(34,52,"job_title")]}),
            ('I am Occupational Therapist and finding the jobs in london',{"entities":[(5,18,"job_title")]}),
            ('I am Pharmacist and finding the jobs in london',{"entities":[(5,15,"job_title")]}),
            ('I am actively looking for the role as a pharmacist',{"entities":[(39,50,"job_title")]}),
            ('I am actively looking for the role as a Medical Technologist',{"entities":[(39,52,"job_title")]}),
            ('I am actively looking for the role as a Medical Doctor',{"entities":[(39,53,"job_title")]}),
            ('I am actively looking for the role as a Psychologist in USA',{"entities":[(39,51,"job_title")]}),
            ("i need a job, i have worked as a Recruiter in the past. i have good experience as Health Coach as well.",{'entities': [(82, 93, 'job_title'), (33, 41, 'job_title')]}),
            ('find a Surgeon jobs for me in Qatar ',{"entities":[(7,15,"job_title")]})            
            ]
nlp=spacy.blank("en")
db=DocBin()

for text, annot in tqdm(train_data): # data in previous format
    doc = nlp.make_doc(text) # create doc object from text
    ents = []
    for start, end, label in annot["entities"]: # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents # label the text with the ents
    db.add(doc)

db.to_disk("./train.spacy")
