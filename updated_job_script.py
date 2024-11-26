import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

logger = logging.getLogger()

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
            'details': '',
            'job_post_time':''
        }

def convert_to_timestamp_with_dateutil(relative_time: str) -> str:
    now = datetime.now(timezone.utc)  # Get current UTC time

    # Remove "ago" from the string if it exists
    relative_time = relative_time.replace("ago", "").strip()
    words = relative_time.split()

    if len(words) != 2:
        raise ValueError("Invalid relative time format. Expected format: '<number> <unit>'")

    amount = int(words[0])
    unit = words[1]

    if unit.startswith("hour"):
        result = now - timedelta(hours=amount)
    elif unit.startswith("day"):
        result = now - timedelta(days=amount)
    elif unit.startswith("week"):
        result = now - timedelta(weeks=amount)
    elif unit.startswith("month"):
        result = now - relativedelta(months=amount)
    else:
        raise ValueError(f"Unsupported time unit: {unit}")
    
    # Format the result as 'YYYY-MM-DD HH:MM:SS.ssssss'
    return result.strftime('%Y-%m-%d %H:%M:%S.%f')

def job_scrapping(job_id, keyword, location):
    job_dict = temp_job_dict
    print("target_url.format(job_id) :", target_url.format(job_id))
    
    resp = requests.get(target_url.format(job_id))
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    try:
        closed_status = soup.find("span", {"class": "closed-job__icon"})
        if closed_status and "No longer accepting applications" in closed_status.text:
            logger.info(f"Skipping job: {soup.text.split()[0]} - Not accepting applications")
            return
    except Exception:
        pass

    # Extract and process job post time
    try:
        post_time_element = soup.select_one("section > div > div:nth-of-type(1) > div > h4 > div:nth-of-type(2) > span")

        if post_time_element:
            relative_time = post_time_element.get_text(strip=True)
            print("Job Post Time (Relative):", relative_time)

            try:
                job_post_time = convert_to_timestamp_with_dateutil(relative_time)
                print("Job Post Time (Timestamp):", job_post_time)

                # Convert the string job_post_time to a datetime object (aware datetime)
                job_post_datetime = datetime.strptime(job_post_time, '%Y-%m-%d %H:%M:%S.%f')
                job_post_datetime = job_post_datetime.replace(tzinfo=timezone.utc)  # Make it aware

                # Get the timestamp for 7 days ago (aware datetime)
                seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

                # Compare the two aware datetime objects
                if job_post_datetime < seven_days_ago:
                    print("Job post is older than 7 days. Skipping this job.")
                    return  # Exit the function without saving job details

                job_dict['job_post_time'] = job_post_time

            except ValueError as e:
                print("Error converting time:", e)
                return  # Exit the function if there's an issue with time conversion
        else:
            print("Post time element not found!")
            return  # Exit the function if post time is not found
    except AttributeError:
        return  # Exit the function if an error occurs while fetching post time

    # Proceed with extracting other job details if the post time is within 7 days
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
    job_dict["search_keywords"] = {"keyword": keyword, "location": location}
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
