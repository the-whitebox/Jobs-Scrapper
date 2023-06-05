import spacy

nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler")
patterns = [{"label": "job_title", "pattern": [{"LOWER":"Registered"},{"LOWER":"Nurse"}]},
            {"label": "job_title", "pattern": [{"LOWER":"Physician"},{"LOWER":"Assistant"}]},
            {"label": "job_title", "pattern": [{"LOWER":"Physical"},{"LOWER":"Therapist"}]},
            {"label": "job_title", "pattern": [{"LOWER":"Occupational"},{"LOWER":"Therapist"}]},
            
            {"label": "job_title", "pattern": "Physical Therapist"},
            {"label": "job_title", "pattern": "Occupational Therapist"},
            {"label": "job_title", "pattern": [{"LOWER":"Speech-Language"},{"LOWER":"Pathologist"}]},

            {"label": "job_title", "pattern": "Speech-Language Pathologist"},
            {"label": "job_title", "pattern": [{"LOWER":"Registered"},{"LOWER":"Dietitian"},{"LOWER":"Nutritionist"}]},

            {"label": "job_title", "pattern": "Registered Dietitian Nutritionist"},
            {"label": "job_title", "pattern": "Pharmacist"},
            {"label": "job_title", "pattern": "Medical Technologist"},
            {"label": "job_title", "pattern": [{"LOWER":"Medicale"},{"LOWER":"Technologist"}]},

            {"label": "job_title", "pattern": "Health Information Management Specialist"},
            {"label": "job_title", "pattern": [{"LOWER":"Health"},{"LOWER":"Information"},{"LOWER":"Management"},{"LOWER":"Specialist"}]},

            {"label": "job_title", "pattern": "Health Educator"},
            {"label": "job_title", "pattern": [{"LOWER":"Health"},{"LOWER":"Educator"}]},

            {"label": "job_title", "pattern": "Nurse Practitioner"},
            {"label": "job_title", "pattern": [{"LOWER":"Nurse"},{"LOWER":"Practitioner"}]},

            {"label": "job_title", "pattern": "Medical Doctor"},
            {"label": "job_title", "pattern": [{"LOWER":"Medical"},{"LOWER":"Doctor"}]},

            {"label": "job_title", "pattern": "Psychologist"},
            {"label": "job_title", "pattern": "Public Health Specialist"},
            {"label": "job_title", "pattern": "Health Coach"},
            {"label": "job_title", "pattern": [{"LOWER":"Health"},{"LOWER":"Coach"}]},

            {"label": "job_title", "pattern": "Massage Therapist"},
            {"label": "job_title", "pattern": [{"LOWER":"Massage"},{"LOWER":"Therapist"}]},

            {"label": "job_title", "pattern": "Acupuncturist"},
            {"label": "job_title", "pattern": "Chiropractor"},
            {"label": "job_title", "pattern": "Physician"},
            {"label": "job_title", "pattern": "surgeon"},
            {"label": "job_title", "pattern": "Surgeon"},

            
            {"label": "job_title", "pattern": "Emergency Medical Technician (EMT)"},
            {"label": "job_title", "pattern": "Radiologic Technologist"},
            {"label": "job_title", "pattern": [{"LOWER":"Radiologic"},{"LOWER":"Technologist"}]},

            {"label": "job_title", "pattern": "Patient Navigator"},
            {"label": "job_title", "pattern": [{"LOWER":"Patient"},{"LOWER":"Navigator"}]},

            {"label": "job_title", "pattern": "Medical Administrative Assistant"},
            {"label": "job_title", "pattern": "doctor"},
            {"label": "job_title", "pattern": [{"LOWER":"nurse"}]},
            {"label": "job_title", "pattern": [{"LOWER":"Physiotherapist"}]},
            {"label": "job_title", "pattern": [{"LOWER":"physiotherapist"}]},
            {"label": "job_title", "pattern": [{"LOWER":"Practitioner"}]},
            {"label": "job_title", "pattern": [{"LOWER":"practitioner"}]},

            

            

            
            
            ]
ruler.add_patterns(patterns)
nlp.to_disk("/home/whitebox/crewdog-BE/jobs/AI_models")

doc = nlp("Registered Dietitian Nutritionist is a medical job in the U.S.")
print([(ent.text, ent.label_) for ent in doc.ents])