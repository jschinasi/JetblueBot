import schedule
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def check_in(last_name, confirmation_code):
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 2})

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

        # Select all travellers
        select_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-passengers/div[2]/div/div/button"))
        )
        select_all_button.click()
        print("Clicked on select all travellers")

        # Wait for the first "Continue" button to be clickable
        continue_button1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-passengers/div[2]/div/jb-transition-button/button"))
        )
        continue_button1.click()
        print("Clicked on first Continue button")

        # Wait for the traveler info "Continue" button to be clickable
        continue_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-hazmat/jb-hazmat-form/jb-transition-button/button"))
        )
        continue_button2.click()
        print("Clicked on second Continue button")

        # Wait for the third "Continue" button to be clickable
        continue_button3 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-hazmat/jb-hazmat-form/jb-transition-button/button"))
        )
        continue_button3.click()
        print("Clicked on third Continue button")

        # Wait for the fourth "Continue" button to be clickable (passport information)
        continue_button4 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-traveler-information/jb-passport-information/form/div[2]/jb-transition-button/button"))
        )
        continue_button4.click()
        print("Clicked on fourth Continue button")

        # Interact with the country dropdown
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-traveler-information/jb-additional-information/form/div[1]/jb-traveler-form-country/jb-traveler-form-dropdown/jb-form-field-container/jb-select/div/button"))
        )
        dropdown.click()
        print("Clicked on dropdown")

        # Use ActionChains to select the country 'United States'
        country_xpath = "/html/body/jb-app/main/jb-traveler-information/jb-additional-information/form/div[1]/jb-traveler-form-country/jb-traveler-form-dropdown/jb-form-field-container/jb-select/div/jb-flyout-inner/div/jb-select-option[233]/div"
        country_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, country_xpath))
        )

        actions = ActionChains(driver)
        actions.move_to_element(country_option).click().perform()
        print("Selected United States option using ActionChains")

        # Wait for the 5th "Continue" button to be clickable (additional traveller)
        continue_button5 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-traveler-information/jb-additional-information/form/div[2]/jb-transition-button/button"))
        )
        continue_button5.click()
        print("Clicked on 5th Continue button")

        # 2nd additional traveller info
        # Wait for the 6th "Continue" button to be clickable (additional traveller)
        continue_button6 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-traveler-information/jb-passport-information/form/div[2]/jb-transition-button/button"))
        )
        continue_button6.click()
        print("Clicked on 6th Continue button")

        # Interact with the country dropdown
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-traveler-information/jb-additional-information/form/div[1]/jb-traveler-form-country/jb-traveler-form-dropdown/jb-form-field-container/jb-select/div/button"))
        )
        dropdown.click()
        print("Clicked on dropdown")

        # Use ActionChains to select the country 'United States'
        country_xpath = "/html/body/jb-app/main/jb-traveler-information/jb-additional-information/form/div[1]/jb-traveler-form-country/jb-traveler-form-dropdown/jb-form-field-container/jb-select/div/jb-flyout-inner/div/jb-select-option[233]/div"
        country_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, country_xpath))
        )

        actions = ActionChains(driver)
        actions.move_to_element(country_option).click().perform()
        print("Selected United States option using ActionChains")

        # Wait for the 7th "Continue" button to be clickable (additional traveller)
        continue_button7 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-traveler-information/jb-additional-information/form/div[2]/jb-transition-button/button"))
        )
        continue_button7.click()
        print("Clicked on 7th Continue button")

        # bags continue
        continue_button8 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/jb-app/main/jb-baggage-info/div/jb-loading-container/div/jb-transition-button/button"))
        )
        continue_button8.click()
        print("Clicked on 8th Continue button")
    except Exception as e:
        print(f"Check-in failed: {str(e)}")
    
    finally:
        # Close the browser
        driver.quit()

def job():
    # Enter your last name and confirmation code here
    last_name = "Schinasi"
    confirmation_code = "DBISLF"

    check_in(last_name, confirmation_code)

    # Schedule the job to run at 11:59:05 PM on
schedule.every().wednesday.at("12:59:40").do(job)

    # Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
