import undetected_chromedriver as uc 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

download_dir = "/home/whitebox/job_scrapper/reports/policies/stackholder_surveys"
# download_path="/Users/DELL/Desktop/reports"

chrome_options = uc.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")

chrome_options.add_experimental_option("prefs", {
  "download.default_directory": download_dir,
  "download.prompt_for_download": False, ## change the downpath accordingly
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True,
  "download.prompt_for_download":False,
  "profile.default_content_settings.popups":False
  })
driver = uc.Chrome(use_subprocess=True, options=chrome_options) 
driver.get("https://app.qcs.co.uk/account/login")

uname = driver.find_element(By.ID, "Username") 
uname.send_keys("colin.rawlinson178") 
password = driver.find_element(By.ID, "Password") 
password.send_keys("Lisaco563!")
driver.find_element(By.ID, "LoginButton").click()
time.sleep(2)
def complaince_stackholder_surveys():
    driver.get("https://app.qcs.co.uk/compliance-tools/stakeholder-surveys")
    driver.implicitly_wait(10)

    # wait for the table to load
    board=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "all-categories-data"))
        )
    table = WebDriverWait(board, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list"))
        )

    if table:
        print("list found....")
        print(type(table))
    rows = table.find_elements(By.TAG_NAME, "tr")
    if rows:
        print(type(rows))
        print(len(rows))
    for row in rows:

    # find the dropdown menu element by id
        dropdown_menu = WebDriverWait(row, 20).until(
        EC.element_to_be_clickable((By.ID, "dropdownMenu1"))
        )
        
# click the dropdown menu to open it
        #dropdown_menu.click()
        #print(dropdown_menu.get_attribute('innerHTML'))
        action=ActionChains(driver)
        action.move_to_element(dropdown_menu)
        action.click(dropdown_menu)
        
        driver.implicitly_wait(20)
        action.perform()
        download_as_doc = WebDriverWait(row, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "downloadAsPdf"))
        )
        print('accessing drop down menue..........')
        print(type(dropdown_menu))
        print(dropdown_menu.get_attribute('innerHTML'))

        action.move_to_element(download_as_doc)
        driver.implicitly_wait(40)
        action.click(download_as_doc)
        
        action.perform()
        time.sleep(30)
    
    print("Covid policy center batch completed Batch comleted ---------------------")

complaince_stackholder_surveys()