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
MAX_TRIES=10

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
def printred(msg):
    if (DEBUG):
        return print(bcolors.FAIL + msg + bcolors.ENDC)
    return


if (DEBUG):
    print(bcolors.OKCYAN + "DEBUG MODE" + bcolors.ENDC)

printlog("Launching driver...")

options = Options()
options.headless = True


def price_found(driver, prices, close_date):
    time_str = datetime.now().strftime("%d/%m/%Y %H/%M/%S")
    price_str = ','.join(prices)
    # file = open('data.txt', 'a')
    # file.write(f"{time_str} - {price}\n")

    print(f"log_date:{time_str},close_date:{close_date},{price_str}")


    printlog("Quitting")
    driver.quit()
    sys.exit(1)

def fetch_website(driver):
    printlog("\nTrying...\n")
    time.sleep(1)

    block_container = driver.find_element(By.CLASS_NAME, "metal-block-container")

    #Scroll to it
    driver.execute_script("arguments[0].scrollIntoView();", block_container)
    printgreen("\tScrolled!")

    #Find prices sections
    printlog("\tSearching for prices sections...")
    block_sections = driver.find_elements(By.CLASS_NAME, "metal-block-row__blocks")

    if (not block_sections or len(block_sections) < 2):
        return

    printgreen(f"\tNum sections is {len(block_sections)}!")

    section_to_fetch = block_sections[1]
    
    price_elements = section_to_fetch.find_elements(By.CLASS_NAME, "metal-block__inner")

    if (not price_elements):
        return

    prices = []
    for element in price_elements:
        try:
            price = element.find_element(By.CLASS_NAME, "metal-block__price").text
            price_float = float(price) # check if it is a number or not
            name = element.find_element(By.CLASS_NAME, "metal-block__title-text").text
            prices.append(f"{name}:{price}")
        except:
            printred("\tPrices not fully loaded")
            return

    # Get the date object
    printlog("\tGetting date element...")
    date_element = WebDriverWait(driver, 10).until(presence_of_element_located((By.CLASS_NAME, "metal-block-container__refreshed-on")))
    try:
        date_str = date_element.text
    except:
        return
    printgreen(f"\tDate is {date_str}!")

    # FINISH IT
    price_found(driver, prices, date_str)


with webdriver.Firefox(options=options) as driver:
    printlog("Loading lme page...")

    driver.get("https://www.lme.com/")
    
    printlog("Page loaded!\n")

    num_tries = 0

    while(num_tries < MAX_TRIES):
        num_tries += 1
        try:
            fetch_website(driver)
        except Exception as e:
            printred(e)
            time.sleep(2)
