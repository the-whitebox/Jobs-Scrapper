import undetected_chromedriver as uc 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import logging
import pickle
import os 
from datetime import datetime
chrome_options = uc.ChromeOptions()
client=MongoClient("mongodb+srv://talhayasir:123fightfight@whiteboxscrapper.f0zx0xd.mongodb.net/?retryWrites=true&w=majority")
db=client['job_scraper']
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
download_dir = "/home/whitebox/job_scrapper/reports/resources"
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": download_dir,
  "download.prompt_for_download": False, ## change the downpath accordingly
  "download.directory_upgrade": False,
  "safebrowsing.enabled": True,
  "download.prompt_for_download":False,
  "profile.default_content_settings.popups":False
  })
#driver = uc.Chrome(use_subprocess=True, options=chrome_options) 


class LinkedScrapper:
    def __init__(self, delay=5):
        if not os.path.exists("data"):
            os.makedirs("data")
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        self.delay=delay
        logging.info("Starting driver")
        self.linkedin_job=db["jobs"]
        self.driver = uc.Chrome(use_subprocess=True, options=chrome_options)

    def login(self, email, password):
        """Go to linkedin and login"""
        # go to linkedin:
        logging.info("Logging in")
        #self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(self.delay)

        self.driver.find_element(By.ID,'username').send_keys(email)
        self.driver.find_element(By.ID,'password').send_keys(password)

        self.driver.find_element(By.ID,'password').send_keys(Keys.RETURN)
        self.driver.implicitly_wait(10)

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def search_linkedin(self, keywords, location):
        """Enter keywords into search bar
        """
        logging.info("Searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs")
        # search based on keywords and location and hit enter
        
        search_bar=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,'global-nav-search')))
        
        time.sleep(self.delay)
        
        # Search_keywords=WebDriverWait(search_bar,10).until(EC.presence_of_element_located((By.CLASS_NAME,'jobs-search-box__text-input')))

        # self.driver.implicitly_wait(10)
        # # Search_keywords=search_keywords[0]
        # Search_keywords.send_keys(keywords)
        # time.sleep(3)
        # search_location_bar=WebDriverWait(search_bar,10).until(EC.presence_of_element_located((By.ID,'location-typeahead-instance-ember238')))
        # search_location = WebDriverWait(search_location_bar,10).until(EC.presence_of_element_located((By.CLASS_NAME,'jobs-search-box__text-input')))
       
        search=WebDriverWait(search_bar,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'jobs-search-box__inner')))
        print(len(search))
        Search_keyword=search[0]
        print("keyword---------------------------------")
        Search_keyword.get_attribute('innerHTML')
        Search_location=search[1]
        Search_location.get_attribute('innerHTML')
        print("location---------------------------------")
        search_keyword=Search_keyword.find_element(By.CLASS_NAME,"jobs-search-box__text-input")
        search_location=Search_location.find_element(By.CLASS_NAME,"jobs-search-box__text-input")
        search_keyword.send_keys(keywords)
        
        self.driver.implicitly_wait(10)
        #search_location.click()
        time.sleep(3)
        search_location.send_keys(location)
        time.sleep(self.delay)
        search_location.send_keys(Keys.RETURN)
        logging.info("Keyword search successful")
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
        list of strings : [position, company, location, details]

        """
        
        
        
        
        print("------------------------------------------------------------------")
        print(job.get_attribute('innerHTML'))
        print("------------------------------------------------------------------")

        print('--------------------------------job_text--------------',job.text)
        raw_details = self.driver.find_element(By.ID,"job-details").text
        details=' '.join(raw_details.splitlines())
        posted_date=self.driver.find_element(By.CLASS_NAME,"jobs-unified-top-card__posted-date").text
        print(posted_date)

        # print("**************************************")
        # print(details)
        # # print("**************************************")
        # try:

        #[position, company, location] = job.text.split('\n')[:3]
        #     return [position, company, location, details]
        # except:
        #     [position, company, location, job_type] = job.text.split('\n')[:4]
        # raw_job_dec=job.text
        # job_des=list(','.join(raw_job_dec.splitline()))
        # print(len(list))
        try:
            position=job.text.split('\n')[0]
        except:
            position=""
        try: 
            company=job.text.split('\n')[1]
        except:
            company=""
        try:
            location=job.text.split('\n')[2]
        except:
            location=""
        try:
            job_type=job.text.split('\n')[3]
        except:
            job_type=""
        return [position, company, location,job_type,posted_date, details]
        

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

    def run(self, email, password, keywords, location):
        if os.path.exists("data/cookies.txt"):
            self.driver.get("https://www.linkedin.com/")
            
            self.load_cookie("data/cookies.txt")
            self.driver.get("https://www.linkedin.com/")
        else:
            self.login(
                email=email,
                password=password
            )
            self.save_cookie("data/cookies.txt")

        logging.info("Begin linkedin keyword search")
        self.search_linkedin(keywords, location)
        self.wait()

        # scrape pages,only do first 8 pages since after that the data isn't 
        # well suited for me anyways:  
        for page in range(2, 40):
            # get the jobs list items to scroll through:
            jobs = self.driver.find_elements(By.CLASS_NAME,"occludable-update")
            self.wait()
            time.sleep(10)
            for job in jobs:
                print("-------------------------------------------------------------")
                #job.text()
                print("---------------------------------------------------------------")
                job_dict={}
                search_keywords={'keyword':keywords,'location':location}
                self.scroll_to(job)
                position_data_list=self.get_position_data(job)

                # if len(position_data_list)==4:
                #     [position, company, location,job_type,details] = self.get_position_data(job)
                #     job_dict["job_type"]=job_type
                # else:
                #     [position, company, location,details] = self.get_position_data(job)

                #print(position,company,location,details)
                # do something with the data...
                
                job_dict["position"]=position_data_list[0]
                job_dict["company"]=position_data_list[1]
                job_dict["location"]=position_data_list[2]
                job_dict["search_keyword"]=search_keywords
                job_dict["job_type"]=position_data_list[3]
                job_dict["posted_date"]=position_data_list[4]
                job_dict["details"]=position_data_list[5]
                
                job_dict["time_stamp"]=str(datetime.now())
                job_dict["job_source"]="linkedin"

                #print(job_dict)
                insertion=self.linkedin_job.insert_one(job_dict)
                if insertion:
                    print("data inserted..............................................")
                    print(job_dict)
                    self.wait()
                    self.driver.implicitly_wait(10)
                job.click()

            
           
            
            #self.driver.find_element(By.XPATH,f"//button[@aria-label='Page {page}']").click()
            self.wait()
            
            self.driver.implicitly_wait(10)
        logging.info("Done scraping.")
        logging.info("Closing DB connection.")
        self.close_session()


if __name__ == "__main__":
    email = "talha.yasirusmani@gmail.com"
    password = "123fightfight"
    bot = LinkedScrapper()
    bot.run(email, password, "Pharmacist", "london")




    
