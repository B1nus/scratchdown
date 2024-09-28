from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import id_parser
import os
import time

LOGIN_URL = "https://scratch.mit.edu/login/"
PROJECT_PAGE = "https://scratch.mit.edu/projects/{}/editor"
GECKODRIVER_PATH = "/usr/bin/geckodriver"

# Constants that could change if scratch devs decide to change paths
USERNAME_FIELD_ID = "id_username"
PASSWORD_FIELD_ID = "id_password"
LOADMORE_XPATH = "//*[@data-control='load-more']"
FILE_DROPDOWN_XPATH = '//div[contains(@class, "menu-bar_menu-bar-item_NKeCD")][3]'
SAVE_BUTTON_XPATH = '//li[contains(@class, "menu_hoverable_ZLcfJ")][5]'
TITLE_FIELD_XPATH = '//input[@placeholder="Project title here"]'
LOADSCREEN_XPATH = '//div[@class="loader_background_KvT9o"]'

class Emulator:
    def __init__(self, download_dir, trash, headless=True):
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", download_dir)  # Set download directory
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-scratch-project")

        # DEBUGGING:
        #
        # To debug you should comment out this line of code. Now the browser
        # emulator will be visible and problems will be easier to debug.
        if headless:
            options.add_argument("--headless")

        service = Service(GECKODRIVER_PATH)

        self.driver = webdriver.Firefox(service=service, options=options)
        self.trash = trash
        self.download_dir = download_dir

    def login(self, username, password):
        # Open the Scratch login page
        self.driver.get(LOGIN_URL)

        username_field =self.driver.find_element(By.ID, USERNAME_FIELD_ID)
        password_field =self.driver.find_element(By.ID, PASSWORD_FIELD_ID)

        # Write username
        username_field.click()
        username_field.send_keys(username)
        # Write password
        password_field.click()
        password_field.send_keys(password)

        # Submit the form
        password_field.send_keys(Keys.RETURN)

        # Check if login was successful
        try:
            WebDriverWait(self.driver, 2).until(lambda d: d.current_url != LOGIN_URL )
        except:
            self.driver.quit()
            exit("\nInvalid login credentials\n")

    def go_to_page(self, page):
        # Navigate to the page
        self.driver.get(page)
        time.sleep(1)
        WebDriverWait(self.driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Repeatedly click loadmore until all projects are visible and return all ids
    def load_more(self):
        while True:
            time.sleep(1)
            try:
                load_more_button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, LOADMORE_XPATH))
                        )
            except:
                return

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            load_more_button.click()

    # Download all projects currently shown on screen
    def download_projects(self, name_prefix=""):
        ids = id_parser.find_ids_in_raw_html(self.driver.page_source)

        for id in ids:
            self.download_project(id, name_prefix=name_prefix)

    def download_project(self, id, name_prefix=""):
        # Make filename based on command line argument
        filename = name_prefix + str(id)

        print("Downloading {}...".format(os.path.join(self.download_dir, filename)))

        # Load Project and wait
        self.driver.get(PROJECT_PAGE.format(id))

        # Wait until Loading Screen is gone
        time.sleep(1)
        try:
            WebDriverWait(self.driver,20).until(
                    EC.invisibility_of_element_located((By.XPATH, LOADSCREEN_XPATH))
                    )
        except:
            exit("Timed Out. Sorry ):")

        # Save old title
        title_field = self.driver.find_element(By.XPATH, TITLE_FIELD_XPATH)
        title = title_field.get_attribute("value")

        # Set new title
        title_field.click()
        title_field.send_keys(Keys.CONTROL + 'a')
        title_field.send_keys(filename)

        # Press Save to Computer
        file_dropdown = self.driver.find_element(By.XPATH, FILE_DROPDOWN_XPATH)
        file_dropdown.click()
        save_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, SAVE_BUTTON_XPATH))
                )
        save_button.click()

        # Give back the old title
        title_field.click()
        title_field.send_keys(Keys.CONTROL + 'a')
        title_field.send_keys(title + Keys.ENTER)
        file_dropdown.click()
