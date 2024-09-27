import downloader
import geckodriver
import getpass
import id_parser
import os
import session
import time

print("""
Welcome to scratchdown. The easiest way to download all of your
Scratch projects.
      """)

# Start selenium while the user is reading the introduction
driver = geckodriver.selenium_init()

username = input("For which user would you like to run scratchdown: ")
password = getpass.getpass("Enter your password: ")

# Login with selenium
driver = geckodriver.selenium_login(username, password, driver)

# Fetch and parse project ids
mystuff_html = geckodriver.raw_html("https://scratch.mit.edu/mystuff/", driver)
project_ids = id_parser.find_ids_in_raw_html(mystuff_html)

trashed_html = None
trashed_ids = None

# Do the same for trashed projects if the user chooses
if input("\nDo you want to download thrashed projects? (y/n) ") == 'y':
    print("Fetching thrashed projects")
    trashed_html = geckodriver.raw_html("https://scratch.mit.edu/mystuff/#trash", driver)
    trashed_ids = id_parser.find_ids_in_raw_html(trashed_html)


# Ask if we got the right amount of ids. The input() comes later
ask_str = "We found {} project's. Is this correct?".format(len(project_ids))
if trashed_ids != None:
    ask_str = "We found {} project's and {} thrashed project's. Is this correct?".format(
            len(project_ids),
            len(trashed_ids)
            )

if input("\n" + ask_str + " (y/n) ") != 'y':
    print("""
    That's unfortunate. Submit a issue through github here:
    https://github.com/B1nus/scratchdown/issues.

    You can also debug the issue yourself:
    https://github.com/B1nus/scratchdown/tree/main?tab=readme-ov-file#Debugging
    """)
    driver.quit()
    exit()

# Get session id and quit the browser emulator
session_id = geckodriver.session_id(driver)
driver.quit()

# Get the user token with the session_id
xtoken = session.xtoken(session_id)

destination = input("\nEnter a destination folder: ")

trash_destination = None
if trashed_ids != None:
    trash_destination = input("""
Enter a destination folder for trashed projects. If left empty,
the trashed projects will be downloaded in the same folder as the
other projects but inside a subfolder called trashed: """)

    # Empty means to use the same destination plus "trashed"
    if trash_destination == '':
        trash_destination = os.path.join(destination, "trashed")

try:
    downloader.bulk_download(project_ids, destination, xtoken)
except:
    print("Error: Destination folder {} is not available".format(destination))

if trash_destination != None:
    try:    
        downloader.bulk_download(trashed_ids, trash_destination, xtoken)
    except:
        print("Error: Destination folder {} is not available".format(destination))

print("\nscratchdown is done, find your projects in the provided folder!\n")

