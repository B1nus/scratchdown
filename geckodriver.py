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
# L + Ratio windows users
WINDOWS_NOT_ALLOWED_CHARS = set('<>:\"/\\|?*') # This is cursed

class Emulator:
    def __init__(self, download_dir, trash, headless=True, timeout=120):
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
        self.timeout = timeout

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
        WebDriverWait(self.driver, self.timeout).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Repeatedly click loadmore until all projects are visible and return all ids
    def load_more(self):
        while True:
            try:
                WebDriverWait(self.driver, self.timeout).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                load_more_button = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, LOADMORE_XPATH))
                        )
            except:
                return

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            load_more_button.click()
            time.sleep(1)

    # Download all projects currently shown on screen
    def download_projects(self, title_format="{id} {name}"):
        ids = id_parser.find_ids_in_raw_html(self.driver.page_source)

        for id in ids:
            self.download_project(id, title_format)

    def compile_filename(filename):
        # Remove trailing whitespace and make mulitspaces into single spaces
        filename = ' '.join(filename.split())
        
        for c in WINDOWS_NOT_ALLOWED_CHARS:
            filename = filename.replace(c, '_')

        return filename

    def download_project(self, id, title_format):

        print("Downloading {} into ".format(PROJECT_PAGE.format(id)), end='')

        # Load Project and wait
        self.driver.get(PROJECT_PAGE.format(id))

        # Wait until Loading Screen is gone
        try:
            WebDriverWait(self.driver,self.timeout).until(
                    EC.invisibility_of_element_located((By.XPATH, LOADSCREEN_XPATH))
                    )
        except:
            exit("Timed Out. Sorry ):")

        # Save old title
        title_field = self.driver.find_element(By.XPATH, TITLE_FIELD_XPATH)
        title = title_field.get_attribute("value")

        # Filename. Account for characters not allowed by windows
        filename = title_format.format(id=id, title=title)
        filename = Emulator.compile_filename(filename)

        path = os.path.join(self.download_dir, filename + ".sb3")
        print(path)

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

        # Wait for the file to download
        starttime = time.time()
        while True:
            if os.path.exists(path):
                break
            elif time.time() - starttime > self.timeout:
                print("This shouldn't happen. But ok.")
                break
            time.sleep(0.5)

