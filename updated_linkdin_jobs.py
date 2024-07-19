import undetected_chromedriver as uc 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import logging
import pickle
import os 
import pandas as pd
from job_embed import linkedin_automate
import random
from fake_useragent import UserAgent
from selenium.webdriver.common.proxy import Proxy, ProxyType
from updated_job_script import job_scrapping
from google_sheet import query_data

# ua = UserAgent()
chrome_options = uc.ChromeOptions()
client = MongoClient("mongodb+srv://shahbazkhan6732:2orI37mNuhTtKzya@cluster0.nqxuncj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client['job_scraper']
USERNAME = "KvGRDz02ozlx8qXC"
PASSWORD = "82whP2ljuC1wf52h_streaming-1"
ENDPOINT = "pr.oxylabs.io:7777"

# proxy_options = {
#     'http': 'http://KvGRDz02ozlx8qXC:82whP2ljuC1wf52h_country-pk_city-lahore@geo.iproyal.com:12321',
#     'https': 'http://KvGRDz02ozlx8qXC:82whP2ljuC1wf52h_country-pk_city-lahore@geo.iproyal.com:12321',
# }

# proxy = Proxy()
# proxy.proxy_type = ProxyType.MANUAL
# proxy.http_proxy = proxy_options['http']
# proxy.ssl_proxy = proxy_options['https']
# proxy.add_to_capabilities(chrome_options.to_capabilities())
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-automation")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--dns-prefetch-disable")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
download_dir = "/"        
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": download_dir,
  "download.prompt_for_download": False, ## change the downpath accordingly
  "download.directory_upgrade": False,
  "safebrowsing.enabled": True,
  "download.prompt_for_download":False,
  "profile.default_content_settings.popups":False,

  })

class LinkedScrapper:
    def __init__(self, delay=5):
        if not os.path.exists("usama_data"):
            os.makedirs("usama_data")
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        self.delay = delay
        logging.info("Starting driver")
        self.linkedin_job = db["jobs"]
        self.driver = uc.Chrome(use_subprocess=True, options=chrome_options, version_main=126)

    def login(self, email, password):
        """Go to LinkedIn and login"""
        logging.info("Logging in")
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(random.uniform(4, 8))
        self.driver.find_element(By.ID, 'username').send_keys(email)
        time.sleep(random.uniform(1, 3))
        self.driver.find_element(By.ID, 'password').send_keys(password)
        time.sleep(random.uniform(1, 3))
        self.driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
        self.driver.implicitly_wait(20)
        logging.info("Logged in successfully")

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def search_linkedin(self, keywords, location):
        """Enter keywords into the search bar"""
        logging.info("Searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs/")
        search_bar = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'global-nav-search')))
        time.sleep(random.uniform(5, 10))
        search = WebDriverWait(search_bar, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'jobs-search-box__inner')))
        Search_keyword = search[0]
        Search_location = search[1]
        search_keyword = Search_keyword.find_element(By.CLASS_NAME, "jobs-search-box__text-input")
        search_location = Search_location.find_element(By.CLASS_NAME, "jobs-search-box__text-input")
        # Clear the fields using JavaScript
        self.driver.execute_script("arguments[0].value = '';", search_keyword)
        self.driver.execute_script("arguments[0].value = '';", search_location)

        search_keyword.send_keys(keywords)
        self.driver.implicitly_wait(10)
        search_location.send_keys(location)
        time.sleep(random.uniform(5, 8))
        search_location.send_keys(Keys.RETURN)
        logging.info(f'Searching for keywords: {keywords} in location: {location}')
        time.sleep(random.uniform(3, 8))


    def wait(self, t_delay=None):
        """Just easier to build this in here"""
        delay = self.delay if t_delay is None else t_delay
        time.sleep(delay)

    def scroll_to(self, job):
        """Scroll to the job element"""
        self.driver.execute_script("arguments[0].scrollIntoView();", job)
        time.sleep(random.uniform(0.5, 1.5))  # Random delay after scrolling

    def close_session(self):
        """Close the session"""
        logging.info("Closing session")
        self.driver.close()

    def load_csv(self, file):
        df = pd.read_csv(file, on_bad_lines='skip')
        data = list(df.itertuples(index=False, name=None))
        return data

    def run(self, email, password):
        # if os.path.exists("/home/whitebox/sementic_search/etl_pipelines/usama_data/cookies.txt"):
        if os.path.exists("usama_data/cookies.txt"):
            self.driver.get("https://www.linkedin.com/")
            # self.load_cookie("/home/whitebox/sementic_search/etl_pipelines/usama_data/cookies.txt")
            self.load_cookie("usama_data/cookies.txt")
            self.driver.get("https://www.linkedin.com/")
        else:
            self.login(email=email, password=password)
            # self.save_cookie("/home/whitebox/sementic_search/etl_pipelines/usama_data/cookies.txt")
            self.save_cookie("usama_data/cookies.txt")
        
        self.wait(random.uniform(10,17))
        logging.info("Begin LinkedIn keyword search")
        
        # keyword = "Python developer"
        # search_location = "United Kingdom"
        for data in query_data():
            self.search_linkedin(data[0], data[1])
            time.sleep(random.uniform(5, 10))
            jobs = self.driver.find_elements(By.CLASS_NAME,"occludable-update")
            time.sleep(random.uniform(5, 10))
            
            # getting job ids
            # pagination 
            ul_class = self.driver.find_element(By.CLASS_NAME,"artdeco-pagination__pages")
            pages = ul_class.find_elements(By.TAG_NAME, "li")
            page_no = 1
            job_no = 1
            for page in range(2, len(pages) + 1):
                job_ids = []
                for job in jobs:
                    job_id = job.get_attribute("data-occludable-job-id")
                    job_ids.append(job_id)
                # scrapping jobs
                for job_id in job_ids:
                    print(f"Data Scrapping for Job No.{job_no}, Page No.{page_no}")
                    job_dict = job_scrapping(job_id, data[0], data[1])
                    if job_dict["position"] == "":
                        continue
                    else:
                        print("data saving in data base :", job_dict["position"])
                        insertion = self.linkedin_job.update_one({'job_id': job_dict.get("job_id")}, {"$set": job_dict}, upsert=True)
                        if insertion:
                            logging.info("Data inserted in MongoDB")
                            query = self.linkedin_job.find_one({'job_id': job_dict.get("job_id")})
                            embedding_status = linkedin_automate(query)
                            if embedding_status:
                                print("Data inserted into vector store")
                            print("Data ingested for:", job_dict.get("job_id"))
                            time.sleep(random.uniform(2, 4))
                    time.sleep(random.uniform(2, 4))
                    job_no += 1
                # page changes here 
                self.driver.find_element(By.CSS_SELECTOR, f"li[data-test-pagination-page-btn='{page}']").click()
                time.sleep(15)
                page_no += 1
                
            self.driver.implicitly_wait(10)
            logging.info("Done scraping.")
            logging.info("Closing DB connection.")
            self.close_session()

if __name__ == "__main__":
    email = "usama.whitebox@gmail.com"
    password = "whitebox@"
    bot = LinkedScrapper()
    bot.run(email, password)
    time.sleep(random.uniform(5, 15))

    # Close the WebDriver 
    bot.driver.quit()
