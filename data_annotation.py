from pymongo import MongoClient
client=MongoClient("mongodb+srv://talhayasir:123fightfight@whiteboxscrapper.f0zx0xd.mongodb.net/?retryWrites=true&w=majority")
db=client['job_scraper']
import csv
import pandas as pd

jobs_descriptions=db.jobs.find({},{'_id':0,'details':1})
db_keys=[]
for description in jobs_descriptions:
    db=str(description.get('details'))
    #print(db)
    print(type(db))
    db_keys.append(db)
print(db_keys)





keywords = ['Physician Assistant','Registered Nurse','Medical Assistant','PhysicalTherapist','Occupational Therapist','Speech-LanguagePathologist','Registered Dietitian Nutritionist','Pharmacist','Medical Technologist','Health Information Management Specialist','ClinicalResearchCoordinator','Health Educator','Nurse' 'Practitioner','Medical Doctor','Psychologist','SocialWorker','Psychiatrist','Public Health Specialist','Health Coach','Massage Therapist','Acupuncturist','Chiropractor','Physician','Surgeon','Radiologic Technologist','Patient Navigator','Medical Transcriptionist','Billing and Coding Specialist','Medical Administrative Assistant','Emergency Medical Technician (EMT)','Care worker','Recruiter','Ophthalmologist','doctor','nurse','surgeon'
]
# data=pd.read_csv("query_set.csv")
# strings=list(data['query'])
# print(strings)       
def data_annotate(strings):
    train_data = []
    for q_string in strings:
        keyword_list = []
        for keyword in keywords:
            if keyword:
                start_index = q_string.find(keyword)
                if start_index != -1:
                    end_index = start_index + len(keyword) - 1
                    keyword_list.append((start_index,end_index,"job_title"))
            else:
                print("keyword not found")
        data = {"entities":keyword_list}

        training_str=f'''{q_string},{data}'''
        training_tuple=tuple((q_string,data))
        train_data.append(training_tuple)
    # print(train_data)
    # print(len(train_data))
    return train_data
data_set_list=data_annotate(db_keys)
print(data_set_list)
print(len(data_set_list))

# for data in train_data:
#     print(data)
# print(len(train_data))




# test_str="I am a doctor and finding the jobs in london"
# check_list = ["doctor", "medical", "surgeon", "london"]

# res = dict()
# for ele in check_list :
#     if ele in test_str:
         
#         # getting front index
#         strt = test_str.find(ele)
         
#         # getting ending index
#         res[ele] = [strt, strt + len(ele) - 1]
#         end=strt+len(ele)-1
        
#         training_str=f'''({test_str},{ {"entities":[(strt,end,"job_title")]} })'''
 
# # printing result
# print("Required extracted indices : " + training_str)



