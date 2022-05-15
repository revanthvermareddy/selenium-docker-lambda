import sys
import os
import time
import multiprocessing
import logging

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

###############################################
# Global variables

logging.basicConfig(format='%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

# -- below properties can also be set from the event or os env variable --
options = {
    "browser_binary_location": "/usr/bin/firefox",
    "driver_binary_location": "/usr/local/bin/geckodriver",
    "url": "https://www.google.com/",
    "processes_count": 1,
    "mode": "lamda"
}
    
###############################################

###############################################
# Methods

# -- method to update the options based on the usecase --
def update_global_options(event):
    print("\n --- UPDATING GLOBAL OPTIONS : START ---\n")

    # -- update option from event object if available --
    global options
    for option in options:
        if option in event:
            options[option] = event[option]
            print(f"Using the {option} passed in the event: { options[option] }")
        else:
            print(f"Using the default {option}: { options[option] }")
    
    print("\n --- UPDATING GLOBAL OPTIONS : END ---\n")

def scraper(name, options):
    url = options["url"]
    browser_binary_location = options["browser_binary_location"]
    driver_binary_location = options["driver_binary_location"]
    mode = options["mode"]

    try:
        logging.info(f" -- Starting process: {name} --")

        # -- driver options --
        options = Options()
        options.binary_location = browser_binary_location
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-dev-tools')
        options.add_argument('--user-data-dir=/tmp/chrome-user-data')
        options.add_argument('--single-process')
        options.add_argument("--no-zygote")
        options.add_argument("--ignore-certificate-errors")

        # -- non-local mode specific driver options --
        if mode != "local":
            options.add_argument("--headless")
        
        # -- open firefox driver for web crawling --
        with webdriver.Firefox(options=options, service_log_path=os.path.devnull, executable_path=driver_binary_location) as driver:
            logging.info(f"Trying to crawl url: { url }")
            driver.get(url)
            # elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "waitCreate")))
            time.sleep(10)
            logging.info("Got response from the url..")
            element_text = driver.page_source
            logging.info(f"Page Title: { driver.title }")
            # logging.info(f"Element text: { element_text }")
    except WebDriverException as ex:
        logging.error(f"WebDriverException occurred while crawling the url: { url }\n{ ex }")
        sys.exit(1)
    except Exception as ex:
        logging.error(f"Exception occurred while crawling the url: { url }\n{ ex }")
        sys.exit(1)
    finally:
        logging.info(f"Successfully crawled the url: { url }")
        logging.info(f" -- Finished process: {name} --")
        return f"Hello world from AWS Lambda using python { sys.version }!"

###############################################

# -- handler function --
def lambda_handler(event=None, context=None):
    print(f"Event received: { event }\n")
    
    # -- update global variables from event object if available --
    update_global_options(event)

    start = time.perf_counter()

    # -- create individual processes based on the processes_count --
    processes = []
    for pid in range(options["processes_count"]):
        pr = multiprocessing.Process(target=scraper, args=(str(pid+1), options))
        processes.append(pr)
    
    # -- start each process --
    for process in processes:
        process.start()
    
    # -- need to wait until all the processes got completed --
    for process in processes:
        process.join()
    
    end = time.perf_counter()

    print(f'\nFinished processing in {round(end-start, 2)} second(s)')
 
# -- driver code for local debugging --
if __name__ == "__main__":
    
    # -- local browser and driver paths (uncomment only during local mode testing) --
    browser_binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    driver_binary_location = "C:\\Users\\Administrator\\Downloads\\geckodriver-v0.31.0-win64\\geckodriver.exe"

    # -- url to scrape --
    url = "https://example.com/"

    local_event = {
        "payload": "hello world!",
        "url": url,
        "browser_binary_location": browser_binary_location,
        "driver_binary_location": driver_binary_location,
        "processes_count": 3,
        "mode": "local"
    }
    
    lambda_handler(local_event, None)
