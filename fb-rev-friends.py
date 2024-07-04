from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

## & 'C:\Program Files\Google\Chrome\Application\Chrome.exe' --remote-debugging-port=5555



options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:5555")
driver = webdriver.Chrome(options=options)


keyword = "Adolf Kitler"

driver.get(f"https://www.facebook.com/search/people/?q={keyword}")

try:
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=\'article\'] span a')))

    # script = 'return document.querySelectorAll("[role=\'article\'] span a");'
    script = 'return document.querySelector("[role=\'article\'] span a");'
    search = driver.execute_script(script)
    
    # for link in search:
    user = search.get_attribute('href')
    driver.get(f"{user}/friends")
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.x78zum5.x1q0g3np.x1a02dak.x1qughib [role=\'link\']:not(:has(img))')))
            
        script = 'return document.querySelectorAll(".x78zum5.x1q0g3np.x1a02dak.x1qughib [role=\'link\']:not(:has(img))");'
        friends = driver.execute_script(script)
        for friend in friends:
            print(f"{friend.text}")
    except:
        print(f'friend is not present on the page.')

finally:
    print("Done")

