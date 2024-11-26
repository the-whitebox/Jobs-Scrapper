import os
import time
import pickle
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from pymongo import MongoClient
from tenacity import retry, stop_after_attempt, wait_fixed
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, WebDriverException
from pymongo.errors import CursorNotFound
from pinecone import Pinecone

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MongoDB connection with exception handling
try:
    client = MongoClient("mongodb+srv://shahbazkhan6732:2orI37mNuhTtKzya@cluster0.nqxuncj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", 
                         serverSelectionTimeoutMS=20000,  # 20 seconds timeout
                         socketTimeoutMS=20000,           # 20 seconds socket timeout
                         connectTimeoutMS=30000)          # 30 seconds connection timeout
    db = client['job_scraper']
    # jobs_collection = db["jobs"]
    archived_jobs_collection = db["expired3821jobs"]
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    raise

# Pinecone API setup
try:
    os.environ['PINECONE_API_KEY'] = "74dbb1f3-abda-4c51-8c24-3e600c7796f4"
    pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index = pc.Index("whitebox")
except Exception as e:
    logging.error(f"Error setting up Pinecone: {e}")
    raise

# Chrome options
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")

class LinkedScrapper:
    def __init__(self, delay=5):
        if not os.path.exists("usama_data"):
            os.makedirs("usama_data")
        self.delay = delay
        logging.info("Starting driver")
        
        try:
            self.linkedin_job = db["jobs"]
            self.driver = uc.Chrome(use_subprocess=True, options=chrome_options, version_main=129)
        except WebDriverException as e:
            logging.error(f"Error initializing WebDriver: {e}")
            raise

    def save_cookie(self, path):
        """Save cookies after login"""
        try:
            with open(path, 'wb') as filehandler:
                pickle.dump(self.driver.get_cookies(), filehandler)
        except Exception as e:
            logging.error(f"Error saving cookies: {e}")

    def load_cookie(self, path):
        """Load cookies to bypass login"""
        try:
            with open(path, 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        except Exception as e:
            logging.error(f"Error loading cookies: {e}")

    def login_with_cookies(self, email, password):
        """Login using cookies or credentials"""
        try:
            if os.path.exists("usama_data/cookies.txt"):
                self.driver.get("https://www.linkedin.com/")
                self.load_cookie("usama_data/cookies.txt")
                time.sleep(5)
                self.driver.get("https://www.linkedin.com/")
            else:
                self.driver.get('https://www.linkedin.com/login')
                self.driver.find_element(By.ID, 'username').send_keys(email)
                time.sleep(random.uniform(1, 3))
                self.driver.find_element(By.ID, 'password').send_keys(password)
                self.driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
                time.sleep(random.uniform(4, 8))
                self.save_cookie("usama_data/cookies.txt")
            logging.info("Logged in successfully")
        except NoSuchElementException as e:
            logging.error(f"Error during login: Element not found: {e}")
            self.driver.quit()
        except Exception as e:
            logging.error(f"Error during login or loading cookies: {e}")
            self.driver.quit()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    def check_job_status(self):
        """Check job status from LinkedIn and MongoDB with retries"""
        try:
            job_records = self.linkedin_job.find({}).batch_size(100)
            for job in job_records:
                job_id = job.get("job_id")
                try:
                    self.driver.get(f"https://www.linkedin.com/jobs/view/{job_id}")
                    time.sleep(random.uniform(4, 8))

                    wait = WebDriverWait(self.driver, 10)
                    try:
                        closed_status = wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, "artdeco-inline-feedback__message"))
                        )

                        if "No longer accepting applications" in closed_status.text:
                            logging.info(f"Job {job_id}: Not accepting applications")
                            print(f"Job ID {job_id} is not accepting applications. This job will be deleted from the database.")

                            # Delete job embedding from Pinecone
                            index.delete(ids=[job_id])
                            logging.info(f"Job {job_id}: Embedding deleted from Pinecone")

                            # Delete job from MongoDB
                            self.linkedin_job.delete_one({'job_id': job_id})

                        else:
                            print(f"Job ID {job_id} is still accepting applications.")

                    except TimeoutException:
                        logging.info(f"Job {job_id}: Still accepting applications (element not found)")
                        print(f"Job ID {job_id} is still accepting applications. (No 'No longer accepting applications' message found)")

                except Exception as e:
                    logging.error(f"Error checking job ID {job_id}: {e}")
                    print(f"Error checking job ID {job_id}: {e}")

        except CursorNotFound as e:
            logging.error(f"CursorNotFound error: {e}. Restarting the job status check.")
            self.check_job_status()

    def close_session(self):
        """Close the session with exception handling"""
        try:
            logging.info("Closing session")
            self.driver.quit()
        except WebDriverException as e:
            logging.error(f"Error closing WebDriver session: {e}")

    def run(self, email, password):
        """Run the full process"""
        try:
            self.login_with_cookies(email, password)
            self.check_job_status()

            # Once all jobs are checked, log the completion
            logging.info("All jobs have been checked.")
            print("All jobs have been checked.")
        except Exception as e:
            logging.error(f"Error during bot execution: {e}")
        finally:
            self.close_session()

if __name__ == "__main__":
    email = "usama.whitebox@gmail.com"
    password = "whitebox@"

    try:
        bot = LinkedScrapper()
        bot.run(email, password)
    except Exception as e:
        logging.error(f"Critical error running the bot: {e}")

# class LinkedScrapper:
#     def __init__(self, delay=5):
#         self.delay = delay
#         logging.info("Starting driver")

#         # MongoDB setup
#         self.linkedin_job = db["jobs"]
#         try:
#             self.driver = uc.Chrome(use_subprocess=True, options=chrome_options, version_main=129)
#         except WebDriverException as e:
#             logging.error(f"Error initializing WebDriver: {e}")
#             raise
    
#     def save_cookie(self, path):
#         """Save cookies after login"""
#         try:
#             with open(path, 'wb') as filehandler:
#                 pickle.dump(self.driver.get_cookies(), filehandler)
#         except Exception as e:
#             logging.error(f"Error saving cookies: {e}")

#     def load_cookie(self, path):
#         """Load cookies to bypass login"""
#         try:
#             with open(path, 'rb') as cookiesfile:
#                 cookies = pickle.load(cookiesfile)
#                 for cookie in cookies:
#                     self.driver.add_cookie(cookie)
#         except Exception as e:
#             logging.error(f"Error loading cookies: {e}")

#     def login_with_cookies(self, email, password):
#         """Login using cookies or credentials"""
#         try:
#             if os.path.exists("usama_data/cookies.txt"):
#                 self.driver.get("https://www.linkedin.com/")
#                 self.load_cookie("usama_data/cookies.txt")
#                 time.sleep(5)
#                 self.driver.get("https://www.linkedin.com/")
#             else:
#                 self.driver.get('https://www.linkedin.com/login')
#                 self.driver.find_element(By.ID, 'username').send_keys(email)
#                 time.sleep(random.uniform(1, 3))
#                 self.driver.find_element(By.ID, 'password').send_keys(password)
#                 self.driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
#                 time.sleep(random.uniform(4, 8))
#                 self.save_cookie("usama_data/cookies.txt")
#             logging.info("Logged in successfully")
#         except NoSuchElementException as e:
#             logging.error(f"Error during login: Element not found: {e}")
#             self.driver.quit()
#         except Exception as e:
#             logging.error(f"Error during login or loading cookies: {e}")
#             self.driver.quit()

#     def save_last_processed_id(self, job_id, path="usama_data/last_processed_id.txt"):
#         """Save the last processed job ID to a file."""
#         try:
#             with open(path, 'w') as file:
#                 file.write(str(job_id))
#             logging.info(f"Saved last processed job ID: {job_id}")
#         except Exception as e:
#             logging.error(f"Error saving last processed job ID: {e}")

#     def load_last_processed_id(self, path="usama_data/last_processed_id.txt"):
#         """Load the last processed job ID from a file."""
#         try:
#             if os.path.exists(path):
#                 with open(path, 'r') as file:
#                     return int(file.read().strip())
#         except Exception as e:
#             logging.error(f"Error loading last processed job ID: {e}")
#         return None

#     def get_all_job_ids(self):
#         """Retrieve all job IDs from MongoDB and store them in a list."""
#         job_ids = []
#         try:
#             job_records = self.linkedin_job.find({}, {"job_id": 1, "_id": 0})
#             job_ids = [job['job_id'] for job in job_records]
#             logging.info(f"Retrieved {len(job_ids)} job IDs from MongoDB.")
#         except Exception as e:
#             logging.error(f"Error fetching job IDs: {e}")
#         return job_ids

#     def check_individual_job(self, job_id):
#         """Check if a specific job ID is still accepting applications."""
#         try:
#             self.driver.get(f"https://www.linkedin.com/jobs/view/{job_id}")
#             time.sleep(random.uniform(4, 8))

#             wait = WebDriverWait(self.driver, 10)
#             closed_status = wait.until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "artdeco-inline-feedback__message"))
#             )

#             if "No longer accepting applications" in closed_status.text:
#                 logging.info(f"Job {job_id}: Not accepting applications")
#                 self.archived_jobs_collection.insert_one(job_id)

#                 self.linkedin_job.delete_one({'job_id': job_id})
#                 # archived_jobs_collection.insert_one(job_data)


#                 index.delete(ids=[job_id])
#                 logging.info(f"Job {job_id}: Embedding deleted from Pinecone")
#             else:
#                 logging.info(f"Job {job_id} is still accepting applications.")

#         except TimeoutException:
#             logging.info(f"Job {job_id} is still accepting applications (element not found).")
#         except Exception as e:
#             logging.error(f"Error checking job {job_id}: {e}")
#             raise

#     def check_job_status(self):
#         """Iterate over job IDs, resuming from the next unprocessed ID if interrupted."""
#         job_ids = self.get_all_job_ids()
#         last_processed_id = self.load_last_processed_id()

#         # Find the index of the last processed ID and start from the next one
#         start_index = 0
#         if last_processed_id:
#             try:
#                 start_index = job_ids.index(last_processed_id) + 1
#             except ValueError:
#                 logging.warning(f"Last processed ID {last_processed_id} not found in job IDs list.")

#         for index, job_id in enumerate(job_ids[start_index:], start=start_index):
#             try:
#                 logging.info(f"Checking job {index + 1}/{len(job_ids)}: Job ID {job_id}")
#                 self.check_individual_job(job_id)
#                 self.save_last_processed_id(job_id)
#             except TypeError as e:
#                 logging.error(f"Error at Job ID {job_id} due to invalid document type: {e}. Skipping this job.")
#                 # Continue to the next job ID
#             except Exception as e:
#                 logging.error(f"Unexpected error at Job ID {job_id}: {e}. Resuming from this ID on retry.")
#                 break    # Exit the loop to allow a restart from the last unprocessed ID

#     def close_session(self):
#         """Close the session with exception handling."""
#         try:
#             logging.info("Closing session")
#             self.driver.quit()
#         except WebDriverException as e:
#             logging.error(f"Error closing WebDriver session: {e}")

#     def run(self, email, password):
#         """Run the entire scraping session, including login and job checks."""
#         try:
#             self.login_with_cookies(email, password)
#             self.check_job_status()
#             logging.info("All jobs have been checked.")
#         except Exception as e:
#             logging.error(f"Critical error during bot execution: {e}")
#         finally:
#             self.close_session()

# if __name__ == "__main__":
#     email = "usama.whitebox@gmail.com"
#     password = "whitebox@"

#     bot = LinkedScrapper()
#     bot.run(email, password)