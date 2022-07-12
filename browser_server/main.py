from contextlib import closing
from shutil import which
import argparse
import sys

from server import BrowserServer
from driver_factories import FirefoxDriverFactory, ChromeDriverFactory

FIREFOX = "F"
CHROME = "C"


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--addon",
        action="append",
        help="Path to an addon to be installed (.xpi or .crx"
        " file). Argument can be used multiple times.",
    )
    parser.add_argument(
        "--bind",
        default="/tmp/browser.sock",
        help="Path to the unix socket the server will bind" " to.",
    )

    browser_flag_descriptions = (
        "Flags determining which browser to use."
        " If neither flag is used the "
        "browser will be selected automatically "
        "depending on available executables. Only"
        " Chrome and Firefox are supported."
    )
    browser_flags = parser.add_argument_group(
        "Browser flags", browser_flag_descriptions
    )
    browser_flags.add_argument(
        "--firefox", action="store_true", help="Use Firefox browser."
    )
    browser_flags.add_argument(
        "--chrome", action="store_true", help="Use Chrome browser."
    )

    args = parser.parse_args(argv)

    # Browser selection
    firefox_available = bool(which("geckodriver")) and bool(which("firefox"))
    chrome_available = (
        bool(which("chromium")) or bool(which("chromium-browser"))
    ) and bool(which("chromedriver"))

    if firefox_available and (args.firefox or not args.chrome):
        browser = FIREFOX
    elif chrome_available:
        browser = CHROME
    else:
        raise FileNotFoundError("Browser or driver executables not in path")

    driver_factory = (
        FirefoxDriverFactory() if browser == FIREFOX else ChromeDriverFactory()
    )

    # addon installation
    addons = args.addon or []
    driver_factory.add_extensions(*addons)

    with closing(BrowserServer(driver_factory, address=args.bind)) as server:
        server.run()


if __name__ == "__main__":
    main(sys.argv[1:])
