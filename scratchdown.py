#!/usr/bin/env /home/linus/Projekt/scratchdown/bin/python
import cli
from geckodriver import Emulator
import getpass
import os
import time

# Read command line arguments
download_dir, trash, debug = cli.validate(os.sys.argv[1:])

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

print("\nI will download projects into {}\n".format(os.path.abspath(download_dir)))

# Login
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

print("\nLogging in through emulator...")
emulator = Emulator(download_dir, trash, headless=not debug)
emulator.login(username, password)


print("Beginning download...")
# Shared Projects
emulator.go_to_page("https://scratch.mit.edu/mystuff/#shared")
emulator.load_more()
emulator.download_projects("{id}_SHARED - {title}")
# Unshared Projects
emulator.go_to_page("https://scratch.mit.edu/mystuff/#unshared")
emulator.load_more()
emulator.download_projects("{id}_UNSHARED - {title}")

if trash:
    print("\nBeginning download of trashed projects...")
    emulator.go_to_page("https://scratch.mit.edu/mystuff/#trash")
    emulator.load_more()
    emulator.download_projects("{id}_TRASHED - {title}")

emulator.driver.quit()
exit("\nscratchdown is done downloading to {}!\n".format(download_dir))
