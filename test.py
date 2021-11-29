from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import time

print("Launching driver...")

options = Options()
options.headless = True

def price_found(price):
    file = open('data.txt', 'a')
    time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    file.write(f"{time_str} - {price}\n")

#This example requires Selenium WebDriver 3.13 or newer
with webdriver.Firefox(options=options) as driver:
    print("Loading lme page...")

    driver.get("https://www.lme.com/")
    
    print("Page loaded!\n")

    while (True):
        #Find prices section
        print("\tSearching for prices section...")
        block_section = driver.find_element(By.CLASS_NAME, "metal-block-container")
    
        print("\tFound prices section")

        #Scroll to it
        driver.execute_script("arguments[0].scrollIntoView();", block_section)
        
        print("\tScrolled to it")

        # Wait until that element shows up
        wait = WebDriverWait(driver, 10)

        print("\tWaiting for prices element to load...")
        first_result = wait.until(presence_of_element_located((By.CLASS_NAME, "metal-block__price")))
        
        priceText = first_result.text

        if (priceText):
            print(f"\tPrice text is: {priceText}")
            
            try:
                price_float = float(priceText)
                print(f"PRICE: {priceText}")
                price_found(priceText)
                driver.quit()
                quit()
            except ValueError:
                print("\tText cannot be converted to float!")
            
        else:
            print("\tElement is null :(")
        
        print("\nTrying again...\n")
        time.sleep(1)

  