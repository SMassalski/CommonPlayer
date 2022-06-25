from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .base import BaseController


class YoutubeController(BaseController):
    
    PLAY = 'play'
    AUTOPLAY = 'autoplay'
    FULLSCREEN = 'fullscreen'
    SUBTITLES = 'subtitles'
    HANDLE_COOKIE_POPUP = 'cookie'
    
    def __init__(self, driver):
        super().__init__(driver)
        
        # Element definition
        self.player = None
        self.play_button = None
        self.next_button = None
        self.autoplay_button = None
        self.captions_button = None
        self.fullscreen_button = None
        
        self.actions = {
            self.PLAY: self.toggle_play_pause,
            self.AUTOPLAY: self.toggle_autoplay,
            self.FULLSCREEN: self.toggle_fullscreen,
            self.SUBTITLES: self.toggle_subtitles,
            self.HANDLE_COOKIE_POPUP: self._handle_cookie_popup,
        }
        
        # Handle cookie popup
        # Maybe should somehow keep info on whether popup was handled
        try:
            WebDriverWait(driver, timeout=10).until(self._handle_cookie_popup)
        except TimeoutException:
            pass
        
        if self._is_video():
            WebDriverWait(driver, timeout=5).until(self._fetch_components)

    def play(self):
        if self.play_button.get_attribute('title') == 'Play (k)':
            self.play_button.click()

    def pause(self):
        if self.play_button.get_attribute('title') == 'Pause (k)':
            self.play_button.click()
            
    def toggle_play_pause(self):
        self.play_button.click()
    
    def toggle_autoplay(self):
        self.autoplay_button.click()
        
    def toggle_fullscreen(self):
        self.fullscreen_button.click()
        
    def toggle_subtitles(self):
        self.captions_button.click()

    # _=None because wait.until passes the driver as an argument
    def _fetch_components(self, _=None):
        self.player = self.driver.find_element(By.ID, 'movie_player')
        
        # Play
        self.play_button = self.player.find_element(By.CLASS_NAME,
                                                    'ytp-play-button')
        # Next
        self.next_button = self.player.find_element(By.CLASS_NAME,
                                                    'ytp-next-button')
        # Subtitles
        self.captions_button = self.player.find_element(By.CLASS_NAME,
                                                        'ytp-subtitles-button')
        # Autoplay
        self.autoplay_button = self.player.find_element(
            By.CLASS_NAME,
            'ytp-autonav-toggle-button')
        
        # Fullscreen
        self.fullscreen_button = self.player.find_element(
            By.CLASS_NAME,
            'ytp-fullscreen-button')
        
        # Title
        self.title = self.driver.find_element(By.CSS_SELECTOR,
                                              '#info h1.title')
        return True

    def _handle_cookie_popup(self, _=None):
        popup = self.driver.find_element(By.TAG_NAME,
                                         'ytd-consent-bump-v2-lightbox')
        popup.find_element(By.LINK_TEXT, 'ACCEPT ALL').click()
        return True
        
    def _is_video(self):
        return urlparse(self.driver.current_url).path == '/watch'
    
    def _subtitles_available(self):
        title = self.captions_button.get_attribute('title')
        return title == 'Subtitles/closed captions unavailable'
