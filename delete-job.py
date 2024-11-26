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
    jobs_collection = db["jobs"]
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
            self.jobs_collection = jobs_collection
            self.archived_jobs_collection = archived_jobs_collection
            self.driver = uc.Chrome(use_subprocess=True, options=chrome_options, version_main=129)
            self.last_processed_id_file = "usama_data/last_processed_id.txt"
        except WebDriverException as e:
            logging.error(f"Error initializing WebDriver: {e}")
            raise

    def save_checkpoint(self, job_id):
        """Save the last processed job ID for resuming."""
        try:
            with open(self.last_processed_id_file, 'w') as file:
                file.write(str(job_id))
        except Exception as e:
            logging.error(f"Error saving checkpoint: {e}")

    def load_checkpoint(self):
        """Load the last processed job ID to resume from."""
        if os.path.exists(self.last_processed_id_file):
            with open(self.last_processed_id_file, 'r') as file:
                return file.read().strip()
        return None

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
        job_ids = list(self.jobs_collection.find({}, {"job_id": 1, "_id": 0}))
        last_id = self.load_checkpoint()
        start_index = 0

        if last_id:
            for i, job in enumerate(job_ids):
                if job["job_id"] == last_id:
                    start_index = i + 1
                    break

        for job in job_ids[start_index:]:
            job_id = job["job_id"]
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
                        print(f"Job ID {job_id} is not accepting applications. Moving it to expired jobs.")

                        # Delete job embedding from Pinecone
                        index.delete(ids=[job_id])
                        logging.info(f"Job {job_id}: Embedding deleted from Pinecone")

                        # Move job to archived collection
                        job_data = self.jobs_collection.find_one_and_delete({'job_id': job_id})
                        self.archived_jobs_collection.insert_one(job_data)

                    else:
                        print(f"Job ID {job_id} is still accepting applications.")

                except TimeoutException:
                    logging.info(f"Job {job_id}: Still accepting applications (element not found)")

                # Save checkpoint after processing each job
                self.save_checkpoint(job_id)

            except Exception as e:
                logging.error(f"Error checking job ID {job_id}: {e}")
                self.save_checkpoint(job_id)
                break

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
