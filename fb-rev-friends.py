from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
from dotenv import load_dotenv

load_dotenv()

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:5555")
driver = webdriver.Chrome(options=options)

listOfCheckedProfiles = []

numberOfSearches = 20
numberOfFriends = 100

def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scroll_to_bottom_check_search():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        script = 'return document.querySelectorAll("[role=\'article\'] span a");'
        friends = driver.execute_script(script)
        if len(friends) > numberOfSearches:
            break
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scroll_to_bottom_check_friends():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        script = 'return document.querySelectorAll("[role=\'link\']:not(:has(img))");'
        friends = driver.execute_script(script)
        if len(friends) > numberOfFriends:
            break
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

potentialSearches = []

firstFind = True

def revSearch(keyword):
    keyword2 = os.getenv("keyword2")
    driver.get(f"https://www.facebook.com/search/people/?q={keyword2}")
    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=\'article\'] span a')))
        
        scroll_to_bottom_check_search()
        
        script = 'return document.querySelectorAll("[role=\'article\'] span a");'
        searches = driver.execute_script(script)
        
        
        print("RevSearch found other users", len(searches))
        foundList = []
        for search in searches:
            user = search.get_attribute('href')
            foundList.append(user)
        
        # print("foundList", foundList)
        
        friendOfSearch = []
        for user in foundList:
            # print("user", user)
            potentialFriend = checkFriends(user)
            if potentialFriend == False:
                continue
            global searchingUser
            # print(f"{searchingUser}")
            # print("potentialFriend", potentialFriend)
            if searchingUser in potentialFriend.keys():
                print(searchingUser)
                friendFriends = checkFriends(potentialFriend[searchingUser])
                print(f"friendFriends: {friendFriends}")
                friendOfSearch.append(user)
            potentialSearches.append(potentialFriend.values())
        
        print(f"friendOf{keyword}: {friendOfSearch}")
            
    except:
        return False


searchingUser = ""
def search(keyword):
    driver.get(f"https://www.facebook.com/search/people/?q={keyword}")
    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=\'article\'] span a')))
        script = 'return document.querySelector("[role=\'article\'] span a");'
        search = driver.execute_script(script)
        global searchingUser
        searchingUser = search.text
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
    
    if userUrl in listOfCheckedProfiles:
        return False
    else:
        listOfCheckedProfiles.append(userUrl)
    
    if "/profile.php?id=" in userUrl: 
        driver.get(f"{userUrl}&sk=friends")
    else:
        driver.get(f"{userUrl}/friends")
    
    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=\'link\']:not(:has(img))')))
        
        scroll_to_bottom_check_friends()
        
        
        script = "return document.querySelectorAll('[role=tab]')[7].text;"
        showsFollowing = driver.execute_script(script)
        
        if showsFollowing == "Volgend":
            return False
        
        
        script = 'return document.querySelectorAll("[role=\'link\']:not(:has(img))");'
        friends = driver.execute_script(script)
        allFriends = {}
        
        for friend in friends:
            if friend.get_attribute('href')== userUrl or friend.text == "" or friend.text == "Vrienden" or " vrienden" in friend.text or "Foto’s" == friend.text or "Check-ins" == friend.text or friend.text == 'Alles weergeven' or friend.text == "Video's" or friend.text == "Vind-ik-leuks":
                continue
            
            # print(friend)
            # print(friend.get_attribute('href'))
            # print(friend.text)
            
            # print(f"{friend.text}")
            allFriends[friend.text] = friend.get_attribute('href')
        return allFriends
    except:
        return False

keyword = os.getenv("keyword")
search(keyword)


# normal search
# search user "userkeyword"
# check friends
# if user has friends return
# else ask "secondkeywyord" search fe city

# revsearch
# check these potential friends
# if user is in friends check these friends, dont continue with potential friends
# if user is not in friends continue with potential friends
