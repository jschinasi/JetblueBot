from flask import Flask, render_template, request
import schedule
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime


# Domestic check-in function with delay before quitting
def check_in_domestic(last_name, confirmation_code):
    dir_path = os.getcwd()
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={dir_path}\\selenium")
    chrome_options.page_load_strategy = 'eager'  # Load DOM and begin interaction before all assets are loaded

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://checkin.jetblue.com/checkin/")

        last_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/jb-app/main/jb-search/jb-search-form/div[2]/div/form/div/div/jb-form-field-container[1]/div/div/input"))
        )
        last_name_field.clear()
        last_name_field.send_keys(last_name)

        confirmation_code_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/jb-app/main/jb-search/jb-search-form/div[2]/div/form/div/div/jb-form-field-container[2]/div/div/input"))
        )
        confirmation_code_field.clear()
        confirmation_code_field.send_keys(confirmation_code)
        confirmation_code_field.submit()

        print("Name and confirmation code submitted")

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-passengers/div[2]/div/jb-transition-button/button"))
        )
        continue_button.click()

        # Wait for Hazardous "Continue" button to be clickable test for bags
        continue_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-hazmat/jb-hazmat-form/jb-transition-button/button"))
        )
        # Click the "Continue" button
        continue_button2.click()

        # Bags continue button
        continue_button3 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-baggage-info/div/jb-loading-container/div/jb-transition-button/button"))
        )
        continue_button3.click()
        # Keep the browser open for 60 seconds before closing
        time.sleep(60)

    except Exception as e:
        print(f"Domestic check-in failed: {str(e)}")

    finally:
        driver.quit()  # Close the browser after the delay

# International check-in function with delay before quitting
def check_in_international(last_name, confirmation_code):
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(options=chrome_options)
    
    
    try:
        driver.get("https://checkin.jetblue.com/checkin/")

        last_name_field = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/jb-app/main/jb-search/jb-search-form/div[2]/div/form/div/div/jb-form-field-container[1]/div/div/input"))
        )
        last_name_field.clear()
        last_name_field.send_keys(last_name)

        confirmation_code_field = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/jb-app/main/jb-search/jb-search-form/div[2]/div/form/div/div/jb-form-field-container[2]/div/div/input"))
        )
        confirmation_code_field.clear()
        confirmation_code_field.send_keys(confirmation_code)
        confirmation_code_field.submit()

        print("International check-in completed")

        # Keep the browser open for 30 seconds before closing
        time.sleep(30)

    except Exception as e:
        print(f"International check-in failed: {str(e)}")

    finally:
        driver.quit()  # Close the browser after the delay

# Function to handle multiple flight check-ins
def schedule_checkin(last_name, confirmation_code, checkin_time, checkin_type):
    def job():
        if checkin_type == 'domestic':
            check_in_domestic(last_name, confirmation_code)
        elif checkin_type == 'international':
            check_in_international(last_name, confirmation_code)

    # Schedule the check-in job for the specified day and time without seconds
    checkin_datetime = datetime.strptime(checkin_time, "%Y-%m-%dT%H:%M")

    day_name = checkin_datetime.strftime('%A').lower()

    # Dynamically schedule based on the day selected, without including seconds
    schedule_time = checkin_datetime.strftime("%H:%M")

    if day_name == "monday":
        schedule.every().monday.at(schedule_time).do(job)
    elif day_name == "tuesday":
        schedule.every().tuesday.at(schedule_time).do(job)
    elif day_name == "wednesday":
        schedule.every().wednesday.at(schedule_time).do(job)
    elif day_name == "thursday":
        schedule.every().thursday.at(schedule_time).do(job)
    elif day_name == "friday":
        schedule.every().friday.at(schedule_time).do(job)
    elif day_name == "saturday":
        schedule.every().saturday.at(schedule_time).do(job)
    elif day_name == "sunday":
        schedule.every().sunday.at(schedule_time).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    last_name = request.form["last_name"]
    confirmation_code = request.form["confirmation_code"]
    checkin_time = request.form["checkin_time"]
    checkin_type = request.form["checkin_type"]

    # Schedule the appropriate check-in
    threading.Thread(target=schedule_checkin, args=(last_name, confirmation_code, checkin_time, checkin_type)).start()

    return f"Check-in scheduled for {last_name} on {checkin_time} as {checkin_type} check-in."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
