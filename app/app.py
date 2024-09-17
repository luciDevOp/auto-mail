# ca sa pornesti proiectu asta trebuie sa ai instalat docker desktop si cred ca docker-compose(librarie -> pip install cred)  
# dupa ce deschizi proiectu in vscode, intri in terminal si scrii docker-compose build 
# dupa ce se termina de builduit, scrii docker-compose up
# si apoi in terminal iti scrie ce ti iesit din codu tau, momentan scrie doar titlu paginii si id-ul inputului de cautare
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import os
import time
import traceback

# Auto install the appropriate ChromeDriver
chromedriver_path = chromedriver_autoinstaller.install()

# Create a Service object
service = ChromeService(executable_path=chromedriver_path)

# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Use the Service object in webdriver.Chrome
driver = webdriver.Chrome(service=service, options=options)

# Example URL
url = 'https://targetare.ro/cauta-firme?state=eyJxdWVyeSI6IiIsImZpbHRlcnMiOltdLCJwYWdlIjp7InNpemUiOjEwLCJmcm9tIjowfSwic29ydEJ5IjoiIn0='
driver.get(url)

try:
    # Wait for the input element to be present in the DOM
    input_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test-subj="comboBoxSearchInput"]'))
    )

    print('Page title was "{}"'.format(driver.title))
    print('Input element found:', input_element.get_attribute('id'))
finally:
    driver.quit()
