from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
import os
from dotenv import load_dotenv
import io

load_dotenv()

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:5555")
driver = webdriver.Chrome(options=options)

# driver.get("https://en.key-test.ru/")

# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
# body_element = driver.find_element(By.CSS_SELECTOR, "body")

actions = ActionChains(driver)
actions.send_keys(Keys.ARROW_UP).perform()
# actions.send_keys("Hello, this is a test input!").perform()
