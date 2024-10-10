import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime


target_url = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}"
job_data = []
temp_job_dict = {'job_id': '',
            'company': '', 
            'position': '',
            'company_address': '', 
            'hiring_person': '',
            'hiring_person_linkedin_link': '', 
            'job_details_link': '',
            'job_source': 'linkedin',
            'job_status': 'active',
            'time_stamp': '',
            'location': '',
            'details': ''
        }
def job_scrapping(job_id, keyword, location):
    job_dict = temp_job_dict
    print("target_url.format(job_id) :", target_url.format(job_id))
    
    resp = requests.get(target_url.format(job_id))
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    job_dict["job_id"] = job_id
    
    try:
        job_dict["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
    except AttributeError:
        job_dict["company"] = ""
    
    try:
        job_dict["position"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
    except AttributeError:
        job_dict["position"] = ""
    
    try:
        job_dict["company_address"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").get("href")
    except AttributeError:
        job_dict["company_address"] = ""
    
    try:
        hiring_person = soup.find("a", {"class": "base-card__full-link"}).get_text()
        job_dict["hiring_person"] = ' '.join(hiring_person.split())
    except AttributeError:
        job_dict["hiring_person"] = ""
    
    try:
        job_dict["hiring_person_linkedin_link"] = soup.find("a", {"class": "base-card__full-link"}).get("href")
    except AttributeError:
        job_dict["hiring_person_linkedin_link"] = ""
    
    try:
        job_dict["job_details_link"] = f"https://www.linkedin.com/jobs/view/{job_id}"
    except AttributeError:
        job_dict["job_details_link"] = ""
    
    job_dict["job_source"] = "linkedin"
    job_dict["job_status"] = "active"
    job_dict["search_keywords"] = {"keyword":keyword,"location":location}
    job_dict["time_stamp"] = str(datetime.now())
    
    try:
        time.sleep(2)
        location = soup.find("h4", {"class": "top-card-layout__second-subline"}).find("span", {"class": "topcard__flavor--bullet"}).get_text().strip()
        job_dict["location"] = ' '.join(location.split())
    except AttributeError:
        job_dict["location"] = ""
    try:
        time.sleep(2)
        details = soup.find("div", {"class": "description__text"}).get_text()
        job_dict["details"] = ' '.join(details.split())
    except:
        job_dict["details"] = ""

    return job_dict
