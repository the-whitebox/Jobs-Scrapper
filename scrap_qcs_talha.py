import undetected_chromedriver as uc 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

download_dir = "/home/whitebox/job_scrapper"
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


def policy_reports():
    driver.get("https://app.qcs.co.uk/policy-centre/latest-updates#month")
    time.sleep(2)

    # wait for the table to load

    table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "content-month"))
    )

    if table:
        print("list found....")
        print(type(table))
    


    # find all the rows in the table
    rows = table.find_elements(By.TAG_NAME, "tr")
    if rows:
        print(type(rows))
        print(len(rows))


    # loop through each row and download the PDFs
    for row in rows:
    
        # find the dropdown menu element by id
        dropdown_menu = WebDriverWait(row, 10).until(
            EC.presence_of_element_located((By.ID, "dropdownMenu1"))
        )
        print('accessing drop down menue..........')

    # click the dropdown menu to open it
        dropdown_menu.click()

    # find the "Download as PDF" menu item by class name and click it
        download_as_pdf = WebDriverWait(row, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "downloadAsPdf"))
        )
        print('pdf downloading.........')
        download_as_pdf.click()

    
        time.sleep(2)
        driver.implicitly_wait(30)


def my_company_reports():
    driver.get("https://app.qcs.co.uk/group-dashboard/most-viewed-policies?isGroup=False")
    time.sleep(2)

    # wait for the table to load

    table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "list"))
    )

    if table:
        print("list found....")
        print(type(table))
    


    # find all the rows in the table

    rows = table.find_elements(By.TAG_NAME, "tr")
    if rows:
        print(type(rows))
        print(len(rows))


    # loop through each row and download the PDFs
    
    for row in rows:
    
        # find the dropdown menu element by id
        dropdown_menu = WebDriverWait(row, 30).until(
            EC.presence_of_element_located((By.ID, "dropdownMenu1"))
        )
        print('accessing drop down menue..........')

    # click the dropdown menu to open it
        dropdown_menu.click()

    # find the "Download as PDF" menu item by class name and click it
        download_as_pdf = WebDriverWait(row, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "downloadAsPdf"))
        )
        print('pdf downloading.........',count)
        download_as_pdf.click()

    
        time.sleep(40)
        count=count+1
        # driver.implicitly_wait(30)


def policy_center():
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"category-tab-189")))
    #tab[0].click()
    tab.click()
    driver.implicitly_wait(5)
    navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"sc-189")))
    print(type(navebar))

    
        
    #print(bar.get_attribute('innerHTML'))
    table = WebDriverWait(navebar, 10).until(
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
        EC.presence_of_element_located((By.CLASS_NAME, "more"))
        )
        print('accessing drop down menue..........')
        print(type(dropdown_menu))
        print(dropdown_menu.get_attribute('innerHTML'))

# click the dropdown menu to open it
        dropdown_menu.click()
        #print(dropdown_menu.get_attribute('innerHTML'))
        driver.implicitly_wait(10)

# find the "Download as PDF" menu item by class name and click it
        download_as_pdf = WebDriverWait(row, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "downloadAsWord"))
        )
        print("pdf downloading......")
        download_as_pdf.click()
        driver.implicitly_wait(10)


    #driver.implicitly_wait(30)

        
    
        
    # tabs=driver.find_elements(By.XPATH,"//*[@href]")
    # for html in tabs:
    #     print(html.get_attribute('innerHTML'))
    
#my_company_reports()
policy_center()

driver.close()