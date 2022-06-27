from contextlib import closing
from shutil import which

from server import BrowserServer


def main():
    
    # Later feature: checking available browsers and allowing user to choose
    # or choosing automatically
    """firefox_available = bool(which('geckodriver')) and bool(which('firefox'))
    
    # TODO: Check if these are correct executables for chrome
    chrome_available = \
        (bool(which('chromium')) or bool(which('chromium-browser')))\
        and bool(which('chromedriver'))"""
    
    with closing(BrowserServer()) as server:
        server.run()


if __name__ == '__main__':
    main()
