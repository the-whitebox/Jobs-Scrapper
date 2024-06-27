import undetected_chromedriver as uc 
from selenium.common.exceptions import TimeoutException
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import logging
import pickle
import os 
from datetime import datetime
import pandas as pd
import re
from job_embed import linkedin_automate
import traceback
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv('MONGO_URI')

chrome_options = uc.ChromeOptions()
client = MongoClient(mongo_uri)

db=client['job_scraper']

proxy_options = {
    'proxy': {
        'http': 'http://KvGRDz02ozlx8qXC:82whP2ljuC1wf52h_country-pk_city-lahore@geo.iproyal.com:12321',
        'https': 'http://KvGRDz02ozlx8qXC:82whP2ljuC1wf52h_country-pk_city-lahore@geo.iproyal.com:12321',
    }
}
# chrome_options.add_argument("--headless")
# chrome_options.add_argument(f'--user-agent={user_agent}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')
download_dir = "/home/whitebox/job_scrapper/reports/resources"
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
        self.delay=delay
        logging.info("Starting driver")
        self.linkedin_job=db["jobs"]
        self.driver = uc.Chrome(use_subprocess=True, options=chrome_options,version_main=124)

    def login(self, email, password):
        """Go to linkedin and login"""
        # go to linkedin:
        logging.info("Logging in")
        self.driver.get('https://www.linkedin.com/login')        
        time.sleep(20)
        time.sleep(self.delay)

        self.driver.find_element(By.ID,'username').send_keys(email)
        self.driver.find_element(By.ID,'password').send_keys(password)
        self.driver.find_element(By.ID,'password').send_keys(Keys.RETURN)
        self.driver.implicitly_wait(10)
        logging.info("logedin successfully..........")
    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def search_linkedin(self, keywords, location):
        print("--------------------------------")
        """Enter keywords into search bar
        """
        logging.info("Searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs")
        time.sleep(30)
        search_bar=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,'global-nav-search')))
        
        time.sleep(self.delay)
        search=WebDriverWait(search_bar,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'jobs-search-box__inner')))
        print(len(search))
        Search_keyword=search[0]
        Search_location=search[1]
        search_keyword=Search_keyword.find_element(By.CLASS_NAME,"jobs-search-box__text-input")
        search_location=Search_location.find_element(By.CLASS_NAME,"jobs-search-box__text-input")
        search_keyword.send_keys(keywords)
        self.driver.implicitly_wait(10)
        time.sleep(3)
        search_location.send_keys(location)
        time.sleep(self.delay)
        search_location.send_keys(Keys.RETURN)
        logging.info(f'Keyword find: {keywords}: {location}')
        time.sleep(self.delay)
    
    def wait(self, t_delay=None):
        """Just easier to build this in here.
        Parameters
        ----------
        t_delay [optional] : int
            seconds to wait.
        """
        delay = self.delay if t_delay == None else t_delay
        time.sleep(delay)

    def scroll_to(self, job_list_item):
        """Just a function that will scroll to the list item in the column 
        """
        print("------------------------------",job_list_item)
        self.driver.execute_script("arguments[0].scrollIntoView();", job_list_item)
        job_list_item.click()
        time.sleep(self.delay)
    
    def get_position_data(self, job):
        """Gets the position data for a posting.
        Parameters
        ----------
        job : Selenium webelement
        Returns
        -------

        """
        
        
        ''''Get job id and and link'''
        try:
            link=job.find_element(By.TAG_NAME,'a')
            job_link=str(link.get_attribute('href'))
            print(job_link)
            Job_id=re.search(r"(?<=/view/).*?(?=/)",str(job_link))
            job_id = str(Job_id.group(0))
        except:
                job_id=""
        
        job_link=f'https://www.linkedin.com/jobs/view/{job_id}/'
        raw_details = self.driver.find_element(By.ID,"job-details").text
        details=' '.join(raw_details.splitlines())
        
        try:
            job_details_div=self.driver.find_element(By.CLASS_NAME,"job-details-jobs-unified-top-card__container--two-pane") 
            Company_address=job_details_div.find_element(By.CLASS_NAME,'app-aware-link')
            company_address=str(Company_address.get_attribute('href'))
            print("company_address :",company_address)
        except:
            company_address=""
        try:
            hiring_person=self.driver.find_element(By.CLASS_NAME,"hirer-card__container")
            hiring_person_profile=hiring_person.find_element(By.TAG_NAME,'a')
            hiring_person_link=str(hiring_person_profile.get_attribute('href'))
            hiring_person_name=hiring_person.text.split('\n')[0]
            print('hiring person linked_id:',hiring_person_link)
            print('hiring person name:',hiring_person_name)
        except:
            hiring_person_link=""
            hiring_person_name=""

        try:
            position=job.text.split('\n')[0]
            print("Position : " ,position)
        except:
            position=""
        try: 
            company=job.text.split('\n')[2]
        except:
            company=""
        try:
            location=job.text.split('\n')[2]
        except:
            location=""
        
        try:
            other_information=job.text.split('\n')[3:]
        except:
            other_information=""
        
        return [position,location,company,company_address,hiring_person_name,hiring_person_link,job_id,details,other_information,job_link]
        

    def wait_for_element_ready(self, by, text):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, text)))
        except TimeoutException:
            logging.debug("wait_for_element_ready TimeoutException")
            pass

    def close_session(self):
        """This function closes the actual session"""
        logging.info("Closing session")
        self.driver.close()
    def load_csv(self,file):
        df= pd.read_csv(file,on_bad_lines='skip')
        data=list(df.itertuples(index=False, name=None))
        return data

    def run(self, email, password):
        if os.path.exists("/home/whitebox/sementic_search/etl_pipelines/usama_data/cookies.txt"):
            self.driver.get("https://www.linkedin.com/")
            
            self.load_cookie("/home/whitebox/sementic_search/etl_pipelines/usama_data/cookies.txt")
            self.driver.get("https://www.linkedin.com/")
        else:
            self.login(
                email=email,
                password=password
            )
            self.save_cookie("/home/whitebox/sementic_search/etl_pipelines/usama_data/cookies.txt")
        self.wait(50)
        logging.info("Begin linkedin keyword search")
        keyword = "ASNT"
        location = "Worldwide"
        self.search_linkedin(keyword, location)
        time.sleep(5)
        try: 
            jobs = self.driver.find_elements(By.CLASS_NAME,"occludable-update")
            print('------------------------total number of jobs found------------',len(jobs))
            self.wait()
            time.sleep(5)
            
            for job in jobs:
                no_of_jobs=len(jobs)
                job_dict={}                
                if len(jobs)!=0:
                    self.scroll_to(job)
                    position_data_list=self.get_position_data(job)
                    print("----------------------------------list of final information------------------------")
                    search_keywords={'keyword':keyword,'location':location}
                    print("Position data List", position_data_list)
                    job_dict["position"]=position_data_list[0]
                    job_dict["location"]=position_data_list[1]
                    job_dict["company"]=position_data_list[2]
                    job_dict["company_address"]=position_data_list[3]
                    job_dict["hiring_person"]=position_data_list[4]
                    job_dict["hiring_person_linkedin_link"]=position_data_list[5]
                    job_dict["job_id"]=position_data_list[6]
                    
                    job_dict["time_stamp"]=str(datetime.now())
                    job_dict["job_source"]="linkedin"
                    job_dict["search_keywords"]=search_keywords
                    job_dict["details"]=position_data_list[7]
                    job_dict["other_information"]= position_data_list[8]
                    job_dict["job_details_link"]=position_data_list[9]
                    job_dict["job_status"]="active"

                    insertion=self.linkedin_job.update_one({'job_id':job_dict.get("job_id")},{"$set":job_dict},upsert=True)
                    if insertion:
                        logging.info("Data inserted in mongo db")
                        query=self.linkedin_job.find_one({'job_id':job_dict.get("job_id")})
                        embedding_status=linkedin_automate(query)
                        if embedding_status:
                            print("data inserted into vector store")
                        print("Data Ingested for:",job_dict.get("job_id"))

                        self.wait()
                        self.driver.implicitly_wait(5)
                    job.click()
                    no_of_jobs=no_of_jobs-1
                time.sleep(5)
                self.wait()
                
        except Exception as e:
            print(traceback.format_exc())
            pass
                            
        self.driver.implicitly_wait(10)
           
        logging.info("Done scraping.")
        logging.info("Closing DB connection.")
        self.close_session()
        


if __name__ == "__main__":
    email = "usama.whitebox@gmail.com"
    password = "whitebox@"
    bot = LinkedScrapper()
    
    bot.run(email, password)
    time.sleep(10)
            
        




    
