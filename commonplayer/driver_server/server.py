import socket
import json
import logging
from urllib.parse import urlparse

from selenium.webdriver.firefox.service import Service
from selenium import webdriver

from controllers.youtube import YoutubeController


class BrowserServer:
    
    START = 'start'  # Initiate the webdriver
    EXIT = 'exit'  # Close the webdriver
    GOTO = 'go_to'  # Go to a given url
    GET = 'get_url'  # Return the current url
    CONTROL = 'control'
    
    domain_controllers = {
        'www.youtube.com': YoutubeController,
        'youtu.be': YoutubeController
    }
    
    def __init__(self, port=7777):
        
        host = socket.gethostname()

        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(1)
        
        self.driver = None
        self.controller = None
        
    def run(self):
        """Run the main loop."""
        conn, address = self.socket.accept()
        logging.debug(f'{address} connected')
        while True:
            data = conn.recv(1024).decode()
    
            if not data:
                conn, address = self.socket.accept()
                logging.debug(f'{address} connected')
                continue
    
            parsed = json.loads(data)
            command = parsed.get('command')
            value = parsed.get('value')
            logging.debug(f'Command: {command}; Value: {value}')
    
            if command == self.START:
                self.init_driver()
                self.send(conn)
                
            elif command == self.EXIT:
                self.close_driver()
                self.send(conn)
                break
                
            elif command == self.GET:
                url = self.current_url
                data = dict(url=url, ok=True)
                if url is None:
                    data['ok'] = False
                self.send(conn, data)
    
            elif command == self.GOTO:
                self.go_to_url(value)
                self.send(conn)
                
            elif command == self.CONTROL:
                self.control_player(value)
                self.send(conn)

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

    # noinspection PyMethodMayBeStatic
    def send(self, conn, data=None):
        """Send data to socket.
        
        Parameters
        ----------
        conn : socket.socket
        data : dict
            Data to be sent. If set to None (default) {'ok':True} is
            sent.
        """
        
        if data is None:
            data = dict(ok=True)
        conn.send(json.dumps(data).encode())
            
    def go_to_url(self, url):
        """Go to a given url.
        
        Parameters
        ----------
        url : str
        """
        if self.driver is not None:
            self.driver.get(url)

        controller_class = self.domain_controllers.get(urlparse(url).netloc)
        if controller_class is None:
            self.controller = None
        elif not isinstance(self.controller, controller_class):
            self.controller = controller_class(self.driver)
           
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
    
    def control_player(self, action):
        """Perform a media controller action.
        
        Parameters
        ----------
        action : str

        """
        
        if action in self.controller.actions:
            self.controller.actions[action]()
        
  
if __name__ == '__main__':
    server = BrowserServer()
    server.run()
