import socket
import json
import logging

from selenium.webdriver.firefox.service import Service
from selenium import webdriver


class BrowserServer:
    
    START = 'start'  # Initiate the webdriver
    EXIT = 'exit'  # Close the webdriver
    GOTO = 'go_to'  # Go to a given url
    GET = 'get_url'  # Return the current url
    
    def __init__(self, port=7777):
        
        host = socket.gethostname()

        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(1)
        
        self.driver = None
        
    def run(self):
        """Run the main loop."""
        conn, address = self.socket.accept()
        while True:
            data = conn.recv(1024).decode()
    
            if not data:
                conn, address = self.socket.accept()
                continue
    
            parsed = json.loads(data)
            command = parsed.get('command')
            value = parsed.get('value')
            logging.debug(f'Command: {command}; Value: {value}')
    
            if command == self.START:
                self.init_driver()
                
            elif command == self.EXIT:
                self.close_driver()
                break
                
            elif command == self.GET:
                url = self.current_url
                data = {
                    'url': url,
                    'ok': True
                }
                if url is None:
                    data['ok'] = False
                conn.send(json.dumps(data).encode())
    
            elif command == self.GOTO:
                self.go_to_url(value)

        conn.close()

    def init_driver(self):
        """Initialize the browser."""
        if self.driver is not None:
            logging.warning('Init driver called, but driver was already '
                            'initialized.')
            return
        service = Service()
        self.driver = webdriver.Firefox(service=service)
        
    def close_driver(self):
        """Close the browser."""
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
            
    def go_to_url(self, url):
        """Go to a given url.
        
        Parameters
        ----------
        url : str
        """
        if self.driver is not None:
            self.driver.get(url)
           
    @property
    def current_url(self):
        """The url the browser is currently on.
        
        Returns
        -------
        str
        """
        if self.driver is not None:
            return self.driver.current_url
        return None
        
  
if __name__ == '__main__':
    server = BrowserServer()
    server.run()
