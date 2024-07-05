from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv

load_dotenv()

## & 'C:\Program Files\Google\Chrome\Application\Chrome.exe' --remote-debugging-port=5555

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:5555")
driver = webdriver.Chrome(options=options)


theRevSearches = []
def revSearch(keyword):
    print("Revsearching")
    print(keyword)
    keyword2 = os.getenv("keyword2")
    driver.get(f"https://www.facebook.com/search/people/?q={keyword2}")
    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=\'article\'] span a')))
        script = 'return document.querySelectorAll("[role=\'article\'] span a");'
        searches = driver.execute_script(script)
        print("Users found", len(searches))
        theRevSearches = searches
        for search in theRevSearches:
            user = search.get_attribute('href')
            print(user)
            print(checkFriends(user))
            
    except:
        return False
    

def search(keyword):
    driver.get(f"https://www.facebook.com/search/people/?q={keyword}")
    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=\'article\'] span a')))
        script = 'return document.querySelector("[role=\'article\'] span a");'
        search = driver.execute_script(script)    
        user = search.get_attribute('href')
        
        checkedFriends = checkFriends(user)
        if checkedFriends:
            print("Checked friends")
            print(checkedFriends)
        else:
            revSearch(keyword)

    except:
        return False



def checkFriends(userUrl):
    driver.get(f"{userUrl}/friends")
    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=\'link\']:not(:has(img))')))
            
        script = 'return document.querySelectorAll("[role=\'link\']:not(:has(img))");'
        friends = driver.execute_script(script)
        allFriends = []
        for friend in friends:
            if friend.text == "" or friend.text == "Vrienden" or " vrienden" in friend.text or "Foto’s" == friend.text:
                continue
            # print(f"{friend.text}")
            allFriends.append(friend.text)
        return allFriends
    except:
        return False

keyword = os.getenv("keyword")
search(keyword)
