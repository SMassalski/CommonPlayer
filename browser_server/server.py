import socket
import json
import logging
from urllib.parse import urlparse

from controllers.youtube import YoutubeController


# FIXME: The server still seems to quit incorrectly
class BrowserServer:
    
    START = 'start'  # Initiate the webdriver
    EXIT = 'exit'  # Close the webdriver
    GOTO = 'go_to'  # Go to a given url
    GET = 'get_url'  # Return the current url
    CONTROL = 'control'  # Send command to media controller
    
    domain_controllers = {
        'www.youtube.com': YoutubeController,
        'youtu.be': YoutubeController
    }
    
    def __init__(self, driver_factory, address):

        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(address)
        self.socket.listen(1)
        
        self.driver_factory = driver_factory
        
        self.driver = None
        self.controller = None
        
        self.connections = []
        
    def run(self):
        """Run the main loop."""
        conn, address = self.await_connection()
        while True:
            data = conn.recv(1024).decode()
    
            if not data:
                conn, address = self.await_connection()
                continue
    
            parsed = json.loads(data)
            command = parsed.get('command')
            value = parsed.get('value')
            logging.debug(f'Command: {command}; Value: {value} from {address}')
    
            if command == self.START:
                self.init_driver()
                self.send(conn)
                
            elif command == self.EXIT:
                self.close_browser()
                self.send(conn)
                conn.close()
                self.connections.remove(conn)
                conn, address = self.await_connection()

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
            logging.warning('Init driver called, but driver was already'
                            ' initialized.')
            return
        self.driver = self.driver_factory.build()
        
    def close(self):
        """Close the browser."""
        
        self.close_browser()
        for conn in self.connections:
            conn.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        
    def close_browser(self):
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
        
    # TODO: Play after page loads
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
            
    def await_connection(self):
        conn, address = self.socket.accept()
        self.connections.append(conn)
        logging.debug(f'{address} connected')
        return conn, address
