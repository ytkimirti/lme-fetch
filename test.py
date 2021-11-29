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
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

DEBUG=True

if (len(sys.argv) >= 2 and sys.argv[1] == "-s"):
    DEBUG=False

def printlog(msg):
    # return print(msg)
    if (DEBUG):
        return print(bcolors.WARNING + msg + bcolors.ENDC)
    return
def printgreen(msg):
    if (DEBUG):
        return print(bcolors.OKGREEN + msg + bcolors.ENDC)
    return


if (DEBUG):
    print(bcolors.OKCYAN + "DEBUG MODE" + bcolors.ENDC)

printlog("Launching driver...")

options = Options()
# options.headless = True


def price_found(price):
    time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # file = open('data.txt', 'a')
    # file.write(f"{time_str} - {price}\n")

    print(f"{time_str} - {price}")


    driver.quit()
    quit()

#This example requires Selenium WebDriver 3.13 or newer
with webdriver.Firefox(options=options) as driver:
    printlog("Loading lme page...")

    driver.get("https://www.lme.com/")
    
    printlog("Page loaded!\n")

    while (True):
        #Find prices section
        printlog("\tSearching for prices section...")
        block_section = driver.find_element(By.CLASS_NAME, "metal-block-container")
    
        printgreen("\tFound prices section!")

        #Scroll to it
        driver.execute_script("arguments[0].scrollIntoView();", block_section)
        
        printgreen("\tScrolled to it!")

        # Wait until that element shows up
        wait = WebDriverWait(driver, 10)

        printlog("\tWaiting for prices element to load...")
        first_result = wait.until(presence_of_element_located((By.CLASS_NAME, "metal-block__price")))
        
        priceText = ""

        try: 
            priceText = first_result.text
        except:
            continue

        if (priceText):
            printlog(f"\tPrice text is: {priceText}")
            
            try:
                price_float = float(priceText)
                printgreen(f"PRICE: {priceText}")
                price_found(priceText)
                
            except ValueError:
                pass
                printlog("\tText cannot be converted to float!")
        # else:
            printlog("\tElement is null :(")
        
        printlog("\nTrying again...\n")
        time.sleep(1)

  