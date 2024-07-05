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

listOfCheckedProfiles = []

def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def capture_full_page_screenshot(driver, file_path):
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    # Get the height of the viewport
    viewport_height = driver.execute_script("return window.innerHeight")
    # Set initial position and scroll step
    scroll_position = 0
    scroll_step = viewport_height
    
    # List to hold all the screenshots
    screenshots = []

    # Scroll and capture screenshots
    while scroll_position < total_height:
        # Scroll to the current position
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(1)  # Wait for the page to load
        
        # Capture screenshot
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(screenshot)
        
        # Move to the next scroll position
        scroll_position += scroll_step
    
    # Stitch screenshots together
    stitched_image = stitch_screenshots(screenshots, viewport_height, total_height)
    stitched_image.save(file_path)

def stitch_screenshots(screenshots, viewport_height, total_height):
    # Create a blank image with the total height
    stitched_image = Image.new('RGB', (1920, total_height))
    
    offset = 0
    for screenshot in screenshots:
        img = Image.open(io.BytesIO(screenshot))
        stitched_image.paste(img, (0, offset))
        offset += viewport_height
    
    return stitched_image

site = "https://nl.wikipedia.org/wiki/Hoofdpagina"

driver.get(site)
scroll_to_bottom()

capture_full_page_screenshot(driver, 'full_page_screenshot.png')

driver.quit()
