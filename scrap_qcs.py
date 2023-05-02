import undetected_chromedriver as uc 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

download_dir = "/Users/muhammadtahir/workspace/django_projects/colin"

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
  "safebrowsing.enabled": True
  })
driver = uc.Chrome(use_subprocess=True, options=chrome_options) 
driver.get("https://app.qcs.co.uk/account/login")

uname = driver.find_element(By.ID, "Username") 
uname.send_keys("colin.rawlinson178") 
password = driver.find_element(By.ID, "Password") 
password.send_keys("Lisaco563!")
driver.find_element(By.ID, "LoginButton").click()
time.sleep(2)
driver.get("https://app.qcs.co.uk/policy-centre")
time.sleep(2)

# wait for the table to load
table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "list"))
)

# find all the rows in the table
rows = table.find_elements(By.TAG_NAME, "tr")

# loop through each row and download the PDFs
for row in rows:

    # find the dropdown menu element by id
    dropdown_menu = WebDriverWait(row, 10).until(
        EC.presence_of_element_located((By.ID, "dropdownMenu1"))
    )

    # click the dropdown menu to open it
    dropdown_menu.click()

    # find the "Download as PDF" menu item by class name and click it
    download_as_pdf = WebDriverWait(row, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "downloadAsPdf"))
    )
    download_as_pdf.click()

    
    time.sleep(2)
    driver.implicitly_wait(30)
driver.close()