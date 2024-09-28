# scratchdown
Download all of your scratch projects fast and easy. Works for unshared projects and trashed alike.

This program uses selenium and GeckoDriver in order to emulate a browser and access the your projects. By default this emulator is hidden and runs in the background, but you can make it visible with the command line flag ```-d```.
# Dependencies
You need to install your systems verison of GeckoDriver. For example by running ```pacman -S geckodriver``` on Archlinux. Then you need to change the constant ```GECKODRIVER_PATH = ``` located in *geckodriver.py* to the path of GeckoDriver's your executable. Get the path by runnig the command ```which geckodriver``` on linux.

You also need selenium: ```pip install selenium```.

# Usage
Run ```python scratchdown.py /path/to/downlad/folder```. There are two command line flags, ```-t``` for downloading trashed projects and ```-d``` enables debug mode. It makes the browser emulator visible. Do not separate the flags into two arguments, my program won't understand you. If you want to both download trashed projects and have debugger mode use the flag ```-td``` or ```-dt```.

# Debugging
A helpful tool for debugging is making the browser emulator visible. As said in [Usage](#Usage) you use the flag ```-d``` to do this.

# Known Issue
I have tried my best to remove most of the calls to ```time.sleep()```, but there are still som left in *geckodriver.py*. If you run into trouble, chances are it's this guys fault.
