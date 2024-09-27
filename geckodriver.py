from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

LOGIN_URL = "https://scratch.mit.edu/login/"
GECKO_DRIVER_PATH = "/usr/bin/geckodriver"
USERNAME_HTML_ID = "id_username"
PASSWORD_HTML_ID = "id_password"
LOADMORE_XPATH = "//*[@data-control='load-more']"

# Initialize Geckodriver and selenium
def selenium_init():
    firefox_options = Options()

    # DEBUGGING:
    #
    # To debug you should comment out this line of code. Now the browser
    # emulator will be visible and problems will be easier to debug.
    firefox_options.add_argument("--headless")

    # Initialize the Firefox browser using GeckoDriver
    service = Service(GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=firefox_options)

    return driver

# Returns the same driver but logged in
def selenium_login(username, password, driver, login_wait_time=1):
    # Open the Scratch login page
    driver.get(LOGIN_URL)

    username_field = driver.find_element(By.ID, USERNAME_HTML_ID)
    password_field = driver.find_element(By.ID, PASSWORD_HTML_ID)

    # Write username
    username_field.click()
    username_field.send_keys(username)
    # Write password
    password_field.click()
    password_field.send_keys(password)

    # Submit the form
    password_field.send_keys(Keys.RETURN)

    print("\nLogging in...")
    # Wait untill logged in
    time.sleep(login_wait_time)

    return driver

# Use selenium to get the session_id
def session_id(driver):
    # After login, get cookies from the browser
    cookies = driver.get_cookies()

    # Find the session ID in cookies
    session_id = None
    for cookie in cookies:
        if cookie['name'] == 'scratchsessionsid':  # Cookie name for Scratch session ID
            session_id = cookie['value']
            break

    return session_id

# Use selenium driver to get the raw html of a page
def raw_html(page, driver, page_load_wait_time=1, loadmore_wait_time=1):
    # Navigate to the page
    driver.get(page)

    print("Loading page...")

    # Wait for the page to load
    time.sleep(page_load_wait_time)

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_more_button = driver.find_element(By.XPATH, LOADMORE_XPATH)

        # Break out of the loop if there is no Load More Button
        if load_more_button.location_once_scrolled_into_view['x'] == 0:
            break

        print("Loading More Projects...")
        load_more_button.click()

        # Wait for the new projects to load and check if the button is still there
        time.sleep(loadmore_wait_time)

    # Return the raw html data
    raw_html = driver.page_source
    return raw_html
