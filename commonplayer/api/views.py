from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .client import BrowserClient
from .serializers import CommandSerializer, NavigateSerializer, \
    ControlSerializer


class BrowserClientView(APIView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = BrowserClient()
        
    # TODO: Handling server failures ({'ok': False} responses)
    def send_to_browser_server(self, data):
        with self.client:
            browser_response = self.client.send(data)
        if not browser_response.get('ok'):
            return Response(browser_response,
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(browser_response)
        

class NavigateView(BrowserClientView):
    """Navigate to or get current url
    https://www.youtube.com/watch?v=AvtVuHMqOOM"""
    # Added url for easy access when manually testing
    
    serializer_class = NavigateSerializer

    def get(self, _):
        """Get the current url of the browser"""
        data = {
            'command': BrowserClient.GET
        }
        return self.send_to_browser_server(data)

    def post(self, request):
        """Go to a url"""
        data = {
            'command': BrowserClient.GOTO,
            'value': request.data.get('url'),
        }
        return self.send_to_browser_server(data)
    
    
class LifecycleView(BrowserClientView):
    """Control the browser's lifecycle"""
    serializer_class = CommandSerializer

    def post(self, request):
        """Send a command to the server
        
        Available commands:
        - Start: start a browser
        - End: close a browser
        """
        
        return self.send_to_browser_server(request.data)
    
        
class ControlView(BrowserClientView):
    """Issue commands to the media controller"""
    
    serializer_class = ControlSerializer
    
    def post(self, request):
        data = dict(command=BrowserClient.CONTROL)
        data['value'] = request.data.get('action')
        return self.send_to_browser_server(data)
