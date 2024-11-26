from pymongo import MongoClient
from datetime import datetime, timedelta
import logging
import os
from pinecone import Pinecone

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://shahbazkhan6732:2orI37mNuhTtKzya@cluster0.nqxuncj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['job_scraper']

jobs_collection = db['jobs']
expired_jobs_collection = db['expired3821jobs']  # New collection to store expired jobs

# Pinecone API key and environment
os.environ['PINECONE_API_KEY'] = "74dbb1f3-abda-4c51-8c24-3e600c7796f4"
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
index = pc.Index("whitebox")

def delete_old_jobs():
    """Delete jobs older than 15 days from MongoDB and Pinecone, and save them in the expired collection."""
    # Calculate the cutoff date (15 days ago from today)
    cutoff_date = datetime.utcnow() - timedelta(days=15)
    logger.info(f"Cutoff date: {cutoff_date}")

    old_jobs = jobs_collection.find()  # Get all jobs to check their timestamps

    # Initialize a counter for deleted jobs
    deleted_count = 0

    for job in old_jobs:
        job_id = job['job_id']  # Get the job_id field
        
        job_time_stamp_str = job['time_stamp']  # Get the time_stamp as a string
        
        # Convert the string timestamp to a datetime object
        job_time_stamp = datetime.strptime(job_time_stamp_str, '%Y-%m-%d %H:%M:%S.%f')
        
        # Check if the job is older than the cutoff date
        if job_time_stamp < cutoff_date:
            try:
                # Save the job to the expired jobs collection
                expired_jobs_collection.insert_one(job)
                logger.info(f"Saved job with ID: {job_id} to expired3821jobs collection")

                # Delete the job from the jobs collection using job_id
                jobs_collection.delete_one({"job_id": job_id})
                logger.info(f"Deleted job with ID: {job_id} from jobs collection")

                # Delete the corresponding embedding from Pinecone index
                try:
                    index.delete(ids=[str(job_id)])  # Convert job_id to string for Pinecone deletion
                    logger.info(f"Deleted embedding for job with ID: {job_id} from Pinecone index")
                except Exception as e:
                    logger.error(f"Error deleting job {job_id} from Pinecone: {e}. Job may not exist in Pinecone.")

                deleted_count += 1
            
            except Exception as e:
                logger.error(f"Error processing job ID {job_id}: {e}. Skipping to the next job.")

    logger.info(f"Old jobs cleanup completed. Deleted {deleted_count} jobs.")

if __name__ == "__main__":
    delete_old_jobs()
