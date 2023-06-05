import spacy
nlp=spacy.load("en_core_web_sm")
user_query=(''' I am a Nurse developer having more then 2 years of experience. I am sound femilier with django framework and python commonly used libraries. I am looking for a Python developer position or a data engineer position in hamburg in a reputable organizations like . I am getting 110k in salary   ''')
query=nlp(user_query)

# for ent in query.ents:
#     print(ent.text,ent.label_)

pronoun=[]
lables=[]
coutries=[]
for token in query:
    if token.pos_ == "PROPN":
        pronoun.append(token)
print(pronoun)
for locations in query.ents:
    #print(locations.text,locations.ents)
    if locations.label_=='GPE':
        coutries.append(locations.text)

#print(pronoun)
#print(coutries)

nlp1 = spacy.load(r"./output/model-last")
doc=nlp1("suggest me dietion jobs in london")
print(doc.ents)
for locations in doc.ents:
    if locations.label_=='GPE':
        coutries.append(locations)
print(coutries)

crew_dog_nlp=spacy.load("/home/whitebox/crewdog-BE/jobs/AI_models")
doc = crew_dog_nlp("Physician nurse is a medical job in the U.S.")
print([(ent.text, ent.label_) for ent in doc.ents])

