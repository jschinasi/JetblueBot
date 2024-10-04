from flask import Flask, render_template, request
import schedule
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os

app = Flask(__name__)

# Domestic check-in logic (from uploaded script)
def check_in_domestic(last_name, confirmation_code):
    dir_path = os.getcwd()
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={dir_path}\\selenium")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://checkin.jetblue.com/checkin/")
    
    try:
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

        print("Domestic check-in completed")

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-passengers/div[2]/div/jb-transition-button/button"))
        )
        continue_button.click()

    except Exception as e:
        print(f"Domestic check-in failed: {str(e)}")
    finally:
        driver.quit()

# International check-in logic (from uploaded script)
def check_in_international(last_name, confirmation_code):
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://checkin.jetblue.com/checkin/")
    
    try:
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

        # Additional logic for international check-in (e.g., country selection)
        print("International check-in completed")
        
    except Exception as e:
        print(f"International check-in failed: {str(e)}")
    finally:
        driver.quit()

# Scheduling function to run either domestic or international check-in
def schedule_checkin(last_name, confirmation_code, checkin_time, checkin_type):
    def job():
        if checkin_type == 'domestic':
            check_in_domestic(last_name, confirmation_code)
        elif checkin_type == 'international':
            check_in_international(last_name, confirmation_code)

    schedule.every().day.at(checkin_time).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

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

    return f"Check-in scheduled for {last_name} at {checkin_time} as {checkin_type} check-in."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
