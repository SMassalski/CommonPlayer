"""Implementations of a common interface for browser setup in the form
of driver factories.
"""
from abc import abstractmethod, ABC

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


class BaseDriverFactory(ABC):
    """Driver factory base class."""
        
    @abstractmethod
    def build(self):
        """Create a webdriver.
        
        Returns
        -------
        WebDriver
        """
        pass
    
        
class FirefoxDriverFactory(BaseDriverFactory):
    """Driver factory for Firefox drivers."""
    def __init__(self):
        self.addons = []
    
    def build(self):
        """Create a Firefox webdriver.
        
        Returns
        -------
        webdriver.Firefox
        """
        service = FirefoxService()
        driver = webdriver.Firefox(service=service)
        for addon in self.addons:
            driver.install_addon(addon, True)
        return driver


class ChromeDriverFactory(BaseDriverFactory):
    """Driver factory for Chrome drivers."""
    def __init__(self):
        self.options = ChromeOptions()
        
    def build(self):
        """Create a Chrome webdriver.

        Returns
        -------
        webdriver.Chrome
        """
        service = ChromeService()
        return webdriver.Chrome(service=service, options=self.options)
