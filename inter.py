from pymongo import MongoClient
import re

client=MongoClient("mongodb+srv://talhayasir:123fightfight@whiteboxscrapper.f0zx0xd.mongodb.net/?retryWrites=true&w=majority")
db=client['job_scraper']

patterns = ['psychiatrist', 'nurse']

# Compile the regex patterns
regex_objects = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
print(regex_objects)

query = {
    'position': {'$in': regex_objects}
}

# Perform the query
results = db.jobs.find(query,{'_id':0})

# Iterate over the results
for result in results:
    print(result)
