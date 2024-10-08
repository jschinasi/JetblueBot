import schedule
import time
from datetime import datetime
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_in(last_name, confirmation_code):

    dir_path = os.getcwd()
    # Configure Chrome options
    chrome_options = Options()

    # chrome_options.add_argument("user-data-dir=selenium")

    chrome_options.add_argument(f"user-data-dir={dir_path}\\selenium") # windows
    # Initialize Chrome WebDriver with configured options
    driver = webdriver.Chrome(options=chrome_options)

    # Open the check-in website
    driver.get("https://checkin.jetblue.com/checkin/")

    try:
        # Find and fill in the last name field
        last_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/jb-app/main/jb-search/jb-search-form/div[2]/div/form/div/div/jb-form-field-container[1]/div/div/input"))
        )
        last_name_field.clear()  # Clear existing text (if any)
        last_name_field.send_keys(last_name)
        print("Last Name entered:", last_name)

        # Find and fill in the confirmation code field
        confirmation_code_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/jb-app/main/jb-search/jb-search-form/div[2]/div/form/div/div/jb-form-field-container[2]/div/div/input"))
        )
        confirmation_code_field.clear()  # Clear existing text (if any)
        confirmation_code_field.send_keys(confirmation_code)
        print("Confirmation Code entered:", confirmation_code)

        # Submit the form
        confirmation_code_field.submit()

        print("Check-in successful!")

        

        # Wait for the first "Continue" button to be clickable
        continue_button1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-passengers/div[2]/div/jb-transition-button/button"))
        )

        # Click the hazardous "Continue" button
        continue_button1.click()

        print("Clicked on first Continue button")

        # Wait for the traveller info "Continue" button to be clickable
        continue_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-hazmat/jb-hazmat-form/jb-transition-button/button"))
        )

        # Click the traveller info "Continue" button
        continue_button2.click()

        print("Clicked on second Continue button")

        # Wait for 3rd "Continue" button to be clickable test for bags
        continue_button3 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-baggage-info/div/jb-loading-container/div/jb-transition-button/button"))
        )
        # Click the 3rd "Continue" button
        continue_button3.click()

    except Exception as e:
        print(f"Check-in failed: {str(e)}")

    # Keep the browser window open for inspection
    input("Press Enter to close the browser...")

    # Close the browser
    driver.quit()

def job():
    # Enter your last name and confirmation code here
    last_name = "Schinasi"
    confirmation_code = "DIHNEW"

    check_in(last_name, confirmation_code)

# Schedule the job to run at 11:59:05 PM on Saturday, March 30
schedule.every().thursday.at("23:05:00").do(job)
# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
