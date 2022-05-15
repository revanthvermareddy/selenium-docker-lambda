import sys
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

###############################################
# Global variables

browser_binary_location = "/usr/bin/firefox"
driver_binary_location = "/usr/local/bin/geckodriver"

# -- url can also be set from the event or os env variable --
url = "https://www.google.com/"

###############################################

# -- handler function --
def lambda_handler(event=None, context=None):
    print(f"Event received: { event }")
    
    # -- update url from event object if available --
    global url
    if "url" in event:
        url = event["url"]
        print(f"Using the url passed in the event: { url }")
    else:
        print(f"Using the default url: { url }")
    
    try:        
        # -- driver options --
        options = Options()
        options.binary_location = browser_binary_location
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-dev-tools')
        options.add_argument('--user-data-dir=/tmp/chrome-user-data')
        options.add_argument('--single-process')
        options.add_argument("--no-zygote")
        options.add_argument("--ignore-certificate-errors")
        
        # -- open firefox driver for web crawling --
        with webdriver.Firefox(options=options, service_log_path=os.path.devnull, executable_path=driver_binary_location) as driver:
            print(f"Trying to crawl url: { url }")
            driver.get(url)
            print("Got response from the url..")
            element_text = driver.page_source
            print(f"Page Title: { driver.title }")
            print(f"Element text: { element_text }")
    except WebDriverException as ex:
        print(f"WebDriverException occurred while crawling the url: { url }\n{ ex }")
        sys.exit(1)
    except Exception as ex:
        print(f"Exception occurred while crawling the url: { url }\n{ ex }")
        sys.exit(1)
    finally:
        print(f"Successfully crawled the url: { url }")
        return f"Hello world from AWS Lambda using python { sys.version }!"
    
# -- driver code for local debugging --
if __name__ == "__main__":
    event = {
        "payload":"hello world!",
        "url":"https://example.com/"
    }
    lambda_handler(event, None)
