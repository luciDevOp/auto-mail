from app import app
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import os
import time
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)



# ca sa pornesti proiectu asta trebuie sa ai instalat docker desktop si cred ca docker-compose(librarie -> pip install cred)  
# dupa ce deschizi proiectu in vscode, intri in terminal si scrii docker-compose build (o sa dureze cam 3 min)
# dupa ce se termina de builduit, scrii docker-compose up
# dupa intri in http://localhost:8081/ si o sa vezi Hello, World! (asta pagina home)
# daca intri in http://localhost:8081/cox o sa se apeleze functia cox( def cox(): de la linia 26) adica ala de webscraping si o sa iti returneze un json

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/cox')
def cox():
    # Auto install the appropriate ChromeDriver
    chromedriver_autoinstaller.install()
    
    # Find the path to the chromedriver executable
    chromedriver_path = chromedriver_autoinstaller.install()
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Use the chromedriver executable path explicitly
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    url = 'https://targetare.ro/cauta-firme?state=eyJxdWVyeSI6IiIsImZpbHRlcnMiOltdLCJwYWdlIjp7InNpemUiOjEwLCJmcm9tIjowfSwic29ydEJ5IjoiIn0='
    driver.get(url)
    current_url = None


    try:
        # Wait for the input element to be present in the DOM
        input_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test-subj="comboBoxSearchInput"]'))
        )

        # Scroll to the element using JavaScript
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", input_element)
        time.sleep(1)  # Allow time for scrolling

        # Focus on the input element and ensure it is interactive
        if input_element.is_displayed():
            logging.info("Element is now visible!")

            # Click the input field to activate it
            input_element.click()
            time.sleep(1)  # Allow time for the input to become active

            # Send the value '01' to the input
            input_element.send_keys("01")
            time.sleep(1)

            # Press arrow down to select the dropdown option
            input_element.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)

            # Press Enter to select the option
            input_element.send_keys(Keys.ENTER)

            # Wait for results (adjust as needed)
            time.sleep(5)
            current_url = driver.current_url
        else:
            logging.error("Element is not visible.")
            current_url = 'Error: Element not visible'

        driver.quit()

        return jsonify({'url': current_url})
    except Exception as e:
        # Capture and log the full exception details
        error_message = str(e)
        error_traceback = traceback.format_exc()
        driver.quit()
        return jsonify({"error": error_message, "traceback": error_traceback}), 500


