from contextlib import closing
from shutil import which
import argparse
import sys

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver

from server import BrowserServer


def main(argv):
    
    parser = argparse.ArgumentParser()
    
    browser_flag_descriptions = 'Flags determining which browser to use.' \
                                ' If neither flag is used the ' \
                                'browser will be selected automatically ' \
                                'depending on available executables. Only' \
                                ' Chrome and Firefox are supported.'
    browser_flags = parser.add_argument_group('Browser flags',
                                              browser_flag_descriptions)
    browser_flags.add_argument('--firefox', action='store_true',
                               help='Use Firefox browser.')
    browser_flags.add_argument('--chrome', action='store_true',
                               help='Use Chrome browser.')
    
    args = parser.parse_args(argv)

    # Browser selection
    firefox_available = bool(which('geckodriver')) and bool(which('firefox'))
    chrome_available = \
        (bool(which('chromium')) or bool(which('chromium-browser')))\
        and bool(which('chromedriver'))
    
    if args.firefox:
        if not firefox_available:
            raise FileNotFoundError('Either geckodriver or firefox are '
                                    'not in path.')
        service_class = FirefoxService
        driver_class = webdriver.Firefox
    elif args.chrome:
        if not chrome_available:
            raise FileNotFoundError('Either chromium, chromium-browser'
                                    'or chromedriver are not in path.')
        service_class = ChromeService
        driver_class = webdriver.Chrome
    elif firefox_available:
        service_class = FirefoxService
        driver_class = webdriver.Firefox
    elif chrome_available:
        service_class = ChromeService
        driver_class = webdriver.Chrome
    else:
        raise FileNotFoundError('Browser or driver executables not in path')
    
    with closing(BrowserServer(driver_class, service_class)) as server:
        server.run()


if __name__ == '__main__':
    main(sys.argv[1:])
