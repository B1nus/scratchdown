import os

# Validate command line arguments. don't forget to set args = os.sys.argv[1:] so we skip the first element
def validate(args):
    if len(args) == 0 or args[0] == "--help" or args[0] == "help" or args[0] == "-h" or args[0] == "-help":
        exit("""
scratchdown.py - Download all of your Scratch Projects fast and easy.

Usage: 'python scratchdown.py [download_folder] -[flags]'

Flags: use flag -t to download trashed projects and flag -d to enable the browser emulator gui (debugger mode).

Please Not: Do not separate the flags if you're using both write '-td' or '-dt'. 
              """)
    if len(args) == 0:
        exit("Missing argument. Argument for download directory missing. Example 'python scratchdown.py ./projects/'")
    if len(args) > 2:
        exit("Too many arguments. Only two are allowed")
    if len(args) == 2:
        if args[1][0] != "-" or len(args[1]) > 3 or len(set(args[1]) - set(['d','t','-'])) > 0:
            exit("Invalid seccond argument. Run 'python scratchdown.py --help' for more information")
    download_dir = args[0]
    if args[0][0] == '-' and len(args[0]) <=4:
        if 'y' != input("""\nHey there fella. That first argument looks a lot like a flag. Are
you sure you want to download your project into the folder called '{}'? (y/n) """.format(download_dir)):
            exit("\nPlease Come again.\n")
            
    if os.path.exists(download_dir) and os.listdir(download_dir):
        exit("The destination folder is not empty! It must be empty.")

    return (
            download_dir,
            len(args) == 2 and 't' in args[1],
            len(args) == 2 and 'd' in args[1],
            )


