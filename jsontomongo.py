import pymongo
import json
from collections import  OrderedDict
from pymongo import MongoClient, InsertOne

client = pymongo.MongoClient("mongodb+srv://talhayasir:123fightfight@whiteboxscrapper.f0zx0xd.mongodb.net/?retryWrites=true&w=majority")
db = client.job_scraper
collection = db.jobs
requesting = []

with open(r"jobs.json") as f:
    data=json.load(f)
    # print(data)
    def rename(old_dict,old_name,new_name):
        new_dict = {}
        for key,value in zip(old_dict.keys(),old_dict.values()):
            new_key = key if key != old_name else new_name
            new_dict[new_key] = old_dict[key]
        return new_dict
    for doc in data:
        updated_dict=rename(doc,"title","position")
        updatedDict=rename(updated_dict,"Description","details")
        # new_dict=OrderedDict(doc)
        # new_dict.rename("title","position")
        # new_dict.rename("Description","details")
        # new_dict["job_source"]="gumtree"
        # # for key,value in doc.items():
        # #     if key=='title':
        # #         new_dict[key]='position'
        # #     if key=='Description':
        # #         new_dict[key]='details'
        # #     else:
        # #         new_dict['key']=value
        # # #new_dict={"position" if k == 'title' else k:v for k,v in doc.items()}
        # # #new_dict={"details" if k == 'Description' else k:v for k,v in doc.items()}
        updatedDict["job_source"]="gumtree"
        insert=collection.insert_one(updatedDict)
        if insert:
            print("data inserted",updatedDict)
        #print(updatedDict)

        
        

    
        

#     for jsonObj in f:
#         print("-------------",jsonObj)
#         #myDict = jsonObj
#         #print("This is a dict--------------------------------",myDict)
# #         requesting.append(InsertOne(myDict))
# #         print('inserted in db',jsonObj)

# # # result = collection.bulk_write(requesting)
client.close()