import socket
import json

from django.conf import settings


class BrowserClient:
    """Client class for communication with a browser server."""
    
    START = 'start'
    EXIT = 'exit'
    GOTO = 'go_to'
    GET = 'get_url'
    CONTROL = 'control'

    # Media controller actions
    PLAY_PAUSE = 'play_pause'
    AUTOPLAY = 'autoplay'
    FULLSCREEN = 'fullscreen'
    SUBTITLES = 'subtitles'
    HANDLE_COOKIE_POPUP = 'cookie'
    
    def __init__(self, address=None):
        self.address = address or settings.BROWSER_SERVER_ADDRESS
        self.socket = None
        
    def __enter__(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(self.address)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()
        self.socket = None
        
    def send(self, value):
        """Send data to the connected server.
        
        Parameters
        ----------
        value : dict
            Data to be sent to the server.
        
        Returns
        -------
        dict
            The received response.
        """
        data = json.dumps(value)
        self.socket.send(data.encode())
        data = self.socket.recv(1024).decode()
        return json.loads(data)
