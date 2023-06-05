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
browser = uc.Chrome(use_subprocess=True, options=chrome_options)

browser.get('https://www.linkedin.com/login')
time.sleep(10)

email='drhussaintariq123@gmail.com'
password='whitebox@'
browser.find_element(By.ID,'username').send_keys(email)
browser.find_element(By.ID,'password').send_keys(password)

browser.find_element(By.ID,'password').send_keys(Keys.RETURN)

browser.implicitly_wait(25)

print('--------------------loggedin-------------------')

info = []

links = [#'https://www.linkedin.com/in/talhayasirusmani0/',
         'https://www.linkedin.com/in/talha-tariq-chaudhry/',
        # 'https://www.linkedin.com/in/asher-muneer/',
        #'https://www.linkedin.com/in/zirvazahid/'
        ]

for link in links:
    browser.get(link)
    browser.implicitly_wait(5)
    def scroll_down_page(speed=20):
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = browser.execute_script("return document.body.scrollHeight")

    #scroll_down_page(speed=20)

    src = browser.page_source
    soup = BeautifulSoup(src, 'html.parser')

    # Get Name of the person
    try:
        #name_div = soup.find('div', {'class': 'pv-text-details__left-panel mr5'})
        name_div=browser.find_element(By.CLASS_NAME,'pv-text-details__left-panel')
        print(name_div.get_attribute('innerHTML'))
        name=name_div.text.split('\n')[0]
        title=name_div.text.split('\n')[1]
        #title=name_div.text.split('\n')[1:]

        print('first name',name)
        print('second name',title)


        # print("==================================================",name_div.text)
        # first_last_name_div = name_div.find_element(By.TAG_NAME,'h1')
        # #print(first_last_name_div.get_attribute('innerHTML'))
        # first_last_name=first_last_name_div.text
        # time.sleep(5)
        
    except Exception as e:
        first_last_name = None
        print(e)
    #print('person name -------------',first_last_name)
    ''' Get person title '''
    # try:
    #   #//*[@id="ember2894"]/div[2]/div[2]/div[1]/div[2]
      
    #   #title_element_div= WebDriverWait(name_div,5).until(EC.presence_of_element_located((By.CLASS_NAME,'text-body-medium break-words')))
    #   title_element_div=name_div.find_element(By.CLASS_NAME,'text-body-medium break-words')
    #   print('title html---',title_element_div.get_attribute('innerHTML'))
    #   title=title_element_div.text
    # except Exception as e:
    #   print('Exception raised while getting title',e)
    #   title=None

    # print(title)
    '''Get the person location'''
    # try:
    #   #location_div=browser.find_element(By.CLASS_NAME,'pv-text-details__left-panel mt2')
    #   location_div=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'text-body-small inline t-black--light break-words')))
    #   print('location html',location_div.get_attribute('innerHTML'))
    #   location=location_div.text
    #   print(location)
    # except Exception as e:
    #     location=None
    #     print("Exception in getting location",e)
    ''' get the persons organizations '''
    organization=[]
    try:
        
        organizations_div=browser.find_element(By.CLASS_NAME,'pv-text-details__right-panel')
        organizations_list=organizations_div.find_elements(By.TAG_NAME,'li')
        for organizations in organizations_list:
            organizations.get_attribute('innerHTML')
            organization.append(organizations.text)
    except Exception as e:
        print("Exceptions raise while getting experience",e)
        organization=None
    print(organization)


    ''' Get the experience of the person''' 
    # Get Talks about section info
    try:
        get_section=WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.TAG_NAME,'section')))
        for section in get_section:
            heading=section.find_element(By.CLASS_NAME,'h2')
            if heading.text=="Experience":
                print("experience section found")
        exp_list=[]
        company_dict={}
        #browser.execute_script("window.ScrollTo(0,500)")
        # //*[@id="ember6654"]/div[3]
        # //*[@id="ember6876"]/div[3]
        #//*[@id="ember6876"]/div[3]
        #//*[@id="ember7251"]/div[3]
        experience_div=WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'pvs-list')))
        for each_exp in experience_div:
            experience_list=WebDriverWait(each_exp,10).until(EC.presence_of_all_elements_located((By.TAG_NAME,'li')))
            print('experience list',len(experience_list))
            for experience in experience_list:
                job_positions=WebDriverWait(experience,10).until(EC.presence_of_all_elements_located((By.TAG_NAME,'li')))
                print(len(job_positions))
                for desc in job_positions:
                    print('-------------------------------------',desc.text)
                
                # company_positions=experience.find_elements(By.TAG_NAME,"li")
            # print(len(company_positions))
            # for posts in company_positions:
            #     print(posts.get_attribute('innerHTML'))


            #print('text----------------',experience.text)

            #print(experience.get_attribute('innerHTML'))

            
            

    except Exception as e:
        traceback.print_exc()
        print("Exception raised while accessing experience block",e)


        

        


#     try:
#         talksAbout_tag = name_div.find('div', {'class': 'text-body-small t-black--light break-words pt1'})
#         talksAbout = talksAbout_tag.find('span').get_text().strip()
#     except:
#         talksAbout = None
    
#     # Get Location of the Person
#     try:
#         location_tag = name_div.find('div', {'class': 'pb2'})
#         location = location_tag.find('span').get_text().strip()
#     except:
#         location = None
    
#     # Get Title of the Person
#     try:
#         title = name_div.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
#     except:
#         title = None
    
#     # Get Company Link of the Person
#     try:
#         exp_section = soup.find('section', {'id':'experience-section'})
#         exp_section = exp_section.find('ul')
#         li_tags = exp_section.find('div')
#         a_tags = li_tags.find('a')

#         company_link = a_tags['href']
#         company_link = 'https://www.linkedin.com/' + company_link
#     except:
#         company_link = None

#     # Get Job Title of the Person
#     try:
#         job_title = li_tags.find('h3', {'class': 't-16 t-black t-bold'}).get_text().strip()
#     except:
#         job_title = None
    
#     # Get Company Name of the Person
#     try:
#         company_name = li_tags.find('p', {'class': 'pv-entity__secondary-title t-14 t-black t-normal'}).get_text().strip()
#     except:
#         company_name = None

#     contact_page = link + 'detail/contact-info/'
#     browser.get(contact_page)
#     browser.implicitly_wait(1)

#     contact_card = browser.page_source
#     contact_page = BeautifulSoup(contact_card, 'lxml')
#     # Get Linkdin Profile Link and Contact details of the Person
#     try:
#         contact_details = contact_page.find('section', {'class': 'pv-profile-section pv-contact-info artdeco-container-card ember-view'})
#         contacts = []
#         for a in contact_details.find_all('a', href=True):
#             contacts.append(a['href'])
#     except:
#         contacts.append('')
#     info.append([first_last_name, title, company_link, job_title, company_name, talksAbout, location, contacts])
#     print('-------------------person info-------------------',info)
#     time.sleep(5)


# column_names = ["Full Name", "Title", "Company URl", 'Job Title', 
#                 'Company Name', 'Talks About', 'Location', 'Profile Link and Contact']
# df = pd.DataFrame(info, columns=column_names)
# df.to_csv('data.csv', index=False)

print(".................Done Scraping!.................")
browser.quit()

