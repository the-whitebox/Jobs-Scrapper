import pandas as pd
from pymongo import MongoClient
import tiktoken



def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)


    return conn[db]


def read_mongo(db, collection, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find({'job_source':'linkedin'},{'search_keywords':0,'job_type':0,'time_stamp':0,'_id':0,'other_information':0,'posted_date':0,'search_keyword':0})

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id

    return df
# data_fram=read_mongo('job_scraper','jobs')
# print(data_fram.columns)
def remove_new_lines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    
    print(type(serie))
    
    return serie



# Visualize the distribution of the number of tokens per row using a histogram

tokenizer = tiktoken.get_encoding("cl100k_base")
# Function to split the text into chunks of a maximum number of tokens
def split_into_many(text, max_tokens = 500):

    # Split the text into sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    
    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater 
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of 
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks
def create_token(df):
    
    df['n_tokens'] = df.details.apply(lambda x: len(tokenizer.encode(x)))

    shortened = []
    for row in df.iterrows():
        #print(list(row))

        # If the text is None, go to the next row
        if row[1]['details'] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > 500:
            text_chunks = split_into_many(row[1]['details'])
            #print(text_chunks)
            
            shortened.extend([{'job_id':str(row[1]['job_id']),'position': row[1]['position'], 'details': chunk, 'company': row[1]['company'],'location':row[1]['location'],'job_source':row[1]['job_source'],'hiring_person':row[1]['hiring_person'],'hiring_person_linkedin_link':row[1]['hiring_person_linkedin_link']} for chunk in text_chunks])
            #print(shortened)
        
        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append({'job_id':str(row[1]['job_id']),'position':row[1]['position'],'details':row[1]['details'],'company':row[1]['company'],'location':row[1]['location'],'job_source':row[1]['job_source'],'hiring_person':row[1]['hiring_person'],'hiring_person_linkedin_link':row[1]['hiring_person_linkedin_link']})
    #print(shortened)
    df = pd.DataFrame(shortened, columns = ['job_id','position','company','location','job_source','hiring_person','hiring_person_linkedin_link','details'])
    df['n_tokens'] = df.details.apply(lambda x: len(tokenizer.encode(x)))
    return df

def final_datafram(): 

    df = read_mongo("job_scraper","jobs")
    # get sample of last 100 jobs
    sample_df=df.tail(200) 

    


    # Tokenize the text and save the number of tokens to a new column

    tokened_data_fram=create_token(sample_df)

    tokened_data_fram['details'] = remove_new_lines(tokened_data_fram.details)
    tokened_data_fram['details']=tokened_data_fram['details'].str.slice(13,)
    try:
        df.to_csv('sample.csv')
        print("Sample data saved in csv.....................")
    except:
        print("csv not saved ...................")   
    return tokened_data_fram
#print(final_datafram())