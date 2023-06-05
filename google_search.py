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
import pandas as pd 
import lxml.html
import traceback
import re
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
download_dir = "/home/whitebox/job_scrapper/reports/resources"
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": download_dir,
  "download.prompt_for_download": False, ## change the downpath accordingly
  "download.directory_upgrade": False,
  "safebrowsing.enabled": True,
  "download.prompt_for_download":False,
  "profile.default_content_settings.popups":False,
  "useAutomationExtension":False,
  "disable_capture":True,
  "excludeSwitches":["enable-automation"]

  })
url = "https://linkedin-profiles-and-company-data.p.rapidapi.com/profile-details"
import requests

browser = uc.Chrome(use_subprocess=True, options=chrome_options)
browser.get('https://www.google.com')
time.sleep(10)
profile_ids=[]
def profile_finder_google(query):
    #query='doctors in london linkedin profiles'
    print(query)
    query1 = query.replace(' ','+')
    print(query1)
    n_pages=10
    a = 0
    for page in range(1, n_pages):

        path = "http://www.google.com/search?q=" + query1 + "&start=" +  str(a)
        browser.get(path)
        #search=browser.find_element(By.NAME,'q')
        # search.send_keys(query)
        # search.send_keys(Keys.RETURN)
        search_result=browser.find_element(By.ID,'search')
        links=search_result.find_elements(By.TAG_NAME,'a')
        
        print(len(links))
        for link in links:
            id=str(link.get_attribute('href'))
            print(id)
            if "linkedin.com/in/" in id:
                profile_name=re.search(r"(?<=/in/).*?(?=$)",str(id))
                print(profile_name)
                #if profile_name is not None:
            

                profile_id = str(profile_name.group(0))
                
                profile_ids.append(profile_id)
            else:
                pass
                
        a = a + 10
    return profile_ids
query = "doctors in london linkedin profiles"
get_ids=profile_finder_google(query)
print(get_ids)
for id in get_ids:
    print(type(id))
    payload = {
        "profile_id": id,
        "profile_type": "personal",
        "contact_info": False,
        "recommendations": False,
        "related_profiles": False
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "875ab400c6msh860842639ef4a3bp15418djsn8b421257c7a3",
        "X-RapidAPI-Host": "linkedin-profiles-and-company-data.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response:
        print("data retrieved")
        time.sleep(10)
    else:
        pass
    print(response.json())