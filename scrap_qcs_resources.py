import undetected_chromedriver as uc 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

download_dir = "/home/whitebox/job_scrapper/reports/resources"
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
def resource_center_covid19():
    driver.get("https://app.qcs.co.uk/resource-centre")
    time.sleep(2)
    tab_list=["189","190","191","192"]
    #tab_list=["192"]

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
            #action.move_to_element(dropdown_menu)
            #action.click(dropdown_menu)
            
            driver.implicitly_wait(40)
            action.perform()
            download_options=row.find_elements(By.TAG_NAME,"li")
            
            print(len(download_options))
            if len(download_options)>2:
                
            
                action.move_to_element(dropdown_menu)
                action.click(dropdown_menu)

        #print("download options type is ............",type(download_options))
                download_resource = WebDriverWait(row, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "download-resource"))
                )
                if download_resource:
                    print("Download resources found............")
                
                    print('accessing drop down menue..........')
                    print(type(dropdown_menu))
                    print(dropdown_menu.get_attribute('innerHTML'))

                    action.move_to_element(download_resource)
                    driver.implicitly_wait(40)
                    action.click(download_resource)
                    
                    action.perform()
                    time.sleep(50)
            
    print(" Covid policy center batch completed Batch comleted ---------------------")
def resource_center_admin():
    driver.get("https://app.qcs.co.uk/resource-centre")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 400);")
    driver.implicitly_wait(10)
    # section=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"tabs my-policies")))
    # print("section found")
    tab_list=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    driver.implicitly_wait(10)
    upper_tab=WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"policy-tab-2")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["7","9","10","47","210"]
    #tab_list=["192"]

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
            #action.move_to_element(dropdown_menu)
            #action.click(dropdown_menu)
            
            driver.implicitly_wait(40)
            action.perform()
            download_options=row.find_elements(By.TAG_NAME,"li")
            
            print(len(download_options))
            if len(download_options)>2:
                
            
                action.move_to_element(dropdown_menu)
                action.click(dropdown_menu)

        #print("download options type is ............",type(download_options))
                download_resource = WebDriverWait(row, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "download-resource"))
                )
                if download_resource:
                    print("Download resources found............")
                
                    print('accessing drop down menue..........')
                    print(type(dropdown_menu))
                    print(dropdown_menu.get_attribute('innerHTML'))

                    action.move_to_element(download_resource)
                    driver.implicitly_wait(40)
                    action.click(download_resource)
                    
                    action.perform()
                    time.sleep(50)
            
    print(" Covid policy center batch completed Batch comleted ---------------------")
def resource_center_care_management():
    driver.get("https://app.qcs.co.uk/resource-centre")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 400);")
    driver.implicitly_wait(10)
    # section=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"tabs my-policies")))
    # print("section found")
    tab_list=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    driver.implicitly_wait(10)
    upper_tab=WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"policy-tab-3")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["12","19","129","225"]
    #tab_list=["192"]

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
            #action.move_to_element(dropdown_menu)
            #action.click(dropdown_menu)
            
            driver.implicitly_wait(40)
            action.perform()
            download_options=row.find_elements(By.TAG_NAME,"li")
            
            print(len(download_options))
            if len(download_options)>2:
                
            
                action.move_to_element(dropdown_menu)
                action.click(dropdown_menu)

        #print("download options type is ............",type(download_options))
                download_resource = WebDriverWait(row, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "download-resource"))
                )
                if download_resource:
                    print("Download resources found............")
                
                    print('accessing drop down menue..........')
                    print(type(dropdown_menu))
                    print(dropdown_menu.get_attribute('innerHTML'))

                    action.move_to_element(download_resource)
                    driver.implicitly_wait(40)
                    action.click(download_resource)
                    
                    action.perform()
                    time.sleep(50)
            
    print(" Covid policy center batch completed Batch comleted ---------------------")

def resource_center_health_and_safety():
    driver.get("https://app.qcs.co.uk/resource-centre")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 400);")
    driver.implicitly_wait(10)
    # section=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"tabs my-policies")))
    # print("section found")
    tab_list=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    driver.implicitly_wait(10)
    upper_tab=WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"policy-tab-5")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["24","25"]
    #tab_list=["192"]

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
            #action.move_to_element(dropdown_menu)
            #action.click(dropdown_menu)
            
            driver.implicitly_wait(40)
            action.perform()
            download_options=row.find_elements(By.TAG_NAME,"li")
            
            print(len(download_options))
            if len(download_options)>2:
                
            
                action.move_to_element(dropdown_menu)
                action.click(dropdown_menu)

        #print("download options type is ............",type(download_options))
                download_resource = WebDriverWait(row, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "download-resource"))
                )
                if download_resource:
                    print("Download resources found............")
                
                    print('accessing drop down menue..........')
                    print(type(dropdown_menu))
                    print(dropdown_menu.get_attribute('innerHTML'))

                    action.move_to_element(download_resource)
                    driver.implicitly_wait(40)
                    action.click(download_resource)
                    
                    action.perform()
                    time.sleep(50)
            
    print(" health and safety batch completed Batch comleted ---------------------")
def resource_center_data_protection():
    driver.get("https://app.qcs.co.uk/resource-centre")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 400);")
    driver.implicitly_wait(10)
    # section=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"tabs my-policies")))
    # print("section found")
    tab_list=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    driver.implicitly_wait(10)
    upper_tab=WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"policy-tab-33")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["132","131","130"]
    #tab_list=["192"]

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
            #action.move_to_element(dropdown_menu)
            #action.click(dropdown_menu)
            
            driver.implicitly_wait(40)
            action.perform()
            download_options=row.find_elements(By.TAG_NAME,"li")
            
            print(len(download_options))
            if len(download_options)>2:
                
            
                action.move_to_element(dropdown_menu)
                action.click(dropdown_menu)

        #print("download options type is ............",type(download_options))
                download_resource = WebDriverWait(row, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "download-resource"))
                )
                if download_resource:
                    print("Download resources found............")
                
                    print('accessing drop down menue..........')
                    print(type(dropdown_menu))
                    print(dropdown_menu.get_attribute('innerHTML'))

                    action.move_to_element(download_resource)
                    driver.implicitly_wait(40)
                    action.click(download_resource)
                    
                    action.perform()
                    time.sleep(50)
            
    print(" resource center data protection batch completed Batch comleted ---------------------")

def resource_center_human_resources():
    driver.get("https://app.qcs.co.uk/resource-centre")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 400);")
    driver.implicitly_wait(10)
    # section=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"tabs my-policies")))
    # print("section found")
    tab_list=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"owl-stage")))
    print(tab_list.get_attribute("innerHTML"))
    driver.implicitly_wait(10)
    upper_tab=WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"policy-tab-10")))
    action=ActionChains(driver)
    action.click(upper_tab)
    action.perform()
    driver.implicitly_wait(20)
    time.sleep(10)
    tab_list=["28","29","30","31","32","34","99","211"]
    #tab_list=["192"]

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
            #action.move_to_element(dropdown_menu)
            #action.click(dropdown_menu)
            
            driver.implicitly_wait(40)
            action.perform()
            download_options=row.find_elements(By.TAG_NAME,"li")
            
            print(len(download_options))
            if len(download_options)>2:
                
            
                action.move_to_element(dropdown_menu)
                action.click(dropdown_menu)

        #print("download options type is ............",type(download_options))
                download_resource = WebDriverWait(row, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "download-resource"))
                )
                if download_resource:
                    print("Download resources found............")
                
                    print('accessing drop down menue..........')
                    print(type(dropdown_menu))
                    print(dropdown_menu.get_attribute('innerHTML'))

                    action.move_to_element(download_resource)
                    driver.implicitly_wait(40)
                    action.click(download_resource)
                    
                    action.perform()
                    time.sleep(50)
            
    print(" resource center human resources batch completed Batch comleted ---------------------")

#resource_center_covid19()
#resource_center_admin()
#resource_center_care_management()
#resource_center_health_and_safety()
resource_center_human_resources()
#resource_center_data_protection()



