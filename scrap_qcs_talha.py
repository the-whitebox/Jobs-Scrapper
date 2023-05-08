import undetected_chromedriver as uc 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

download_dir = "/home/whitebox/job_scrapper/reports/policies"
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
        print('pdf downloading.........')
        download_as_pdf.click()

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

def policy_center_covid19():
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=["189","190","191","192"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(20)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
            dropdown_menu = WebDriverWait(row, 40).until(
            EC.element_to_be_clickable((By.ID, "dropdownMenu1"))
            )
            
    # click the dropdown menu to open it
            #dropdown_menu.click()
            #print(dropdown_menu.get_attribute('innerHTML'))
            action=ActionChains(driver)
            action.move_to_element(dropdown_menu)
            action.click(dropdown_menu)
            
            driver.implicitly_wait(40)
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
            time.sleep(50)
    print(" Covid policy center batch completed Batch comleted ---------------------")

def policy_center_managers():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-50")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["227","231"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("policy center manager batch completed-------------------- ")

def policy_center_admin():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-2")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["7","9","10","47","210"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("policy center admin batch completed-------------------- ")

def policy_center_care_management():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-3")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["12"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
            driver.implicitly_wait(20)
            download_as_pdf = WebDriverWait(row, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "downloadAsPdf"))
            )
            print('accessing drop down menue..........')
            print(type(dropdown_menu))
            print(dropdown_menu.get_attribute('innerHTML'))

            action.move_to_element(download_as_pdf)
            driver.implicitly_wait(40)
            action.click(download_as_pdf)
            
            action.perform()
            time.sleep(30)
        print("policy center manager batch completed-------------------- ")
def policy_center_personal_planning():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-36")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["167","168","170","171","172","173","174","175"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("policy center personal planning batch completed-------------------- ")
def policy_center_health_and_saftey():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-5")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["24","25","165","166"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("policy center health and safety batch completed-------------------- ")
def policy_center_support_service():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-25")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["22","23","37"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("policy center manager batch completed-------------------- ")
def policy_center_human_resource():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-10")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["28","29","30","31","32","33","34","99","211"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("policy center manager batch completed-------------------- ")
def policy_center_quality_insurance():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-18")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["38","39","44","194"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("Quality Assurance batch completd batch completed-------------------- ")
def policy_center_madication_management():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-31")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["13"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("Quality Assurance batch completd batch completed-------------------- ")

def policy_center_Data_protection():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-33")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["132","131","130"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("Data Protection batch completd batch completed-------------------- ")
def policy_center_advice_and_support():
    driver.implicitly_wait(10)
    driver.get("https://app.qcs.co.uk/policy-centre/my-policies")
    time.sleep(2)
    tab_list=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    upper_tab=WebDriverWait(tab_list,20).until(EC.presence_of_element_located((By.ID,"policy-tab-51")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["240"]
    for tab in tab_list:
        new_tab=str("category"+"-"+"tab"+"-"+tab)
        type(new_tab)
        print(new_tab)
        new_tab_sc=str("sc"+"-"+tab)
        tab=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab)))
        #tab[0].click()
        tab.click()
        driver.implicitly_wait(5)
        navebar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,new_tab_sc)))
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
        print("Data Protection batch completd batch completed-------------------- ")
def complaince_stackholder_surveys():
    driver.get("https://app.qcs.co.uk/compliance-tools/stakeholder-surveys")
    time.sleep(2)

    # wait for the table to load

    table = WebDriverWait(driver, 10).until(
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
        print(" batch completd batch completed-------------------- ")

#policy_reports()
#my_company_reports()
#policy_center_covid19()
#time.sleep(10)
#policy_center_managers()
#policy_center_admin()
#complaince_stackholder_surveys()
#policy_center_care_management()
policy_center_personal_planning()

driver.implicitly_wait(20)
driver.close()