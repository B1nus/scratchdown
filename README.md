# scratchdown
Download all of your scratch projects fast and easy

This program uses selenium and GeckoDriver in order to emulate a browser and access the ids of your projects. By default this emulator is hidden and runs in the background, but you can make it visible as explained in [Debugging](#Debugging).
# Dependencies
You need to download GeckoDriver For example running the command ```pacman -S geckodriver```on Archlinux. Then you need to change the constant ```GECKO_DRIVER_PATH = ``` located in *geckodriver.py* to the path of GeckoDriver's executable. Get the path by runnig the command ```which geckodriver```.

You also need selenium: ```pip install selenium```.

# Credit
Massive credit to TimMcCool for [scratchattach](https://github.com/TimMcCool/scratchattach). I used his code as reference for much of my code. Some of the code is more or less copied from scratchattach so thank you TimMcCool, I learned a lot from your code.

# Debugging
Firstly there is one massively helpful tool for debugging. That is making the browser emulator visible. Go into the file *geckodriver.py* and comment out this line ```firefox_options.add_argument("--headless")```. There are comments above this line to make it easier to spot.

There is a known issue with this code. That is the way it waits for sites to load. Currently this is implemented through calls to ```time.sleep()``` which is prone to errors since every computers loading times are different. In the calls to functions ```geckodriver.selenium_login()``` and ```geckodriver.raw_html()``` you can change these times through arguments. The calls to these functions are located in *scratchdown.py*. Try increasing the wait times and see if it solves your problems.
